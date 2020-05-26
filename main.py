import cv2 as cv
import cairo
import numpy as np
import matplotlib.pyplot as plt

def draw_pic():
    image_width = 50

    data = np.zeros((image_width,image_width,4), dtype=np.uint8)
    surface = cairo.ImageSurface.create_for_data(data, cairo.FORMAT_ARGB32, image_width, image_width)
    cr = cairo.Context(surface)

    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.paint()

    cr.arc(image_width/2, image_width/2, image_width/4, 0,2*np.pi)
    cr.set_source_rgb(0.0, 0.0, 1.0)
    cr.fill()

    surface.write_to_png("example.png")
    print(data)
    plt.imshow(data)
    plt.show()


def gen_a_video():
    output_format = cv.VideoWriter_fourcc('m', 'p', '4', 'v')
    output = cv.VideoWriter('output.mp4', output_format, 256, (256, 256))

    for i in range(256):
        data = np.zeros((256, 256, 3), dtype=np.uint8)
        data[:i, :, :] = 255
        output.write(data)


if __name__ == "__main__":
    draw_pic()
