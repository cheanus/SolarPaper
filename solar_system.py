"""
太阳系壁纸生成器
使用 skyfield 计算行星实时位置，使用 cairo 绘制
"""

import math
import cairo
from datetime import datetime
from skyfield.api import load
import config


class SolarSystemRenderer:
    def __init__(self):
        """初始化渲染器"""
        self.width = config.IMAGE_WIDTH
        self.height = config.IMAGE_HEIGHT
        self.center_x = config.CENTER_X
        self.center_y = config.CENTER_Y

        # 加载天文数据
        self.ts = load.timescale()
        self.eph = load("de421.bsp")  # 行星星历表

        # 获取天体对象
        self.sun = self.eph["sun"]
        self.planets_obj = {
            "mercury": self.eph["mercury"],
            "venus": self.eph["venus"],
            "earth": self.eph["earth"],
            "mars": self.eph["mars"],
            "jupiter": self.eph["jupiter barycenter"],
            "saturn": self.eph["saturn barycenter"],
            "uranus": self.eph["uranus barycenter"],
            "neptune": self.eph["neptune barycenter"],
        }

    def get_planet_position(self, planet_name, time):
        """
        获取行星在指定时间的位置（日心坐标系）
        返回: (x, y) 相对于太阳的位置，单位：天文单位
        """
        planet = self.planets_obj[planet_name]

        # 计算行星相对于太阳的位置
        astrometric = planet.at(time).observe(self.sun)  # type:ignore
        ra, dec, distance = astrometric.radec()

        # 使用 ecliptic 坐标系更准确
        # 获取行星相对于太阳系质心的位置
        barycentric = planet.at(time)  # type:ignore
        sun_barycentric = self.sun.at(time)  # type:ignore

        # 计算相对位置向量
        pos = barycentric.position.au - sun_barycentric.position.au

        # 返回 x, y 坐标（忽略 z 轴，投影到黄道面）
        return pos[0], pos[1]

    def get_moon_position(self, time):
        """获取月球相对于地球的位置"""
        earth = self.eph["earth"]
        moon = self.eph["moon"]

        # 月球相对于地球的位置
        earth_pos = earth.at(time)  # type:ignore
        moon_pos = moon.at(time)  # type:ignore

        relative_pos = moon_pos.position.au - earth_pos.position.au
        return relative_pos[0], relative_pos[1]

    def draw_orbit(self, ctx, radius, color, dashed=True):
        """绘制轨道圆圈"""
        ctx.save()
        ctx.set_source_rgba(*color)
        ctx.set_line_width(config.ORBIT_LINE_WIDTH)

        if dashed:
            ctx.set_dash(config.ORBIT_DASH_PATTERN)

        ctx.arc(self.center_x, self.center_y, radius, 0, 2 * math.pi)
        ctx.stroke()
        ctx.restore()

    def draw_planet(self, ctx, x, y, planet_config):
        """绘制行星"""
        size = planet_config["size"]
        color = planet_config["color"]

        # 绘制行星主体
        ctx.save()
        ctx.set_source_rgb(*color)
        ctx.arc(x, y, size, 0, 2 * math.pi)
        ctx.fill()

        # 添加高光效果
        gradient = cairo.RadialGradient(
            x - size * 0.3, y - size * 0.3, size * 0.2, x, y, size
        )
        gradient.add_color_stop_rgba(0, 1, 1, 1, 0.3)
        gradient.add_color_stop_rgba(1, color[0], color[1], color[2], 0)
        ctx.set_source(gradient)
        ctx.arc(x, y, size, 0, 2 * math.pi)
        ctx.fill()
        ctx.restore()

    def draw_sun(self, ctx, planet_config):
        """绘制太阳（带光晕效果）"""
        x, y = self.center_x, self.center_y
        size = planet_config["size"]
        color = planet_config["color"]

        # 绘制光晕
        if planet_config.get("glow"):
            glow_radius = planet_config["glow_radius"]
            gradient = cairo.RadialGradient(x, y, size, x, y, glow_radius)
            gradient.add_color_stop_rgba(0, color[0], color[1], color[2], 0.8)
            gradient.add_color_stop_rgba(0.5, color[0], color[1], color[2], 0.2)
            gradient.add_color_stop_rgba(1, color[0], color[1], color[2], 0.0)
            ctx.set_source(gradient)
            ctx.arc(x, y, glow_radius, 0, 2 * math.pi)
            ctx.fill()

        # 绘制太阳主体
        ctx.set_source_rgb(*color)
        ctx.arc(x, y, size, 0, 2 * math.pi)
        ctx.fill()

    def draw_saturn_ring(self, ctx, x, y, planet_config):
        """绘制土星环"""
        if not planet_config.get("has_ring"):
            return

        ctx.save()
        inner = planet_config["ring_inner"]
        outer = planet_config["ring_outer"]
        color = planet_config["ring_color"]

        # 创建环的渐变效果
        ctx.set_source_rgba(*color)
        ctx.set_line_width(outer - inner)
        ctx.arc(x, y, (inner + outer) / 2, 0, 2 * math.pi)
        ctx.stroke()
        ctx.restore()

    def draw_decorative_bodies(self, ctx):
        """绘制装饰性小天体"""
        if not config.SHOW_DECORATIVE_BODIES:
            return

        import random

        random.seed(42)  # 固定种子，保持一致性

        for i in range(config.DECORATIVE_BODY_COUNT):
            # 随机分布在小行星带区域（火星和木星之间）
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(320, 420)

            x = self.center_x + radius * math.cos(angle)
            y = self.center_y + radius * math.sin(angle)
            size = random.uniform(*config.DECORATIVE_BODY_SIZE_RANGE)

            ctx.set_source_rgba(*config.DECORATIVE_BODY_COLOR)
            ctx.arc(x, y, size, 0, 2 * math.pi)
            ctx.fill()

    def render(self, output_path="solar_system.png", time=None):
        """
        渲染太阳系图像

        Args:
            output_path: 输出文件路径
            time: datetime 对象，如果为 None 则使用当前时间
        """
        # 创建画布
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        ctx = cairo.Context(surface)

        # 填充背景
        ctx.set_source_rgb(*config.BACKGROUND_COLOR)
        ctx.paint()

        # 设置时间
        if time is None:
            time = datetime.now()
        t = self.ts.utc(
            time.year, time.month, time.day, time.hour, time.minute, time.second
        )

        # 绘制轨道
        for planet_name, planet_config in config.PLANETS.items():
            if planet_name == "sun":
                continue
            orbit_radius = planet_config["orbit_radius"]
            orbit_color = planet_config["orbit_color"]
            self.draw_orbit(ctx, orbit_radius, orbit_color, config.ORBIT_DASHED)

        # 绘制装饰性小天体
        self.draw_decorative_bodies(ctx)

        # 绘制太阳
        self.draw_sun(ctx, config.PLANETS["sun"])

        # 绘制行星
        for planet_name, planet_config in config.PLANETS.items():
            if planet_name == "sun":
                continue

            # 获取行星实际位置
            pos_x_au, pos_y_au = self.get_planet_position(planet_name, t)

            # 转换为屏幕坐标
            # 计算角度
            angle = math.atan2(pos_y_au, pos_x_au)

            # 使用配置的视觉轨道半径
            orbit_radius = planet_config["orbit_radius"]
            screen_x = self.center_x + orbit_radius * math.cos(angle)
            screen_y = self.center_y + orbit_radius * math.sin(angle)

            # 绘制土星环（在行星之前）
            if planet_name == "saturn":
                self.draw_saturn_ring(ctx, screen_x, screen_y, planet_config)

            # 绘制行星
            self.draw_planet(ctx, screen_x, screen_y, planet_config)

            # 绘制月球
            if planet_config.get("has_moon"):
                moon_x_au, moon_y_au = self.get_moon_position(t)
                moon_angle = math.atan2(moon_y_au, moon_x_au)

                moon_dist = planet_config["moon_distance"]
                moon_x = screen_x + moon_dist * math.cos(moon_angle)
                moon_y = screen_y + moon_dist * math.sin(moon_angle)

                moon_config = {
                    "size": planet_config["moon_size"],
                    "color": planet_config["moon_color"],
                }
                self.draw_planet(ctx, moon_x, moon_y, moon_config)

        # 保存图像
        surface.write_to_png(output_path)
        print(f"太阳系壁纸已生成: {output_path}")
        print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")


def main():
    """主函数"""
    renderer = SolarSystemRenderer()
    renderer.render()


if __name__ == "__main__":
    main()
