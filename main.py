import numpy as np
from core.canvas import canvas
from core.action import obj2obj
from core.aniobject import aniobject
from core.aniobject import circle
from core.aniobject import rectangle

def animate_demo():
    width, height = 2000, 1600
    canv = canvas(width, height, 10, 'output.mp4')
    canv.set_bg_color(0, 0, 0)
    c = circle(-3, 0, 3, fill_color = (1, 0, 0, 0.5))
    r = rectangle(2, 1, 3, -1, fill_color = (0, 0, 1, 0.5))
    obj2obj(canv, r, c, 2)
    canv.save()


if __name__ == "__main__":
    animate_demo()
