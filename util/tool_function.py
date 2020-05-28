'''
工具函数
'''

def color_transform(color):
    # 颜色转换: #xxxxxxxx -> (red, green, blue, alpha)
    color = color[1:]

    if len(color) == 6:
        red = int(color[:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:], 16)
        alpha = 255
    elif len(color) == 8:
        red = int(color[:2], 16)
        green = int(color[2:4], 16)
        blue = int(color[4:6], 16)
        alpha = int(color[6:], 16)

    return (red / 255, green / 255, blue / 255, alpha / 255)
