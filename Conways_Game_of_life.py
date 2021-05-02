import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QColorDialog, QInputDialog, QMenu
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer

class Figures(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Figures")

        self.height_button = 100
        self.width_button = 100
        self.setFixedSize(self.height_button*2, self.width_button*2)

        self.make_buttons()
        self.grid = np.copy(parent.grid)
        self.show()

    def make_buttons(self):
        but_fig1 = QPushButton('Spaceship', self)
        but_fig1.setGeometry(0, 0, self.width_button, self.height_button)

        but_fig2 = QPushButton('Schick', self)
        but_fig2.setGeometry(self.width_button, 0, self.width_button, self.height_button)

        but_fig3 = QPushButton('Popower', self)
        but_fig3.setGeometry(0, self.height_button, self.width_button, self.height_button)

        but_cancel = QPushButton('Cancel', self)
        but_cancel.setGeometry(self.width_button, self.height_button, self.width_button, self.height_button)

        but_fig1.clicked.connect(self.set_fig1)
        but_fig2.clicked.connect(self.set_fig2)
        but_fig3.clicked.connect(self.set_fig3)
        but_cancel.clicked.connect(self.cancel)

    def set_fig1(self):
        height = (self.parent.size().height() - self.parent.height_button) // self.parent.gridstep
        width = self.parent.size().width() // self.parent.gridstep
        if height < 5 or width < 7:
            print("Small window")
        fig = np.array([[False, False, True, True, False, False, False],
                        [True, False, False, False, False, True, False],
                        [False, False, False, False, False, False, True],
                        [True, False, False, False, False, False, True],
                        [False, True, True, True, True, True, True]])

        dx = width - 7
        dy = (height - 5) // 2
        for j in range(dy):
            for i in range(width):
                self.grid[j, i] = False
        for j in range(dy, height - dy - 1 + height % 2):
            for i in range(width-dx):
                self.grid[j, i] = fig[j - dy, i]
            for i in range(width-dx, width):
                self.grid[j, i] = False
        for j in range(height - dy - 1 + height % 2, height):
            for i in range(width):
                self.grid[j, i] = False

        self.parent.grid = np.copy(self.grid)
        self.hide()

    def set_fig2(self):
        height = (self.parent.size().height() - self.parent.height_button) // self.parent.gridstep
        width = self.parent.size().width() // self.parent.gridstep
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

        dx = width - 20
        dy = (height - 11) // 2
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
        height = (self.parent.size().height() - self.parent.height_button) // self.parent.gridstep
        width = self.parent.size().width() // self.parent.gridstep
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
                          True, True, False, False, False, True, False, False, False, True, True, False, False, False,
                          False, False, False, False, False],
                         [False, False, False, False, False, False, False, False, False, False, False, False, False,
                          True, True, False, False, True, False, False, False, False, False, True, False, False, False,
                          False, False, False, False, False],
                         [False, False, False, False, False, False, False, False, False, False, False, False, False,
                          False, False, False, False, False, True, False, True, False, False, False, False, False, False,
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
                          False, False, False, False, True, False, False, False, True, False, False, True, False, False,
                          True, True, False, False, False],
                         [False, False, False, False, False, False, False, False, True, False, False, False, False,
                          False, False, False, True, True, True, False, False, False, True, False, True, False, False,
                          False, False, False, False, False],
                         [False, False, False, False, False, False, False, True, False, True, False, False, False,
                          False, False, False, True, False, True, False, False, False, False, True, False, False, False,
                          False, False, False, False, False],
                         [False, False, False, True, True, False, False, True, False, False, True, False, False, False,
                          False, False, False, False, False, False, False, False, False, False, False, False, False,
                          True, False, False, False, False],
                         [False, False, False, True, True, False, False, False, True, True, False, False, False, False,
                          False, False, False, False, False, False, False, False, False, False, False, False, True,
                          False, True, False, False, False],
                         [False, False, False, False, False, False, False, False, False, False, False, False, False,
                          False, False, False, False, False, False, False, False, False, False, False, False, False,
                          False, False, False, False, False, False],
                         [False, False, False, False, False, False, False, False, False, False, False, True, False,
                          False, False, False, False, False, False, False, True, True, True, False, False, True, True,
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
                          True, False, False, False, True, True, False, False, False, False, False, False, False, False,
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

            dx = (width - 32) // 2
            dy = (height - 32) // 2
            for j in range(dy):
                for i in range(width):
                    self.grid[j, i] = False
            for j in range(dy, height - dy - height % 2):
                for i in range(dx):
                    self.grid[j, i] = False
                for i in range(dx, width - dx - width % 2):
                    self.grid[j, i] = fig[i-dx, j-dy]
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


class Settings(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Settings")

        self.height_button = 200
        self.width_button = 200
        self.setFixedSize(self.height_button*2, self.width_button*2)

        self.make_buttons()
        self.color = parent.color
        self.delay = parent.delay

        self.show()

    def make_buttons(self):
        but_color = QPushButton('Color', self)
        but_color.setGeometry(0, 0, self.width_button, self.height_button)

        but_delay = QPushButton('Delay', self)
        but_delay.setGeometry(self.width_button, 0, self.width_button, self.height_button)

        but_cancel = QPushButton('Cancel', self)
        but_cancel.setGeometry(0, self.height_button, self.width_button, self.height_button)

        but_ok = QPushButton('Ok', self)
        but_ok.setGeometry(self.width_button, self.height_button, self.width_button, self.height_button)

        but_color.clicked.connect(self.set_color)
        but_delay.clicked.connect(self.set_delay)
        but_cancel.clicked.connect(self.cancel)
        but_ok.clicked.connect(self.ok)

    def set_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color

    def set_delay(self):
        ok = False
        delay, ok = QInputDialog.getInt(self, "Set delay", "New delay:", value=1, min=1)
        if ok:
            self.delay = delay


    def cancel(self):
        self.hide()

    def ok(self):
        self.parent.color = self.color
        self.parent.delay = self.delay
        self.hide()


class Game(QWidget):
    def __init__(self, width=50, height=50, gridstep=20):
        super().__init__()

        self.setWindowTitle("Conways Game of life")

        self.color = QBrush(QColor(0, 0, 0))
        self.delay = 10    #мс

        self.height_button = 50
        self.width_button = width * gridstep // 7
        self.grid = np.zeros([height, width], dtype=bool)
        self.gridstep = gridstep
        self.setFixedSize(width * gridstep, height * gridstep + self.height_button)
        self.has_boundaries = False

        self.make_buttons()
        self.show()

    def make_buttons(self):
        height = self.size().height() - self.height_button
        but_start = QPushButton('Start', self)
        but_start.setGeometry(0, height, self.width_button, self.height_button)
        self.is_start = False

        but_stop = QPushButton('Stop', self)
        but_stop.setGeometry(self.width_button, height, self.width_button, self.height_button)
        self.is_stop = False

        but_next = QPushButton('Next', self)
        but_next.setGeometry(self.width_button*2, height, self.width_button, self.height_button)

        but_settings = QPushButton('Settings', self)
        but_settings.setGeometry(self.width_button * 3, height, self.width_button, self.height_button)

        but_clear = QPushButton('Clear', self)
        but_clear.setGeometry(self.width_button * 4, height, self.width_button, self.height_button)

        but_boundar = QPushButton('Boundaries', self)
        but_boundar.setGeometry(self.width_button * 5, height, self.width_button, self.height_button)

        but_figures = QPushButton('Figures', self)
        but_figures.setGeometry(self.width_button * 6, height, self.width_button, self.height_button)

        but_start.clicked.connect(self.start)
        but_stop.clicked.connect(self.stop)
        but_next.clicked.connect(self.next)
        but_settings.clicked.connect(self.settings)
        but_clear.clicked.connect(self.clear)
        but_boundar.clicked.connect(self.boundar)
        but_figures.clicked.connect(self.figures)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawCells(qp)
        qp.end()

    def drawCells(self, qp):
        pen = QPen(self.color, 2, Qt.SolidLine)
        qp.setPen(pen)
        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep

        qp.setBrush(self.color)

        for j in range(height//step):
            for i in range(width // step):
                if self.grid[j, i]:
                    qp.drawRect(i * step, j * step, step, step)

    def drawLines(self, qp):
        pen = QPen(self.color, 2, Qt.SolidLine)
        qp.setPen(pen)
        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep
        for i in range(0, height+1, step):
            qp.drawLine(0, i, width, i)
        for i in range(0, width+1, step):
            qp.drawLine(i, 0, i, height)

        if self.has_boundaries:
            pen = QPen(self.color, 4, Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(0, 0, width, 0)
            qp.drawLine(0, 0, 0, height)
            qp.drawLine(0, height, width, height)
            qp.drawLine(width, 0, width, height)

    def mousePressEvent(self, event):
        if not self.is_start:
            x, y = event.x() // self.gridstep, event.y() // self.gridstep
            self.grid[y, x] = not self.grid[y, x]
            self.update()
            self.press_update = (y, x)

    def mouseMoveEvent(self, event):
        if not self.is_start:
            x, y = event.x() // self.gridstep, event.y() // self.gridstep
            if self.press_update != (y, x):
                if x >= 0 and y >= 0 and event.x() < self.width() and event.y() < self.height() - self.height_button:
                    self.grid[y, x] = not self.grid[y, x]
                    self.update()
                    self.press_update = (y, x)

    def mouseReleaseEvent(self, event):
        self.press_update = (-1, -1)

    def start(self):
        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep
        gheight = height // step
        gwidth = width // step
        f = open("1.txt", 'w')
        for j in range(gheight):
            for i in range(gwidth):
                f.write(str(self.grid[j, i]))
                f.write(" ")
                if self.grid[j, i]:
                    f.write(" ")
            f.write("\n")
        f.close()
        print("ok")

        self.is_start = True
        self.go()

    def stop(self):
        self.is_start = False

    def next(self):
        self.is_start = False
        self.go()

    def settings(self):
        self.sett = Settings(self)

    def boundar(self):
        self.has_boundaries = not self.has_boundaries
        self.update()

    def clear(self):
        self.is_start = False
        self.grid = np.zeros([(self.size().height() - self.height_button) // self.gridstep,
                              self.size().width() // self.gridstep], dtype=bool)
        self.update()

    def figures(self):
        self.fig = Figures(self)
        self.update()

    def go(self):
        if not self.update_grid():
            self.is_start = False
            return
        self.update()
        if self.is_start:
            QTimer.singleShot(self.delay, self.go)
        else:
            return

    def update_grid(self):
        new_grid = np.copy(self.grid)

        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep
        gheight = height // step
        gwidth = width // step

        for j in range(gheight):
            for i in range(gwidth):
                s = 0
                for k in range(-1, 2):
                    for n in range(-1, 2):
                        if self.has_boundaries:
                            if j + n < 0 or j + n == gheight:
                                continue
                            if i + k < 0 or i + k == gwidth:
                                continue
                        y = j + n if j + n < gheight else 0
                        x = i + k if i + k < gwidth else 0
                        if self.grid[y, x]:
                            s += 1
                if self.grid[j, i]:
                    s -= 1
                    if s != 2 and s != 3:
                        new_grid[j, i] = False
                else:
                    if s == 3:
                        new_grid[j, i] = True

        if (self.grid == new_grid).all():
            return False

        self.grid = new_grid
        return True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    sys.exit(app.exec_())
