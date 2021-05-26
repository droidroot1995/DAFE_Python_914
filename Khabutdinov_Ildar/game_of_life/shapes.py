from libraries import *

class Shapes(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Shapes")

        self.height_button, self.width_button = 100, 100
        self.setFixedSize(self.height_button * 2, self.width_button * 2)

        self.make_buttons()
        self.grid = np.copy(parent.grid)
        self.show()

    def make_buttons(self):
        but_fig1 = QPushButton('Spaceship', self).setGeometry(0,
                                                              0,
                                                              self.width_button,
                                                              self.height_button)

        but_fig2 = QPushButton('Schick', self).setGeometry(self.width_button,
                                                           0,
                                                           self.width_button,
                                                           self.height_button)

        but_fig3 = QPushButton('Popower', self).setGeometry(0,
                                                            self.height_button,
                                                            self.width_button,
                                                            self.height_button)

        but_cancel = QPushButton('Cancel', self).setGeometry(self.width_button,
                                                             self.height_button,
                                                             self.width_button,
                                                             self.height_button)

        but_fig1.clicked.connect(self.set_fig1)
        but_fig2.clicked.connect(self.set_fig2)
        but_fig3.clicked.connect(self.set_fig3)
        but_cancel.clicked.connect(self.cancel)

    def set_fig1(self):
        height, width = (self.parent.size().height() - self.parent.height_button) // self.parent.gridstep,\
                        self.parent.size().width() // self.parent.gridstep

        if height < 5 or width < 7:
            print("Small window")

        fig = np.array([[False, False, True, True, False, False, False],
                        [True, False, False, False, False, True, False],
                        [False, False, False, False, False, False, True],
                        [True, False, False, False, False, False, True],
                        [False, True, True, True, True, True, True]])

        dx, dy = width - 7, (height - 5) // 2

        for j in range(dy):
            for i in range(width):
                self.grid[j, i] = False

        for j in range(dy, height - dy - 1 + height % 2):
            for i in range(width - dx):
                self.grid[j, i] = fig[j - dy, i]
            for i in range(width - dx, width):
                self.grid[j, i] = False

        for j in range(height - dy - 1 + height % 2, height):
            for i in range(width):
                self.grid[j, i] = False

        self.parent.grid = np.copy(self.grid)
        self.hide()

    def set_fig2(self):
        height, width = (self.parent.size().height() - self.parent.height_button) // self.parent.gridstep, \
                        self.parent.size().width() // self.parent.gridstep

        if height < 11 or width < 20:
            print("Small window")

        fig = np.array([[False, True, False, False, True, False, False, False, False, False, False, False, False, False,
                         False, False, False, False, False, False],
                        [True, False, False, False, False, False, False, False, False, False, False, False, False,
                         False, False, False, False, False, False, False],
                        [True, False, False, False, True, False, False, False, False, False, False, False, False,
                         False, False, False, False, False, False, False],
                        [True, True, True, True, False, False, False, False, False, False, False, False, False, True,
                         True, False, False, False, False, False],
                        [False, False, False, False, False, False, True, True, True, False, False, False, False, False,
                         True, True, False, False, False, False],
                        [False, False, False, False, False, False, True, True, False, True, True, False, False, False,
                         False, False, False, True, True, True],
                        [False, False, False, False, False, False, True, True, True, False, False, False, False, False,
                         True, True, False, False, False, False],
                        [True, True, True, True, False, False, False, False, False, False, False, False, False, True,
                         True, False, False, False, False, False],
                        [True, False, False, False, True, False, False, False, False, False, False, False, False, False,
                         False, False, False, False, False, False],
                        [True, False, False, False, False, False, False, False, False, False, False, False, False,
                         False, False, False, False, False, False, False],
                        [False, True, False, False, True, False, False, False, False, False, False, False, False, False,
                         False, False, False, False, False, False]])

        dx, dy = width - 20, (height - 11) // 2

        for j in range(dy):
            for i in range(width):
                self.grid[j, i] = False

        for j in range(dy, height - dy - 1 + height % 2):
            for i in range(dx):
                self.grid[j, i] = False
            for i in range(dx, width):
                self.grid[j, i] = fig[j - dy, i - dx]

        for j in range(height - dy - 1 + height % 2, height):
            for i in range(width):
                self.grid[j, i] = False

        self.parent.grid = np.copy(self.grid)
        self.hide()

    def set_fig3(self):
        height, width = (self.parent.size().height() - self.parent.height_button) // self.parent.gridstep, \
                        self.parent.size().width() // self.parent.gridstep

        if height < 32 or width < 32:
            print("Small window")
        else:
            fig = np.array([[False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, True, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, True, False, True, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             True, True, False, False, False, True, False, False, False, True, True, False, False,
                             False,
                             False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             True, True, False, False, True, False, False, False, False, False, True, False, False,
                             False,
                             False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, True, False, True, False, False, False, False, False,
                             False,
                             False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, True, True, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, True, True, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, True, True, False, False, False, False, False, False, False, False,
                             True, False, False, True, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, True, False, True, False, False, False, False, False, False, False, False, False,
                             True, False, True, False, False, False, False, True, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [True, False, False, False, False, False, True, False, False, False, False, False, False,
                             False, True, False, False, False, False, False, True, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, True, False, False, False, True, True, False, False, True, True, True, False, False,
                             False, False, False, False, False, False, True, False, False, False, False, False, False,
                             False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, True, False, True, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, True, True, False, False,
                             False, True, True, False, False, False],
                            [False, False, False, False, True, False, False, False, False, False, False, False, False,
                             False, False, False, False, True, False, False, False, True, False, False, True, False,
                             False,
                             True, True, False, False, False],
                            [False, False, False, False, False, False, False, False, True, False, False, False, False,
                             False, False, False, True, True, True, False, False, False, True, False, True, False,
                             False,
                             False, False, False, False, False],
                            [False, False, False, False, False, False, False, True, False, True, False, False, False,
                             False, False, False, True, False, True, False, False, False, False, True, False, False,
                             False,
                             False, False, False, False, False],
                            [False, False, False, True, True, False, False, True, False, False, True, False, False,
                             False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             True, False, False, False, False],
                            [False, False, False, True, True, False, False, False, True, True, False, False, False,
                             False,
                             False, False, False, False, False, False, False, False, False, False, False, False, True,
                             False, True, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, True, False,
                             False, False, False, False, False, False, False, True, True, True, False, False, True,
                             True,
                             False, False, False, True, False],
                            [False, False, False, False, False, False, False, False, False, False, False, True, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, True,
                             False, False, False, False, False, True],
                            [False, False, False, False, False, False, False, False, False, False, False, True, False,
                             False, False, False, False, True, True, False, False, False, False, False, False, False,
                             False, False, True, False, True, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, True, False, True, False, False, False, False, False, False, False,
                             False, True, True, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, True, True, True, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, True, True, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, True, False,
                             True, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, True, False, False, False, False,
                             False, True, False, False, True, True, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, True, True, False, False, False,
                             True, False, False, False, True, True, False, False, False, False, False, False, False,
                             False,
                             False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, True, False, True, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False],
                            [False, False, False, False, False, False, False, False, False, False, True, False, False,
                             False, False, False, False, False, False, False, False, False, False, False, False, False,
                             False, False, False, False, False, False]])

            dx, dy = (width - 32) // 2, (height - 32) // 2

            for j in range(dy):
                for i in range(width):
                    self.grid[j, i] = False

            for j in range(dy, height - dy - height % 2):
                for i in range(dx):
                    self.grid[j, i] = False
                for i in range(dx, width - dx - width % 2):
                    self.grid[j, i] = fig[i - dx, j - dy]
                for i in range(width - dx - width % 2, width):
                    self.grid[j, i] = False

            for j in range(height - dy - height % 2, height):
                for i in range(width):
                    self.grid[j, i] = False

            self.parent.grid = np.copy(self.grid)
            self.hide()

    def cancel(self):
        self.hide()

    def ok(self):
        self.parent.grid = np.copy(self.grid)
        self.hide()
