import numpy as np
from constants import VIDEO_FRAME_RATE
from core.aniobject import aniobject

'''
aniobject的变换
'''
def obj2obj(canv, src, dst, time, style = 'cos'):
    if src.points != dst.points:
        # 点数不一致，插值
        src.interpolate_obj(dst)

    frames = time * VIDEO_FRAME_RATE
    x = np.linspace(0, 1, frames)
    if style == 'linear':
        y = (x * frames).astype(int)
    elif style == 'square':
        y = ((x ** 2) * frames).astype(int) # 变换曲线，必须是起点为0终点为frames的曲线
    elif style == 'cos':
        y = ((-0.5 * np.cos(np.pi * x) + 0.5) * frames).astype(int)

    src_path = src.get_path()
    dst_path = dst.get_path()

    for i in y:
        temp_obj = aniobject(src_path[0] + i * (dst_path[0] - src_path[0]) / frames, src_path[1] + i * (dst_path[1] - src_path[1]) / frames)
        canv.add_animate_obj(temp_obj)
        canv.update(clear = True)
        canv.del_animate_obj(temp_obj)
