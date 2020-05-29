import numpy as np
from constants import FFMPEG_BIN
from core.animate import animate
from core.canvas import canvas


class game_of_life:
    """
    康威生命游戏
    """

    def __init__(self, width, height):
        self._row = height
        self._col = width
        self._board = np.zeros((self._row, self._col), dtype=np.uint8)

    def random_init(self, seed_nums):
        x = np.random.randint(0, self._row, seed_nums)
        y = np.random.randint(0, self._col, seed_nums)
        for i in zip(x, y):
            self._board[i[0], i[1]] = 1

    def user_init(self, board):
        self._board = board

    def _count_live(self, i, j):
        board = self._board
        return (
            board[i - 1, j - 1]
            + board[i - 1, j]
            + board[i - 1, j + 1]
            + board[i, j - 1]
            + board[i, j + 1]
            + board[i + 1, j - 1]
            + board[i + 1, j]
            + board[i + 1, j + 1]
        )

    def update(self):
        temp_board = self._board.copy()

        for i in range(1, self._row - 1):
            for j in range(1, self._col - 1):
                live = self._count_live(i, j)
                if self._board[i, j] == 0 and live == 3:
                    temp_board[i, j] = 1
                elif self._board[i, j] == 1 and live > 3:
                    temp_board[i, j] = 0
                elif self._board[i, j] == 1 and live < 2:
                    temp_board[i, j] = 0

        self._board = temp_board

    def get_board(self):
        return self._board


def update_from_board(board, row_scale, col_scale):
    res = board.copy() * 255
    res = np.repeat(res, row_scale, axis=0)
    res = np.repeat(res, col_scale, axis=1)
    res = res.reshape((*res.shape, 1))
    return np.concatenate((res, res, res, res), axis=-1)


def pattern(board, i, j):
    for p in zip([i, i + 1, i + 2, i + 2, i + 2], [j + 1, j + 2, j, j + 1, j + 2]):
        board[p[0], p[1]] = 1


def main():
    width, height, scale = 128, 128, 16
    canv = canvas(width * scale, height * scale, 1, "output.mp4")
    game = game_of_life(width, height)

    board = game.get_board()

    for i in range(20):
        for j in range(20):
            pattern(board, 1 + 5 * i, 1 + 5 * j)

    game.user_init(board)

    for time in range(300):
        game.update()
        canv.frame_array = update_from_board(game.get_board(), scale, scale)
        canv.update()

        if time % 10 == 0:
            print("正在写入第%d帧......" % time)

    canv.save()
