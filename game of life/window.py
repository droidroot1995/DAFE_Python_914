import numpy as np

class Board:

    def __init__(self, width, height):
        self.board = np.zeros((width, height), 'uint8')
        self.counters = np.zeros((width, height), 'uint8')
        self.width = width
        self.height = height

    def change(self, i, j):
        self.board[i, j] = (self.board[i, j] == 0)

    def update_board(self):
        mask1 = (self.board == 0)
        mask2 = (self.board != 0)

        self.board = np.zeros((self.width, self.height), 'uint8')

        self.board[mask1] = (self.counters[mask1] == 3)
        self.board[mask2] = ((self.counters[mask2] == 3) | (self.counters[mask2] == 2))

    def update_counters(self):
        self.counters = self.conv_fast(self.board)

    def step(self):
        check = self.board.copy()

        if not np.any(self.board):
            return False

        self.update_counters()
        self.update_board()

        if np.all(np.equal(check, self.board)):
            return False

        self.update_counters()

        return True

    def clear(self):
        self.board = np.zeros((self.width, self.height), 'uint8')
        self.counters = np.zeros((self.width, self.height), 'uint8')

    def zero_pad(self, image, pad_height = 2, pad_width = 2):
        H, W = image.shape
        out = np.zeros((H + 2 * pad_height, W + 2 * pad_width))
        out[pad_height:H + pad_height, pad_width:W + pad_width] = image

        return out

    def conv_fast(self, image):
        kernel = np.ones((3, 3))
        kernel[1, 1] = 0
        Hi, Wi = image.shape
        Hk, Wk = kernel.shape
        Hi += 2
        Wi += 2
        out = np.zeros((Hi, Wi))

        image = self.zero_pad(image)

        for height in range(Hi):
            for width in range(Wi):
                out[height][width] = np.sum(image[height:height + Hk, width:width + Wk] * kernel)

        out[1, :] += out[-1, :]
        out[-2, :] += out[0, :]
        out[:, 1] += out[:, -1]
        out[:, -2] += out[:, 0]
        return out[1: -1, 1: -1]