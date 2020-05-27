import numpy as np
from core.canvas import canvas

def animate_demo():
    width, height = 2000, 1600
    canv = canvas(width, height, 10, 'output.mp4')
    ctx = canv.get_cairo_context()
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()

    for i in np.linspace(0, 5, 200):
        ctx.set_source_rgb(1, 1, 1)
        ctx.set_line_width(0.02)
        ctx.new_path()
        ctx.arc(0, 0, i, 0, 2 * np.pi)
        ctx.close_path()
        ctx.stroke()
        canv.update()
        ctx.set_source_rgb(0, 0, 0)
        ctx.paint()

    canv.save()


if __name__ == "__main__":
    animate_demo()
