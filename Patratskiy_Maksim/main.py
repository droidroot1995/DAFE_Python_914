import sys
import numpy as np

from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QTimer


class Game:
    # class Game - логика игры
    # отвечает за взаимодействие с объектамми
    # основной объект - карта, заполненная 0
    # объекты на карте - ячейки, если живы, то значение в них 1, иначе 0

    def __init__(self, width=100, height=100):
        # создаем карту размерами w на h, изначально
        # заданную массивом из 0

        self.map_size = (width, height)
        self.map = np.zeros(self.map_size)

    def _map_size_mod_of_number(self, x, map_index):
        x = x + self.map_size[map_index]
        x = divmod(x, self.map_size[map_index])[1]
        return x

    def put_cell(self, i, j):
        self.map[i, j] = 1

    def del_cell(self, i, j):
        self.map[i, j] = 0

    def _map_size_mod(self, x, y, z, map_index):
        x = x + self.map_size[map_index]
        x = divmod(x, self.map_size[map_index])[1]

        y = y + self.map_size[map_index]
        y = divmod(y, self.map_size[map_index])[1]

        z = z + self.map_size[map_index]
        z = divmod(z, self.map_size[map_index])[1]

        return [x, y, z]

    def _chek_neighbourhood(self, i, j):
        # возвращает количество соседей у [i, j] ячейки
        xdiap = np.array(self._map_size_mod(i - 1, i, i + 1, map_index=0))
        ydiap = np.array(self._map_size_mod(j - 1, j, j + 1, map_index=1))

        sum = 0
        for m in xdiap:
            for n in ydiap:
                if self.map[m, n] == 1:
                    sum += 1

        sum -= int(self.map[i, j])
        return sum

    def _update_cell(self, i, j, new_map):
        # обновляем состояние ячейки при обновлении всей карты
        num_of_neighbours = self._chek_neighbourhood(i, j)
        if num_of_neighbours == 3 or (num_of_neighbours == 2 and self.map[i, j] == 1):
            new_map[i, j] = 1
            return
        new_map[i, j] = 0

    def update_map(self):
        # обновляем состояние всех ячеек на карте
        new_map = np.array(self.map.copy())

        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                self._update_cell(i, j, new_map)

        if (self.map == new_map).all():
            return False

        self.map = new_map
        return True

    def clear_map(self):
        # очищаем карту
        self.map = np.zeros(self.map_size)


# ---------------------------------------------------------------------------------------------------------------------

class GameWindow(QWidget, Game):
    # class Window - холст и кисть для изображения игры

    def __init__(self, map_width=100, map_height=50, cell_size=10):
        QWidget.__init__(self)
        Game.__init__(self, map_width, map_height)

        self.cell_size = cell_size
        self.size = (map_width * cell_size, map_height * cell_size)
        self.button_size = (min(180, round(self.size[0] / 5)), 100)

        self.time_delay = 40
        self.is_game_on = False

        self.brush_index = 0
        self.brush_colors = {0: (QColor(255, 80, 0, 160), QColor(0, 0, 100)),
                             1: (QColor(0, 255, 80, 160), QColor(100, 0, 0)),
                             2: (QColor(0, 0, 0), QColor(255, 255, 255)),
                             3: (QColor(200, 50, 80, 160), QColor(30, 100, 80)),
                             4: (QColor(0, 150, 0, 160), QColor(0, 0, 100, 160))}

        self.is_mouse_left_clicked = False
        self.is_mouse_right_clicked = False
        self.setMouseTracking(True)
        self.brush_size = 1

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game of life')
        self.setFixedSize(self.size[0] + 1, self.size[1] + self.button_size[1])

        self.initButtons()
        self.show()

    def initButtons(self):
        start_button = QPushButton('start', self)
        start_button.setGeometry(0, self.size[1], self.button_size[0], self.button_size[1])
        start_button.clicked.connect(self.start)

        stop_button = QPushButton('stop', self)
        stop_button.setGeometry(self.button_size[0], self.size[1], self.button_size[0], self.button_size[1])
        stop_button.clicked.connect(self.stop)

        clear_button = QPushButton('clear', self)
        clear_button.setGeometry(2 * self.button_size[0], self.size[1], self.button_size[0], self.button_size[1])
        clear_button.clicked.connect(self.clear)

        color_button = QPushButton('color', self)
        color_button.setGeometry(3 * self.button_size[0], self.size[1], self.button_size[0], self.button_size[1])
        color_button.clicked.connect(self.color)

        brush_size_button = QPushButton('brush size', self)
        brush_size_button.setGeometry(4 * self.button_size[0], self.size[1], self.button_size[0], self.button_size[1])
        brush_size_button.clicked.connect(self.brushSize)

    def changeStateOfCell(self, i, j, func):
        brush_half = (self.brush_size - 1) // 2
        x_diap = np.array([self._map_size_mod_of_number(k, 0) for k in range(i - brush_half, i + brush_half + 1, 1)])
        y_diap = np.array([self._map_size_mod_of_number(k, 1) for k in range(j - brush_half, j + brush_half + 1, 1)])
        for m in x_diap:
            for n in y_diap:
                func(m, n)

    def mousePressEvent(self, event):
        if event.button() == 1:
            x = event.x()
            y = event.y()
            if x < self.size[0] and y < self.size[1]:
                i = x // self.cell_size
                j = y // self.cell_size
                self.changeStateOfCell(i, j, self.put_cell)
                self.update()
            self.is_mouse_left_clicked = True
        else:
            x = event.x()
            y = event.y()
            if x < self.size[0] and y < self.size[1]:
                i = x // self.cell_size
                j = y // self.cell_size
                self.changeStateOfCell(i, j, self.del_cell)
                self.update()
            self.is_mouse_right_clicked = True

    def mouseMoveEvent(self, event):
        if self.is_mouse_left_clicked:
            x = event.x()
            y = event.y()
            if x < self.size[0] and y < self.size[1]:
                i = x // self.cell_size
                j = y // self.cell_size
                self.changeStateOfCell(i, j, self.put_cell)
                self.update()

        if self.is_mouse_right_clicked:
            x = event.x()
            y = event.y()
            if x < self.size[0] and y < self.size[1]:
                i = x // self.cell_size
                j = y // self.cell_size
                self.changeStateOfCell(i, j, self.del_cell)
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == 1:
            self.is_mouse_left_clicked = False
        else:
            self.is_mouse_right_clicked = False

    def start(self, event):
        self.is_game_on = True
        self.updateWorld()

    def stop(self, event):
        self.is_game_on = False

    def clear(self, event):
        self.clear_map()
        self.update()

    def color(self, event):
        self.brush_index = (self.brush_index + 1) % 5
        self.update()

    def brushSize(self, event):
        self.brush_size = (self.brush_size + 2) % 6
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.paint(qp)
        qp.end()

    def paint(self, qp):
        color_for_alive = self.brush_colors[self.brush_index][0]
        color_for_dead = self.brush_colors[self.brush_index][1]

        for i in range(self.map_size[0]):
            for j in range(self.map_size[1]):
                if self.map[i, j] == 1:
                    qp.setBrush(color_for_alive)
                else:
                    qp.setBrush(color_for_dead)
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

    w = GameWindow(77, 77, 7)
    w.show()

    sys.exit(app.exec_())
