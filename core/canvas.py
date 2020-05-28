import numpy as np
from core.animate import animate
from core.aniobject import aniobject
import cairo
from config.constants import VIDEO_FRAME_RATE

class canvas:
    '''
    画布

    v1.0: 把canvas作为一个平面直角坐标系，固定坐标原点就是图像中心点
    '''
    def __init__(self, frame_width, frame_height, scale, video_name = 'untitled.mp4'):
        self._frame_width = frame_width
        self._frame_height = frame_height
        self._scale = scale
        self._animate = animate(self._frame_width, self._frame_height, video_name)
        self._frame_array = np.zeros((self._frame_height, self._frame_width, 4), dtype = np.uint8)
        self._animate.open_writing_pipeline()
        self._bg_color = None

        # 利用cairo产生画布
        surface = cairo.ImageSurface.create_for_data(self._frame_array, cairo.FORMAT_ARGB32, self._frame_width, self._frame_height)
        ctx = cairo.Context(surface)
        ctx.scale(self._frame_width, self._frame_height)
        ctx.transform(cairo.Matrix(
            self._frame_height / self._frame_width * (1.0 / self._scale), 0,
            0, -1.0 / self._scale, 0.5, 0.5
        ))
        self._cairo_context = ctx

        self._animate_objs = {}

    def get_cairo_context(self):
        return ctx

    def get_frame_array(self):
        # 返回原始帧数据的作用是让用户有直接操纵它的自由
        return self._frame_array

    def set_frame_array(self, frame_array):
        self._frame_array = frame_array

    def set_bg_color(self, red, green, blue, alpha = 1.0):
        # 设置并绘制背景
        self._cairo_context.set_source_rgba(red, green, blue, alpha)
        self._cairo_context.paint()
        self._bg_color = (red, green, blue, alpha)

    def update(self, clear = False):
        # 写入帧
        for key, obj in self._animate_objs.items():
            obj.draw(self._cairo_context)

        self._animate.write_frame(self._frame_array)

        if self._bg_color and clear:
            # 清理画布背景
            self._cairo_context.set_source_rgba(*self._bg_color)
            self._cairo_context.paint()

    def add_animate_obj(self, obj):
        self._animate_objs[id(obj)] = obj # 方便今后索引

    def del_animate_obj(self, obj):
        del self._animate_objs[id(obj)]

    def save(self):
        self._animate.close_writing_pipeline()

    @property
    def frame_width(self):
        return self._frame_width

    @property
    def frame_height(self):
        return self._frame_height

