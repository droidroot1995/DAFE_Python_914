import numpy as np
from scipy.signal import convolve2d


class Board:

    def __init__(self, n, m, cyclic=True):

        self.board = np.zeros((n, m), 'uint8')
        self.counters = np.zeros((n, m), 'uint8')
        self.cyclic = cyclic
        self.n = n
        self.m = m

    def change(self, i, j):

        self.board[i, j] ^= 1

        if self.cyclic:
            X, Y = np.meshgrid([(i - 1) % self.n, i, (i + 1) % self.n], [(j - 1) % self.m, j, (j + 1) % self.m])
            self.counters[X, Y] += (self.board[i, j] * 2 - 1).astype('uint8')
        else:
            self.counters[min(0, i - 1): max(i + 1, self.n - 1), min(0, j - 1): max(j + 1, self.m - 1)] += (self.board[i, j] * 2 - 1)

        self.counters[i, j] -= (self.board[i, j] * 2 - 1).astype('int8')

    def show(self):
        print(self.board)
        print()
        print(self.counters)
        print()

    def update_board(self):

        new_board = np.zeros((self.n, self.m), 'uint8')

        mask1 = (self.board == 0)
        mask2 = (self.board != 0)

        new_board[mask1] = (self.counters[mask1] == 3)
        new_board[mask2] = ((self.counters[mask2] == 3) | (self.counters[mask2] == 2))

        self.board = new_board

    def update_counters(self):

        temp_board = np.pad(self.board, [1, 1], 'wrap' if self.cyclic else 'constant')
        kernel = np.ones((3, 3), 'uint8')
        kernel[1, 1] = 0
        self.counters = convolve2d(temp_board, kernel, mode='valid')

    def step(self):

        check = self.board.copy()

        if not np.any(self.board):
            return False

        self.update_board()

        if np.all(np.equal(check, self.board)):
            return False

        self.update_counters()

        return True

    def clear(self):

        self.board *= 0
        self.counters *= 0
