# 太阳系实时壁纸生成器 🌌

根据当前时间生成太阳系的实时位置壁纸。使用 Skyfield 库计算行星的精确位置，使用 Cairo 绘制精美的图像。

![示例](assets/example.png)

## 功能特点

- ✨ **实时位置**: 根据真实天文数据计算行星位置
- 🎨 **精美设计**: 参考提供的示意图风格，深色背景配合柔和光晕
- 🌍 **包含所有行星**: 水星、金星、地球(含月球)、火星、木星、土星、天王星、海王星
- 💍 **特殊效果**: 土星环、太阳光晕、行星高光、小行星带装饰
- 🖼️ **4K 分辨率**: 默认 3840x2160，可自定义
- ⚙️ **灵活配置**: 可调整颜色、大小、轨道等所有参数

## 安装依赖

```bash
# 创建虚拟环境（可选）
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

首次运行时，Skyfield 会自动下载行星星历表数据（约 17MB）。
或者你也可下载[de421.bsp](https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp)到本项目根目录中。

## 使用方法

### 基本使用

生成当前时间的太阳系壁纸：

```bash
python main.py
```

### 指定输出文件

```bash
python main.py -o wallpaper.png
```

### 指定时间

生成特定时间的太阳系状态：

```bash
python main.py -t "2025-12-31 23:59:59"
```

### 自定义分辨率

```bash
python main.py -w 1920 -H 1080
```

### 完整示例

```bash
python main.py -o ~/Pictures/solar_wallpaper.png -t "2025-12-07 12:00:00" -w 2560 -H 1440
```

## 定时更新壁纸

### Linux/macOS (使用 cron)

编辑 crontab：

```bash
crontab -e
```

添加以下行（每小时更新一次）：

```bash
0 * * * * cd /home/test/Codes/solarpaper && python main.py -o ~/Pictures/solar_wallpaper.png
```

然后设置系统壁纸为 `~/Pictures/solar_wallpaper.png`。大多数桌面环境会自动检测文件变化并刷新壁纸。

## 配置说明

所有配置项都在 `config.py` 文件中：

- **IMAGE_WIDTH / IMAGE_HEIGHT**: 图像尺寸
- **BACKGROUND_COLOR**: 背景颜色 (RGB 0-1)
- **PLANETS**: 行星参数字典
  - `color`: 行星颜色
  - `size`: 显示半径（像素）
  - `orbit_radius`: 视觉轨道半径（像素）
  - `real_orbit_au`: 真实轨道半径（天文单位，用于计算位置）

### 调整建议

- **如果行星太小**: 增加 `PLANETS[planet]['size']`
- **如果轨道太密集**: 调整 `orbit_radius` 的比例
- **改变背景**: 修改 `BACKGROUND_COLOR`
- **显示标签**: 设置 `SHOW_LABELS = True`

## 技术原理

1. **位置计算**: 使用 Skyfield 库和 JPL DE421 星历表计算行星在指定时刻的日心坐标
2. **坐标转换**: 将三维空间坐标投影到黄道面，转换为屏幕坐标
3. **视觉优化**: 由于太阳系实际尺度差异巨大，使用配置的视觉半径代替真实比例
4. **图像渲染**: 使用 Cairo 绘制矢量图形，支持渐变、透明度等高级效果

## 项目结构

```
solarpaper/
├── main.py              # 主程序入口
├── solar_system.py      # 核心渲染逻辑
├── config.py            # 配置文件
├── requirements.txt     # 依赖包
├── README.md           # 说明文档
└── assets/             # 资源文件
```

## 致谢

- **skyfield**: 天文计算库，提供高精度行星位置计算
- **pycairo**: Python 的 Cairo 图形库绑定，用于绘制矢量图形
- **星历**：行星位置数据来自 NASA JPL 星历表

---

享受你的太阳系实时壁纸！ 🚀✨
