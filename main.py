import numpy as np
from core.canvas import canvas
import core.action as ca
from core.aniobject import aniobject
from core.aniobject import circle
from core.aniobject import rectangle


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
    ca.hold(canv, c, 3)
    canv.save()


if __name__ == "__main__":
    demo1()
