import numpy as np
from config.constants import VIDEO_FRAME_RATE
from core.aniobject import aniobject


def transform_style(frames, style):
    # 移动风格
    x = np.linspace(0, 1, frames)
    if style == 'linear':
        y = (x * frames).astype(int)
    elif style == 'square':
        y = ((x ** 2) * frames).astype(int) # 变换曲线，必须是起点为0终点为frames的曲线
    elif style == 'cos':
        y = ((-0.5 * np.cos(np.pi * x) + 0.5) * frames).astype(int)
    return y


'''
对象到对象的平滑过渡
'''
def obj2obj(canv, src, dst, time, style = 'cos'):
    if src.points != dst.points:
        # 点数不一致，插值
        src.interpolate_obj(dst)

    frames = time * VIDEO_FRAME_RATE
    src_path = src.path
    dst_path = dst.path
    src_color = src.fill_color if src.is_fill else (0, 0, 0, 0)
    dst_color = dst.fill_color if dst.is_fill else (0, 0, 0, 0)

    for i in transform_style(frames, style):
        temp_obj = aniobject((
            src_path[0] + i * (dst_path[0] - src_path[0]) / frames,
            src_path[1] + i * (dst_path[1] - src_path[1]) / frames
        ))
        temp_obj.fill_color = (
            src_color[0] + i * (dst_color[0] - src_color[0]) / frames,
            src_color[1] + i * (dst_color[1] - src_color[1]) / frames,
            src_color[2] + i * (dst_color[2] - src_color[2]) / frames,
            src_color[3] + i * (dst_color[3] - src_color[3]) / frames,
        )
        canv.add_animate_obj(temp_obj)
        canv.update(clear = True)
        canv.del_animate_obj(temp_obj)


def obj2obj_pairs(canv, obj_pairs, style = 'cos'):
    '''
    解决多组对象同时变换的问题
    obj_pairs = (src, dst, time) 或者 (src, dst, time, style)
    '''
    # 分析obj_pairs
    obj_pair_list = []
    max_frame = 0
    for pair in obj_pairs:
        if pair[0].points != pair[1].points:
            pair[0].interpolate_obj(pair[1])

        if len(pair) == 3:
            obj_pair_list.append([
                pair[0], pair[1],
                transform_style(pair[2] * VIDEO_FRAME_RATE, style), 0
            ]) # 最后一个元素表示当前帧数
        elif len(pair) == 4:
            obj_pair_list.append([
                pair[0], pair[1],
                transform_style(pair[2] * VIDEO_FRAME_RATE, pair[3]), 0
            ]) # 最后一个元素表示当前帧数

        if pair[2] * VIDEO_FRAME_RATE > max_frame:
            max_frame = pair[2] * VIDEO_FRAME_RATE

    final_objs = set({})
    for f in range(max_frame):
        temp_objs = set({})
        for pair in obj_pair_list:
            cur_frames = len(pair[2]) # 当前的帧

            if pair[3] == cur_frames:
                canv.add_animate_obj(pair[1])
                final_objs.add(pair[1])
            else:
                src_path = pair[0].path
                dst_path = pair[1].path
                src_color = pair[0].fill_color if pair[0].is_fill else (0, 0, 0, 0)
                dst_color = pair[1].fill_color if pair[1].is_fill else (0, 0, 0, 0)

                cur_i = pair[2][pair[3]]

                temp_obj = aniobject((
                    src_path[0] + cur_i * (dst_path[0] - src_path[0]) / cur_frames,
                    src_path[1] + cur_i * (dst_path[1] - src_path[1]) / cur_frames
                ))
                temp_obj.fill_color = (
                    src_color[0] + cur_i * (dst_color[0] - src_color[0]) / cur_frames,
                    src_color[1] + cur_i * (dst_color[1] - src_color[1]) / cur_frames,
                    src_color[2] + cur_i * (dst_color[2] - src_color[2]) / cur_frames,
                    src_color[3] + cur_i * (dst_color[3] - src_color[3]) / cur_frames,
                )
                canv.add_animate_obj(temp_obj)
                temp_objs.add(temp_obj)
                pair[3] += 1

        canv.update(clear = True)
        for obj in temp_objs:
            canv.del_animate_obj(obj)

    for obj in final_objs:
        canv.del_animate_obj(obj)


'''
静止
'''
def hold(canv, src, time):
    if src not in canv.animate_objs:
        canv.add_animate_obj(src)

    for i in range(time * VIDEO_FRAME_RATE):
        canv.update(clear = True)
