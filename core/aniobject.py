import numpy as np

class aniobject:
    def __init__(self, x = None, y = None):
        self._x = x
        self._y = y
        if self._x.shape != self._y.shape:
            raise Exception('目标aniobject具有长度不一致的维数')
        self._points = len(self._x)

    def set_path(self, x, y):
        if self._x.shape != self._y.shape:
            raise Exception('目标aniobject具有长度不一致的维数')
        self._x = x
        self._y = y
        self._points = len(self._x)

    def get_path(self):
        return (self._x, self._y)

    @property
    def points(self):
        return self._points

    def draw_path(self, ctx):
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(0.02)
        ctx.new_path()
        for p in zip(self._x, self._y):
            ctx.line_to(p[0], p[1])
        ctx.close_path()
        ctx.stroke()

    def _interpolate(self, points):
        # 插值，将当前的路径点数用线性插值的方法扩增或者缩减到设定的点数
        cur_points = self._points
        target_points = points

        temp_t = np.linspace(0, cur_points, target_points)
        temp_x = np.arange(cur_points)

        self._x = np.interp(temp_t, temp_x, self._x)
        self._y = np.interp(temp_t, temp_x, self._y)

        self._points = target_points

    def interpolate_obj(self, obj):
        self._interpolate(obj.points)

    def set_points(self, points):
        self._interpolate(points)


class circle(aniobject):
    def __init__(self, px, py, rad, points=500):
        x = np.linspace(0, 2 * np.pi, points)
        self._points = points
        self._x = np.real(rad * np.exp(-x * 1j)) + px
        self._y = np.imag(rad * np.exp(-x * 1j)) + py
        self._rad = rad
        self._cx = px
        self._cy = py


class rectangle(aniobject):
    def __init__(self, p1_x, p1_y, p2_x, p2_y, points = 400):
        '''
        左上角是第一个点，右下角是第二个点
        '''
        self._p1_x = p1_x
        self._p1_y = p1_y
        self._p2_x = p2_x
        self._p2_y = p2_y
        self._points = points
        self._x = np.concatenate((
            np.linspace(self._p1_x, self._p2_x, self._points // 4),
            self._p2_x * np.ones(self._points // 4),
            np.linspace(self._p2_x, self._p1_x, self._points // 4),
            self._p1_x * np.ones(self._points // 4),
        ))
        self._y = np.concatenate((
            self._p1_y * np.ones(self._points // 4),
            np.linspace(self._p1_y, self._p2_y, self._points // 4),
            self._p2_y * np.ones(self._points // 4),
            np.linspace(self._p2_y, self._p1_y, self._points // 4),
        ))
