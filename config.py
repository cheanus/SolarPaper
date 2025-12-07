"""
太阳系配置文件
定义行星参数、颜色、大小等
"""

# 图像尺寸配置
IMAGE_WIDTH = 3840  # 4K分辨率宽度
IMAGE_HEIGHT = 2160  # 4K分辨率高度
BACKGROUND_COLOR = (0.1, 0.1, 0.12)  # 深色背景

# 太阳系中心位置
CENTER_X = IMAGE_WIDTH // 2
CENTER_Y = IMAGE_HEIGHT // 2

# 行星配置 (name, color_rgb, relative_size, orbit_radius_au)
# relative_size 是视觉显示大小，orbit_radius_au 是实际轨道半径（天文单位）
PLANETS = {
    "sun": {
        "name": "太阳",
        "color": (1.0, 0.9, 0.3),  # 金黄色
        "size": 35,  # 显示半径
        "glow": True,
        "glow_radius": 60,
    },
    "mercury": {
        "name": "水星",
        "color": (0.7, 0.7, 0.7),  # 灰色
        "size": 4,
        "orbit_radius": 100,  # 像素，视觉轨道半径
        "orbit_color": (0.3, 0.3, 0.35),
        "real_orbit_au": 0.39,  # 实际轨道半径（天文单位）
    },
    "venus": {
        "name": "金星",
        "color": (0.9, 0.8, 0.5),  # 淡黄色
        "size": 8,
        "orbit_radius": 150,
        "orbit_color": (0.3, 0.3, 0.35),
        "real_orbit_au": 0.72,
    },
    "earth": {
        "name": "地球",
        "color": (0.3, 0.5, 0.9),  # 蓝色
        "size": 9,
        "orbit_radius": 210,
        "orbit_color": (0.3, 0.35, 0.4),
        "real_orbit_au": 1.0,
        "has_moon": True,
        "moon_distance": 20,
        "moon_size": 3,
        "moon_color": (0.8, 0.8, 0.8),
    },
    "mars": {
        "name": "火星",
        "color": (0.9, 0.4, 0.3),  # 红色
        "size": 6,
        "orbit_radius": 280,
        "orbit_color": (0.3, 0.3, 0.35),
        "real_orbit_au": 1.52,
    },
    "jupiter": {
        "name": "木星",
        "color": (0.8, 0.7, 0.6),  # 浅褐色
        "size": 22,
        "orbit_radius": 450,
        "orbit_color": (0.3, 0.3, 0.35),
        "real_orbit_au": 5.2,
        "bands": True,  # 标记有条纹
    },
    "saturn": {
        "name": "土星",
        "color": (0.9, 0.8, 0.6),  # 浅黄色
        "size": 19,
        "orbit_radius": 600,
        "orbit_color": (0.3, 0.3, 0.35),
        "real_orbit_au": 9.54,
        "has_ring": True,
        "ring_inner": 24,
        "ring_outer": 38,
        "ring_color": (0.7, 0.6, 0.5, 0.6),
    },
    "uranus": {
        "name": "天王星",
        "color": (0.5, 0.8, 0.9),  # 青色
        "size": 13,
        "orbit_radius": 750,
        "orbit_color": (0.3, 0.3, 0.35),
        "real_orbit_au": 19.19,
    },
    "neptune": {
        "name": "海王星",
        "color": (0.3, 0.4, 0.9),  # 深蓝色
        "size": 12,
        "orbit_radius": 850,
        "orbit_color": (0.3, 0.3, 0.35),
        "real_orbit_au": 30.07,
    },
}

# 轨道样式
ORBIT_LINE_WIDTH = 1.5
ORBIT_DASHED = True  # 使用虚线
ORBIT_DASH_PATTERN = [5, 10]

# 是否显示标签
SHOW_LABELS = False
LABEL_COLOR = (0.7, 0.7, 0.7)
LABEL_FONT_SIZE = 12

# 添加装饰性的小天体（小行星、卫星）
SHOW_DECORATIVE_BODIES = True
DECORATIVE_BODY_COUNT = 30  # 装饰性小天体数量
DECORATIVE_BODY_SIZE_RANGE = (1, 2)
DECORATIVE_BODY_COLOR = (0.5, 0.5, 0.55, 0.6)
