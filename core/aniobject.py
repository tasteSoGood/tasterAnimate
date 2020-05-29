import numpy as np


class aniobject(object):
    '''
    animate object:

    所有的动画对象都继承自此类，在此类中需要实现：

    1. 规定一个可绘制物体的
      1. 路径数据
      2. 路径的宽度
      3. 路径的颜色
      4. 填充的颜色
    '''
    def __init__(self, path, path_color=(1, 1, 1, 1), fill_color=None):
        self._path = path

        if self._path[0].shape != self._path[1].shape:
            raise Exception("目标aniobject具有长度不一致的维数")

        self._points = len(self._path[0])

        # 颜色
        self._path_color = path_color  # 路径色
        if not fill_color:
            self._fill = False
            self._fill_color = None
        else:
            self._fill = True
            self._fill_color = fill_color  # 填充色

    """
    路径数据的获取和重置
    """

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, nums):
        self._interpolate(nums)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: tuple):
        if path[0].shape != path[1].shape:
            raise Exception("接收到的x和y具有不一致的长度")
        self._path = path
        self._points = len(path[0])

    def interpolate_obj(self, obj):
        self._interpolate(obj.points)

    """
    颜色的获取和重置
    """

    @property
    def path_color(self):
        return self._path_color

    @path_color.setter
    def path_color(self, color: tuple):
        if len(color) == 3:
            self._path_color = (*color, 1.0)
        elif len(color) == 4:
            self._path_color = color

    @property
    def fill_color(self):
        return self._fill_color

    @fill_color.setter
    def fill_color(self, color: tuple):
        if len(color) == 3:
            self._fill_color = (*color, 1.0)
        elif len(color) == 4:
            self._fill_color = color

        self._fill = True

    @property
    def is_fill(self):
        return self._fill

    """
    绘制
    """

    def draw(self, ctx):
        ctx.set_source_rgba(*self._path_color)
        ctx.set_line_width(0.02)
        ctx.new_path()
        for p in zip(self._path[0], self._path[1]):
            ctx.line_to(p[0], p[1])
        ctx.close_path()
        ctx.stroke_preserve()
        if self._fill:
            ctx.set_source_rgba(*self._fill_color)
            ctx.fill()

    """
    工具函数
    """

    def _interpolate(self, points):
        # 插值，将当前的路径点数用线性插值的方法扩增或者缩减到设定的点数
        cur_points = self._points
        target_points = points

        temp_t = np.linspace(0, cur_points, target_points)
        temp_x = np.arange(cur_points)

        self._path = (
            np.interp(temp_t, temp_x, self._path[0]),
            np.interp(temp_t, temp_x, self._path[1])
        )

        self._points = target_points


"""
正圆
"""


class circle(aniobject):
    def __init__(self, px, py, rad, points=500, **kwargs):
        x = np.linspace(0, 2 * np.pi, points)
        self._points = points
        self._path = (
            np.real(rad * np.exp(-x * 1j)) + px,
            np.imag(rad * np.exp(-x * 1j)) + py
        )
        self._rad = rad
        self._cx = px
        self._cy = py
        super(circle, self).__init__(self._path, **kwargs)


"""
矩形
"""


class rectangle(aniobject):
    def __init__(self, p1_x, p1_y, p2_x, p2_y, points=500, **kwargs):
        """
        左上角是第一个点，右下角是第二个点
        """
        self._p1_x = p1_x
        self._p1_y = p1_y
        self._p2_x = p2_x
        self._p2_y = p2_y
        self._points = points
        self._path = (
            np.concatenate(
                (
                    np.linspace(self._p1_x, self._p2_x, self._points // 4),
                    self._p2_x * np.ones(self._points // 4),
                    np.linspace(self._p2_x, self._p1_x, self._points // 4),
                    self._p1_x * np.ones(self._points // 4),
                )
            ),
            np.concatenate(
                (
                    self._p1_y * np.ones(self._points // 4),
                    np.linspace(self._p1_y, self._p2_y, self._points // 4),
                    self._p2_y * np.ones(self._points // 4),
                    np.linspace(self._p2_y, self._p1_y, self._points // 4),
                )
            )
        )
        super(rectangle, self).__init__(self._path, **kwargs)


"""
坐标系
"""


class axis(aniobject):
    def __init__(self, p1_x, p1_y, p2_x, p2_y, gap_x=1, gap_y=1):
        pass
