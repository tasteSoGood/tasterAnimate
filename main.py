import numpy as np
from core.canvas import canvas
import core.action as ca
from core.aniobject import *


def demo1():
    width, height = 2000, 1600
    canv = canvas(width, height, 10, 'output.mp4')
    canv.set_bg_color(0, 0, 0)
    c = circle(-3, 0, 3, fill_color = (0, 1, 0, 0.5))
    sub_c = circle(-3, 0, 2, fill_color = (1, 0, 0, 0.5))
    r = rectangle(2, 1, 3, -1, fill_color = (0, 0, 1, 0.5))
    ca.obj2obj_pairs(canv, [
        (c, r, 2),
        (sub_c, r, 3),
    ])
    ca.obj2obj_pairs(canv, [
        (r, c, 2),
        (r, sub_c, 1),
    ])
    canv.save()


def demo2():
    width, height = 2000, 1600
    canv = canvas(width, height, 10, 'output.mp4')
    canv.set_bg_color(0, 0, 0)
    c = circle(0, 0, 5)
    ca.hold(canv, c, times = 3)
    canv.save()

def demo3():
    width, height = 2000, 1600
    canv = canvas(width, height, 200, 'output.mp4')
    canv.set_bg_color(0, 0, 0)

    polygons = [polygon(0, 0, i, i + 2, path_width = 0.2) for i in range(1, 100)]

    for p in polygons:
        ca.hold(canv, p, time = 0.1)
        canv.add_bg_obj(p)
    canv.save()

def demo4():
    width, height = 2000, 1600
    canv = canvas(width, height, 10, 'output.mp4')
    canv.set_bg_color(0, 0, 0)

    d = circle(0, 0, 1, dashed = True)

    for i in range(180):
        ca.hold(canv, d, time = 0.05)
        d.rad = d.rad + 0.01

    canv.save()

def demo5():
    width, height = 3000, 1600
    canv = canvas(width, height, 10, 'output.mp4')
    canv.set_bg_color(0, 0, 0)

    c1 = circle(0, 0, 2, fill_color = (255 / 225.0, 130 / 225.0, 203 / 225.0, 0.8))
    c2 = circle(0, 0, 3)
    ca.show_creation(canv, c1, c2)
    ca.fade_out(canv, c1, c2)
    ca.fade_in(canv, c1, c2)

    r = rectangle(3, 1, 4, -1, fill_color = (255 / 225.0, 130 / 225.0, 203 / 225.0, 0.8))
    ca.obj2obj_pairs(canv, (c1, r, 1), (c2, r, 2))

    canv.save()

def demo6():
    width, height = 3000, 1600
    canv = canvas(width, height, 20, 'output.mp4')
    # canv.add_function(lambda pos: (pos[0] / (pos[0] ** 2 + pos[1] ** 2), pos[1] / (pos[0] ** 2 + pos[1] ** 2))) # 复平面变换 z -> 1/z
    canv.add_function(lambda pos: (pos[0] * np.cos(pos[1]), pos[0] * np.sin(pos[1]))) # 平面坐标转极坐标
    canv.set_bg_color(0, 0, 0)
    x = np.linspace(-3 * np.pi, 3 * np.pi, 2000)
    obj2 = aniobject((x, -3 * np.sin(2 * x)))
    ca.show_creation(canv, obj2, time = 3)
    for i in np.linspace(-3, 3, 90):
        obj2.path = (x, i * np.sin(2 * x))
        ca.hold(canv, obj2, time = 0.01)

    ca.fade_out(canv, obj2, time = 2)
    canv.save()

if __name__ == "__main__":
    demo6()
