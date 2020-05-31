import numpy as np
import copy

def affine_transform(array, mat):
    '''
    array.shape = (2, n)
    res.shape = (2, n)
    遵守变换规律，使用左乘
    '''
    array = np.concatenate((
        array, np.ones((1, array.shape[-1]))
    ))
    return (mat @ array)[:2, :]

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
    def __init__(
            self,
            path,
            path_color=(1, 1, 1, 1),
            fill_color=(0, 0, 0, 0),
            path_width=0.02,
            dashed = False
    ):
        self._path = path

        if self._path[0].shape != self._path[1].shape:
            raise Exception("目标aniobject具有长度不一致的维数")

        self._points = len(self._path[0])

        # 颜色
        self._path_color = path_color  # 路径色
        self._fill_color = fill_color  # 填充色

        # 线宽
        self._path_width = path_width

        # 是否画虚线
        self._dashed = dashed

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

    '''
    路径宽度的获取和重置
    '''

    @property
    def path_width(self):
        return self._path_width

    @path_width.setter
    def path_width(self, width):
        self._path_width = width

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

    """
    绘制
    """

    def draw(self, canv):
        canv.draw_path(self._path, self._path_color, self._path_width, self._fill_color, self._dashed)

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

    def copy(self):
        return copy.deepcopy(self)

    '''
    变换: 大概率需要子类重载
    '''
    def apply_matrix(self, mat):
        path = np.array(self._path)

        if mat.shape == (2, 2):
            temp_mat = np.eye(3)
            temp_mat[:2, :2] = mat
            mat = temp_mat

        self._path = affine_transform(path, mat)

"""
正圆
"""


class circle(aniobject):
    def __init__(self, px, py, rad, points=500, **kwargs):
        self._cx = px
        self._cy = py
        self._points = points
        self._rad = rad
        self._gen_path()
        super(circle, self).__init__(self._path, **kwargs)

    @property
    def rad(self):
        return self._rad

    @rad.setter
    def rad(self, value):
        self._rad = value
        self._gen_path()

    @property
    def pos(self):
        return (self._cx, self._cy)

    @pos.setter
    def pos(self, pos):
        self._cx, self._cy = pos
        self._gen_path()

    def apply_matrix(self, mat):
        # 仿射变换
        path = np.array(self._path)
        if mat.shape == (2, 2):
            temp_mat = np.eye(3)
            temp_mat[:2, :2] = mat
            mat = temp_mat

        [self._cx, self._cy] = affine_transform(np.array([[self._cx, self._cy]]).T, mat).T[0]
        self._gen_path()

    '''
    生成路径
    '''

    def _gen_path(self):
        x = np.linspace(0, 2 * np.pi, self._points)
        self._path = np.array((
            np.real(self._rad * np.exp(x * 1j)) + self._cx,
            np.imag(self._rad * np.exp(x * 1j)) + self._cy
        ))


'''
点
'''

class dot(aniobject):
    def __init__(self, px, py, size = 0.06, **kwargs):
        self._points = 100
        self._cx = px
        self._cy = py
        self._size = size
        self._gen_path()
        super(dot, self).__init__(self._path, **kwargs)
        self._fill_color = self._path_color
        self._fill = True

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._gen_path()

    @property
    def pos(self):
        return (self._cx, self._cy)

    @pos.setter
    def pos(self, pos):
        self._cx, self._cy = pos
        self._gen_path()

    def apply_matrix(self, mat):
        # 仿射变换
        if mat.shape == (2, 2):
            temp_mat = np.eye(3)
            temp_mat[:2, :2] = mat
            mat = temp_mat

        [self._cx, self._cy] = affine_transform(np.array([[self._cx, self._cy]]).T, mat).T[0]
        self._gen_path()

    '''
    生成路径
    '''

    def _gen_path(self):
        x = np.linspace(0, 2 * np.pi, self._points)
        self._path = np.array((
            np.real(0.5 * self._size * np.exp(x * 1j)) + self._cx,
            np.imag(0.5 * self._size * np.exp(x * 1j)) + self._cy
        ))

"""
矩形
"""


class rectangle(aniobject):
    def __init__(self, p1_x, p1_y, p2_x, p2_y, points=500, **kwargs):
        """
        左上角是第一个点，右下角是第二个点

        记录的时候需要四个点：
        p1: 左上
        p2: 右上
        p3: 右下
        p4: 左下
        """
        self._p1 = [p1_x, p1_y]
        self._p2 = [p1_x, p2_y]
        self._p3 = [p2_x, p2_y]
        self._p4 = [p2_x, p1_y]
        self._points = points
        self._gen_path()
        super(rectangle, self).__init__(self._path, **kwargs)

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, pos):
        self._p1 = pos
        self._gen_path()

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, pos):
        self._p2 = pos
        self._gen_path()

    @property
    def p3(self):
        return self._p3

    @p3.setter
    def p3(self, pos):
        self._p3 = pos
        self._gen_path()

    @property
    def p4(self):
        return self._p4

    @p4.setter
    def p4(self, pos):
        self._p4 = pos
        self._gen_path()

    def apply_matrix(self, mat):
        # 仿射变换
        if mat.shape == (2, 2):
            temp_mat = np.eye(3)
            temp_mat[:2, :2] = mat
            mat = temp_mat

        self._p1 = affine_transform(np.array([self.p1]).T, mat).T[0]
        self._p2 = affine_transform(np.array([self.p2]).T, mat).T[0]
        self._p3 = affine_transform(np.array([self.p3]).T, mat).T[0]
        self._p4 = affine_transform(np.array([self.p4]).T, mat).T[0]
        self._gen_path()

    def _gen_path(self):
        self._path = np.array((
            np.array([self._p1[0], self._p2[0], self._p3[0], self._p4[0], self._p1[0]]),
            np.array([self._p1[1], self._p2[1], self._p3[1], self._p4[1], self._p1[1]])
        ))


'''
直线
'''


class line(aniobject):
    def __init__(self, p1_x, p1_y, p2_x, p2_y, **kwargs):
        self._p1 = [p1_x, p1_y]
        self._p2 = [p2_x, p2_y]
        self._gen_path()
        super(line, self).__init__(self._path, **kwargs)

    @property
    def p1(self):
        return self._p1

    @p1.setter
    def p1(self, pos):
        self._p1 = pos
        self._gen_path()

    @property
    def p2(self):
        return self._p2

    @p2.setter
    def p2(self, pos):
        self._p2 = pos
        self._gen_path()

    def apply_matrix(self, mat):
        # 仿射变换
        if mat.shape == (2, 2):
            temp_mat = np.eye(3)
            temp_mat[:2, :2] = mat
            mat = temp_mat

        self._p1 = affine_transform(np.array([self.p1]).T, mat).T[0]
        self._p2 = affine_transform(np.array([self.p2]).T, mat).T[0]
        self._gen_path()

    def _gen_path(self):
        self._path = np.array((
            np.array([self._p1[0], self._p2[0]]),
            np.array([self._p1[1], self._p2[1]])
        ))

'''
正多边形
'''

class polygon(aniobject):
    def __init__(self, center_x, center_y, rad, n, **kwargs):
        self._n = n
        self._rad = rad
        self._cx = center_x
        self._cy = center_y
        self._gen_path()
        super(polygon, self).__init__(self._path, **kwargs)

    @property
    def rad(self):
        return self._rad

    @rad.setter
    def rad(self, value):
        self._rad = value
        self._gen_path()

    @property
    def pos(self):
        return (self._cx, self._cy)

    @pos.setter
    def pos(self, x, y):
        self._cx = x
        self._cy = y
        self._gen_path()

    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self._n = value
        self._gen_path()

    def apply_matrix(self, mat):
        # 仿射变换
        path = np.array(self._path)
        if mat.shape == (2, 2):
            temp_mat = np.eye(3)
            temp_mat[:2, :2] = mat
            mat = temp_mat

        [self._cx, self._cy] = affine_transform(np.array([[self._cx, self._cy]]).T, mat).T[0]
        self._gen_path()

    def _gen_path(self):
        x = np.linspace(0, 2 * np.pi, self._n + 1)
        self._path = (
            np.real(self._rad * np.exp(x * 1j)) + self._cx,
            np.imag(self._rad * np.exp(x * 1j)) + self._cy
        )
