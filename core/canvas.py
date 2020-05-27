import numpy as np
from core.animate import animate
import cairo

class canvas:
    '''
    画布

    v1.0: 把canvas作为一个平面直角坐标系，固定坐标原点就是图像中心点
    '''
    def __init__(self, frame_width, frame_height, scale, video_name):
        self._frame_width = frame_width
        self._frame_height = frame_height
        self._scale = scale
        self._animate = animate(self._frame_width, self._frame_height, video_name)
        self._frame_array = np.zeros((self._frame_height, self._frame_width, 4), dtype = np.uint8)
        self._animate.open_writing_pipeline()

    def get_cairo_context(self):
        surface = cairo.ImageSurface.create_for_data(self._frame_array, cairo.FORMAT_ARGB32, self._frame_width, self._frame_height)
        ctx = cairo.Context(surface)
        ctx.scale(self._frame_width, self._frame_height)
        ctx.transform(cairo.Matrix(
            self._frame_height / self._frame_width * (1.0 / self._scale), 0,
            0, -1.0 / self._scale, 0.5, 0.5
        ))
        self._cairo_context = ctx
        return ctx

    def get_frame_array(self):
        return self._frame_array

    def set_frame_array(self, frame_array):
        self._frame_array = frame_array

    def update(self):
        self._animate.write_frame(self._frame_array)

    def save(self):
        self._animate.close_writing_pipeline()

    @property
    def frame_width(self):
        return self._frame_width

    @property
    def frame_height(self):
        return self._frame_height
