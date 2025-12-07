#!/usr/bin/env python3
"""
太阳系实时壁纸生成器 - 主程序
"""

import argparse
from datetime import datetime
from solar_system import SolarSystemRenderer


def main():
    parser = argparse.ArgumentParser(description="生成太阳系实时壁纸")
    parser.add_argument(
        "-o",
        "--output",
        default="solar_system.png",
        help="输出文件路径 (默认: solar_system.png)",
    )
    parser.add_argument(
        "-t",
        "--time",
        help="指定时间 (格式: YYYY-MM-DD HH:MM:SS)，不指定则使用当前时间",
    )
    parser.add_argument("-W", "--width", type=int, help="图像宽度 (默认: 3840)")
    parser.add_argument("-H", "--height", type=int, help="图像高度 (默认: 2160)")

    args = parser.parse_args()

    # 解析时间
    time = None
    if args.time:
        try:
            time = datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            print(f"错误: 时间格式不正确，请使用 'YYYY-MM-DD HH:MM:SS' 格式")
            return

    # 如果指定了尺寸，修改配置
    if args.width or args.height:
        import config

        if args.width:
            config.IMAGE_WIDTH = args.width
            config.CENTER_X = args.width // 2
        if args.height:
            config.IMAGE_HEIGHT = args.height
            config.CENTER_Y = args.height // 2

    # 生成壁纸
    try:
        renderer = SolarSystemRenderer()
        renderer.render(output_path=args.output, time=time)
        print(f"\n✓ 壁纸生成成功！")
        print(f"  文件: {args.output}")
    except Exception as e:
        print(f"错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
