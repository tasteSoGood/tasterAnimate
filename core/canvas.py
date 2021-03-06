import numpy as np
from core.animate import animate
from core.aniobject import aniobject
import cairo
from config.constants import VIDEO_FRAME_RATE
from core.coordinate import coordinate


class canvas(object):
    """
    画布

    v1.0: 把canvas作为一个平面直角坐标系，固定坐标原点就是图像中心点
    """

    def __init__(self, frame_width, frame_height, scale, video_name="untitled.mp4"):
        self._frame_width = frame_width
        self._frame_height = frame_height
        self._scale = scale
        self._animate = animate(self._frame_width, self._frame_height, video_name)
        self._frame_array = np.zeros((self._frame_height, self._frame_width, 4), dtype=np.uint8)

        self._animate.open_writing_pipeline()
        self._bg_color = None
        self._cairo_context = self._gen_cairo_context()
        self._animate_objs = {}
        self._bg_objs = {}
        self._xlims = (-(self._frame_width / self._frame_height * self._scale) / 2, (self._frame_width / self._frame_height * self._scale) / 2)
        self._ylims = (-self._scale / 2, self._scale / 2)
        self._coordinate = coordinate(self._xlims, self._ylims)

        # 为画布加入一个坐标变换
        self._func = lambda pos: pos

    def add_function(self, func):
        self._func = func

    @property
    def xlims(self):
        return self._xlims

    @property
    def ylims(self):
        return self._ylims

    def _gen_cairo_context(self):
        # 利用cairo产生画布
        surface = cairo.ImageSurface.create_for_data(
            self._frame_array, cairo.FORMAT_ARGB32, self._frame_width, self._frame_height
        )
        ctx = cairo.Context(surface)
        ctx.scale(self._frame_width, self._frame_height)
        ctx.transform(
            cairo.Matrix(
                self._frame_height / self._frame_width * (1.0 / self._scale),
                0,
                0,
                -1.0 / self._scale,
                0.5,
                0.5,
            )
        )
        return ctx

    def set_bg_color(self, red, green, blue, alpha=1.0):
        # 设置并绘制背景
        self._cairo_context.set_source_rgba(red, green, blue, alpha)
        self._cairo_context.paint()
        self._bg_color = (red, green, blue, alpha)

    def update(self, clear=False):
        # 写入帧
        self._coordinate.draw(self)

        for obj in self._bg_objs.values():
            obj.draw(self)

        for obj in self._animate_objs.values():
            obj.draw(self)

        self._animate.write_frame(self._frame_array)

        if self._bg_color and clear:
            # 清理画布背景
            self._cairo_context.set_source_rgba(*self._bg_color)
            self._cairo_context.paint()

    def draw_path(self, path_array, path_color, path_width, fill_color, dashed):
        '''
        直接接触cairo.Context的方法
        path_array.shape = (2, n)
        '''
        path_array = np.array(path_array).T # 转成 (n, 2)
        ctx = self._cairo_context
        ctx.set_source_rgba(*path_color)
        ctx.set_line_width(path_width)
        if dashed:
            ctx.set_dash([0.1, 0.1, 0.1, 0.1])
        ctx.new_path()
        for p in path_array:
            ctx.line_to(*self._func(p))
        ctx.stroke_preserve()
        ctx.close_path()
        ctx.set_source_rgba(*fill_color)
        ctx.fill()
        if dashed:
            ctx.set_dash([1, 0])

    def add_animate_obj(self, obj):
        self._animate_objs[id(obj)] = obj  # 方便今后索引

    def del_animate_obj(self, obj):
        del self._animate_objs[id(obj)]

    def add_bg_obj(self, obj):
        self._bg_objs[id(obj)] = obj  # 方便今后索引

    def del_bg_obj(self, obj):
        del self._bg_objs[id(obj)]

    def save(self):
        self._animate.close_writing_pipeline()

    @property
    def frame_width(self):
        return self._frame_width

    @property
    def frame_height(self):
        return self._frame_height

    @property
    def animate_objs(self):
        return self._animate_objs

    @property
    def bg_objs(self):
        return self._bg_objs

    @property
    def context(self):
        return self._cairo_context

    @property
    def frame_array(self):
        # 返回原始帧数据的作用是让用户有直接操纵它的自由
        return self._frame_array

    @frame_array.setter
    def frame_array(self, array):
        self._frame_array = frame_array
