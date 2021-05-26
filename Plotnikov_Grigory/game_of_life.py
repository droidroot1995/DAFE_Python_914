import sys
import numpy as np

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer, Qt


class Map:
    def __init__(self, n=50):
        # поле игры состоит из n на n клеток, заполненных 0 (нет жизни) и 1 (есть жизнь)
        self.n = n
        self.map = np.zeros((n, n))

    def countAliveNeighbors(self, i, j):
        x_range = np.array([(i - 1) % self.n, i % self.n, (i + 1) % self.n])
        y_range = np.array([(j - 1) % self.n, j % self.n, (j + 1) % self.n])
        sum = 0
        for m in x_range:
            for n in y_range:
                if self.map[m, n] == 1:
                    sum += 1

        sum -= int(self.map[i, j])
        return sum

    def updateCell(self, i, j, new_map):
        num_of_neighbours = self.countAliveNeighbors(i, j)
        if num_of_neighbours == 3 or (num_of_neighbours == 2 and self.map[i, j] == 1):
            new_map[i, j] = 1
            return
        new_map[i, j] = 0

    def update_map(self):
        new_map = np.array(self.map.copy())

        for i in range(self.n):
            for j in range(self.n):
                self.updateCell(i, j, new_map)

        if (self.map == new_map).all():
            return False

        self.map = new_map
        return True

    def clear_map(self):
        self.map = np.zeros((self.n, self.n))

class GameWindow(QWidget, Map):
    def __init__(self, n=50, cell_size=16):
        QWidget.__init__(self)
        Map.__init__(self, n)

        self.cell_size = cell_size
        self.size = n * cell_size

        self.button_w = round(self.size / 3)
        self.button_h = 50

        self.time_delay = 100
        self.is_game_on = False

        self.alive_cell_color = QColor(80, 220, 255, 235)
        self.dead_cell_color = QColor(0, 0, 0)
        self.is_mouse_left_clicked = False
        self.is_mouse_right_clicked = False
        self.setMouseTracking(True)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game of life')
        self.setFixedSize(self.size + 1, self.size + self.button_h)
        self.initButtons()
        self.show()

    def initButtons(self):
        start_button = QPushButton('start', self)
        start_button.setGeometry(0, self.size, self.button_w, self.button_h)
        start_button.setStyleSheet(
            "QPushButton {background-color: black; color: rgb(50, 200, 240); border: 1px solid rgb(50, 200, 240)}")
        start_button.clicked.connect(self.start)

        stop_button = QPushButton('stop', self)
        stop_button.setGeometry(self.button_w, self.size, self.button_w, self.button_h)
        stop_button.setStyleSheet(
            "QPushButton {background-color: black; color: rgb(50, 200, 240); border: 1px solid rgb(50, 200, 240)}")
        stop_button.clicked.connect(self.stop)

        clear_button = QPushButton('clear', self)
        clear_button.setGeometry(2 * self.button_w, self.size, self.button_w, self.button_h)
        clear_button.setStyleSheet(
            "QPushButton {background-color: black; color: rgb(50, 200, 240); border: 1px solid rgb(50, 200, 240)}")
        clear_button.clicked.connect(self.clear)

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        if x < self.size and y < self.size:
            i = x // self.cell_size
            j = y // self.cell_size
            if event.button() == Qt.RightButton:
                self.map[i, j] = 0
            elif event.button() == Qt.LeftButton:
                self.map[i, j] = 1
            self.update()

        if event.button() == Qt.RightButton:
            self.is_mouse_right_clicked = True
        elif event.button() == Qt.LeftButton:
            self.is_mouse_left_clicked = True

    def mouseMoveEvent(self, event):
        if self.is_mouse_right_clicked or self.is_mouse_left_clicked:
            x = event.x()
            y = event.y()
            if x < self.size and y < self.size:
                i = x // self.cell_size
                j = y // self.cell_size
                self.map[i, j] = 1 if self.is_mouse_left_clicked else 0
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.is_mouse_right_clicked = False
        elif event.button() == Qt.LeftButton:
            self.is_mouse_left_clicked = False

    def start(self, event):
        self.is_game_on = True
        self.updateWorld()

    def stop(self, event):
        self.is_game_on = False

    def clear(self, event):
        self.clear_map()
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.paint(qp)
        qp.end()

    def paint(self, qp):
        for i in range(self.n):
            for j in range(self.n):
                if self.map[i, j] == 1:
                    qp.setBrush(self.alive_cell_color)
                else:
                    qp.setBrush(self.dead_cell_color)
                qp.drawRect(i * self.cell_size, j * self.cell_size, self.cell_size, self.cell_size)

    def updateWorld(self):
        if self.is_game_on:
            map_state = self.update_map()
            if not map_state:
                self.is_game_on = False
                return

            self.update()
            QTimer.singleShot(self.time_delay, self.updateWorld)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = GameWindow()
    w.show()

    sys.exit(app.exec_())