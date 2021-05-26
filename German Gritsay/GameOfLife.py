import sys
import numpy as np

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QColorDialog, QInputDialog, QMenu
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer


class GameOfLife(QWidget):
    def __init__(self, width=50, height=50, grid_step=10):
        super().__init__()

        self.color = QBrush(QColor(50, 50, 50))
        self.time_delay = 10

        self.gridstep = grid_step
        self.height_button = height
        self.width_button = width * self.gridstep // 7

        self.grid = np.zeros([height, width], dtype=bool)
        self.setFixedSize(width * self.gridstep, height * self.gridstep + self.height_button)

        self.init_comp()

    def init_comp(self):
        self.setWindowTitle("Game of life")

        self.buttons()
        self.show()

    def buttons(self):
        height = self.size().height() - self.height_button

        start_button = QPushButton('Start', self)
        start_button.setGeometry(0, height, int(self.width_button * 1.75), self.height_button)
        start_button.clicked.connect(self.start)
        self.is_start = False

        stop_button = QPushButton('Stop', self)
        stop_button.setGeometry(int(self.width_button * 1.75), height, int(self.width_button * 1.75), self.height_button)
        stop_button.clicked.connect(self.stop)
        self.is_stop = False

        next_button = QPushButton('Next', self)
        next_button.setGeometry(int(self.width_button * 3.5), height, int(self.width_button * 1.75), self.height_button)
        next_button.clicked.connect(self.next)

        clear_button = QPushButton('Clear', self)
        clear_button.setGeometry(int(self.width_button * 5.25), height, int(self.width_button * 1.75), self.height_button)
        clear_button.clicked.connect(self.clear)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.paint(qp)
        qp.end()

    def paint(self, qp):
        pencil = QPen(self.color, 1, Qt.SolidLine)
        qp.setPen(pencil)

        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep

        qp.setBrush(self.color)

        for j in np.arange(height // step):
            for i in np.arange(width // step):
                if self.grid[j, i]:
                    qp.drawRect(i * step, j * step, step, step)

        for i in np.arange(0, height + 1, step):
            qp.drawLine(0, i, width, i)
        for i in np.arange(0, width + 1, step):
            qp.drawLine(i, 0, i, height)

    def mousePressEvent(self, event):
        if not self.is_start:
            x = event.x() // self.gridstep
            y = event.y() // self.gridstep
            self.grid[y, x] = not self.grid[y, x]
            self.update()
            self.press_update = (y, x)

    def mouseMoveEvent(self, event):
        if not self.is_start:
            x = event.x() // self.gridstep
            y = event.y() // self.gridstep
            if self.press_update != (y, x):
                if x >= 0 and y >= 0 and event.x() < self.width() and event.y() < self.height() - self.height_button:
                    self.grid[y, x] = not self.grid[y, x]
                    self.update()
                    self.press_update = (y, x)

    def start(self):
        self.is_start = True
        self.upd_step()

    def stop(self):
        self.is_start = False

    def next(self):
        self.is_start = False
        self.upd_step()

    def clear(self):
        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep

        self.is_start = False
        self.grid = np.zeros([height // step, width // step], dtype=bool)
        self.update()

    def upd_step(self):
        if not self.update_grid():
            self.is_start = False
            return

        self.update()

        if self.is_start:
            QTimer.singleShot(self.time_delay, self.upd_step)
        else:
            return

    def update_grid(self):
        sec_grid = np.copy(self.grid)

        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep

        for j in range(height // step):
            for i in range(width // step):
                s = 0
                for k in range(-1, 2):
                    for n in range(-1, 2):
                        y = j + n if j + n < height // step else 0
                        x = i + k if i + k < width // step else 0
                        if self.grid[y, x]:
                            s += 1
                if self.grid[j, i]:
                    s -= 1
                    if s != 2 and s != 3:
                        sec_grid[j, i] = False
                else:
                    if s == 3:
                        sec_grid[j, i] = True

        if (self.grid == sec_grid).all():
            return False

        self.grid = sec_grid
        return True



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = GameOfLife(70, 40, 15)

    sys.exit(app.exec_())
