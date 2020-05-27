import numpy as np
from constants import FFMPEG_BIN
from core.animate import animate

def chessboard2frame(chessboard, width, height, width_scale, height_scale):
    frame = np.zeros((width * width_scale, height * height_scale, 4), dtype = np.uint8)

    for i in range(width):
        for j in range(height):
            if chessboard[i, j]:
                frame[i * width_scale : (i + 1) * width_scale, j * height_scale : (j + 1) * height_scale, :] = 255

    return frame

def main():
    width, height = 72, 128
    anim = animate(height*32, width*32, "output.mp4")
    anim.open_writing_pipeline()

    frame = np.zeros((width, height), dtype = int)

    seed = 20000

    for i in zip(np.random.randint(0, width, seed), np.random.randint(0, height, seed)):
        frame[i[0], i[1]] = 1

    anim.write_frame(chessboard2frame(frame, width, height, 32, 32))

    """
    康威生命游戏

    x[i-1, j-1] x[i-1, j] x[i-1, j+1]
    x[i, j-1] x[i, j] x[i, j+1]
    x[i+1, j-1] x[i+1, j] x[i+1, j+1]
    """

    count_live = lambda i, j: (frame[i - 1, j - 1] + frame[i - 1, j] + frame[i - 1, j + 1] + frame[i, j - 1] + frame[i, j + 1] + frame[i + 1, j - 1] + frame[i + 1, j] + frame[i + 1, j + 1])

    for time in range(20):
        temp_frame = frame.copy()
        for i in range(1, width - 1):
            for j in range(1, height - 1):
                live = count_live(i, j)
                if frame[i, j] == 0 and live == 3:
                    temp_frame[i, j] = 1
                elif frame[i, j] == 1 and live > 3:
                    temp_frame[i, j] = 0
                elif frame[i, j] == 1 and live < 2:
                    temp_frame[i, j] = 0

        if time % 10 == 0:
            print('正在写入第%d帧......' % time)

        frame = temp_frame
        anim.write_frame(chessboard2frame(frame, width, height, 32, 32))

    anim.close_writing_pipeline()
