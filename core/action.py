import numpy as np
from config.constants import VIDEO_FRAME_RATE
from core.aniobject import aniobject


def transform_style(start, end, frames, style):
    # 移动风格
    frames = int(frames)
    x = np.linspace(0, 1, frames)
    if style == 'linear':
        y = x * (end - start) + start
    elif style == 'square':
        y = (x ** 2) * (end - start) + start # 变换曲线，必须是起点为0终点为frames的曲线
    elif style == 'cos':
        y = (-0.5 * np.cos(np.pi * x) + 0.5) * (end - start) + start
    return y


'''
对象到对象的平滑过渡
'''
def obj2obj(canv, src, dst, time, style = 'cos'):
    # 点数不一致，插值
    if src.points < dst.points:
        src.interpolate_obj(dst)
    elif src.points > dst.points:
        dst.interpolate_obj(src)

    frames = time * VIDEO_FRAME_RATE
    if frames < 1:
        frames = 1

    src_path = src.path
    dst_path = dst.path
    src_color = src.fill_color
    dst_color = dst.fill_color

    for i in transform_style(0, frames, frames, style):
        temp_obj = src.copy()
        temp_obj.path = (
            src_path[0] + i * (dst_path[0] - src_path[0]) / frames,
            src_path[1] + i * (dst_path[1] - src_path[1]) / frames
        )
        temp_obj.fill_color = (
            src_color[0] + i * (dst_color[0] - src_color[0]) / frames,
            src_color[1] + i * (dst_color[1] - src_color[1]) / frames,
            src_color[2] + i * (dst_color[2] - src_color[2]) / frames,
            src_color[3] + i * (dst_color[3] - src_color[3]) / frames,
        )
        canv.add_animate_obj(temp_obj)
        canv.update(clear = True)
        canv.del_animate_obj(temp_obj)


def obj2obj_pairs(canv, *obj_pairs, style = 'cos'):
    '''
    解决多组对象同时变换的问题
    obj_pairs = (src, dst, time) 或者 (src, dst, time, style)
    '''
    # 分析obj_pairs
    obj_pair_list = []
    max_frame = 0
    for pair in obj_pairs:
        # 点数不一致，插值
        if pair[0].points < pair[1].points:
            pair[0].interpolate_obj(pair[1])
        elif pair[0].points > pair[1].points:
            pair[1].interpolate_obj(pair[0])

        frames = pair[2] * VIDEO_FRAME_RATE
        if frames < 1:
            frames = 1

        if len(pair) == 3:
            obj_pair_list.append([
                pair[0], pair[1],
                transform_style(0, frames, pair[2] * VIDEO_FRAME_RATE, style), 0
            ]) # 最后一个元素表示当前帧数
        elif len(pair) == 4:
            obj_pair_list.append([
                pair[0], pair[1],
                transform_style(0, frames, pair[2] * VIDEO_FRAME_RATE, pair[3]), 0
            ]) # 最后一个元素表示当前帧数

        if frames > max_frame:
            max_frame = frames

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
                src_color = pair[0].fill_color
                dst_color = pair[1].fill_color

                cur_i = pair[2][pair[3]]

                temp_obj = pair[0].copy()
                temp_obj.path = (
                    src_path[0] + cur_i * (dst_path[0] - src_path[0]) / cur_frames,
                    src_path[1] + cur_i * (dst_path[1] - src_path[1]) / cur_frames
                )
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
def hold(canv, *objs, time = 1.0):
    for src in objs:
        if src not in canv.animate_objs:
            canv.add_animate_obj(src)

    frames = int(time * VIDEO_FRAME_RATE)
    if frames < 1:
        frames = 1

    for i in range(frames):
        canv.update(clear = True)

    for src in objs:
        canv.del_animate_obj(src)


'''
旋转
'''
def rotate_matrix(deg):
    '''
    deg: 角度，不是弧度
    '''
    deg = deg * np.pi / 180
    return np.array([[np.cos(deg), -np.sin(deg)], [np.sin(deg), np.cos(deg)]])


def rotate(canv, *objs, deg = 90, time = 1.0, style = 'cos'):
    for src in objs:
        if src not in canv.animate_objs:
            canv.add_animate_obj(src)

    frames = time * VIDEO_FRAME_RATE
    if frames < 1:
        frames = 1

    origin_path = {}
    for src in objs:
        origin_path[id(src)] = src.path

    for i in transform_style(0, deg, frames, style):
        canv.update(clear = True)
        for obj in objs:
            obj.path = rotate_matrix(i) @ np.array(origin_path[id(obj)])

    for src in objs:
        canv.del_animate_obj(src)

'''
生成
'''
def show_creation(canv, *objs, time = 1.0, style = 'cos'):
    max_points = 0
    for src in objs:
        if src not in canv.animate_objs:
            canv.add_animate_obj(src)

        if src.points > max_points:
            max_points = src.points

    for src in objs:
        src.points = max_points

    frames = time * VIDEO_FRAME_RATE
    if frames < 1:
        frames = 1

    origin_path = {}
    for src in objs:
        origin_path[id(src)] = src.path

    for i in transform_style(0, max_points, frames, style):
        for obj in objs:
            obj.path = np.array(origin_path[id(obj)])[:, :int(i)]
        canv.update(clear = True)

    for src in objs:
        src.path = origin_path[id(src)]
        canv.del_animate_obj(src)

'''
淡入淡出
'''
def fade_in(canv, *objs, time = 1.0, style = 'cos'):
    frames = time * VIDEO_FRAME_RATE
    if frames < 1:
        frames = 1
    path_alpha_style, fill_alpha_style = {}, {}
    origin_path_color, origin_fill_color = {}, {}
    for src in objs:
        origin_path_color[id(src)] = src.path_color
        origin_fill_color[id(src)] = src.fill_color
        path_alpha_style[id(src)] = transform_style(0, src.path_color[-1], frames, style)
        fill_alpha_style[id(src)] = transform_style(0, src.fill_color[-1], frames, style)
        if src not in canv.animate_objs:
            canv.add_animate_obj(src)

    for i in range(int(frames)):
        for obj in objs:
            obj.path_color = (*obj.path_color[:3], path_alpha_style[id(obj)][i])
            obj.fill_color = (*obj.fill_color[:3], fill_alpha_style[id(obj)][i])
        canv.update(clear = True)

    for src in objs:
        src.path_color = origin_path_color[id(src)]
        src.fill_color = origin_fill_color[id(src)]
        canv.del_animate_obj(src)

def fade_out(canv, *objs, time = 1.0, style = 'cos'):
    frames = time * VIDEO_FRAME_RATE
    if frames < 1:
        frames = 1
    path_alpha_style, fill_alpha_style = {}, {}
    origin_path_color, origin_fill_color = {}, {}
    for src in objs:
        origin_path_color[id(src)] = src.path_color
        origin_fill_color[id(src)] = src.fill_color
        path_alpha_style[id(src)] = transform_style(src.path_color[-1], 0, frames, style)
        fill_alpha_style[id(src)] = transform_style(src.fill_color[-1], 0, frames, style)
        if src not in canv.animate_objs:
            canv.add_animate_obj(src)

    for i in range(int(frames)):
        for obj in objs:
            obj.path_color = (*obj.path_color[:3], path_alpha_style[id(obj)][i])
            obj.fill_color = (*obj.fill_color[:3], fill_alpha_style[id(obj)][i])
        canv.update(clear = True)

    for src in objs:
        src.path_color = origin_path_color[id(src)]
        src.fill_color = origin_fill_color[id(src)]
        canv.del_animate_obj(src)
