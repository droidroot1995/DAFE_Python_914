import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QColorDialog, QInputDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QTimer

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

        #self.color = Qt.black
        self.color = QBrush(QColor(0, 0, 0))
        self.delay = 10    #мс

        self.height_button = 50
        self.width_button = 100
        self.grid = np.zeros([height, width], dtype=bool)
        self.gridstep = gridstep
        self.setFixedSize(width * gridstep, height * gridstep + self.height_button)

        self.make_buttons()

        self.show()

        #self.press_update = (-1, -1)

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

        but_start.clicked.connect(self.start)
        but_stop.clicked.connect(self.stop)
        but_next.clicked.connect(self.next)
        but_settings.clicked.connect(self.settings)
        but_clear.clicked.connect(self.clear)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.drawLines(qp)
        self.drawCells(qp)
        qp.end()

    def drawCells(self, qp):
        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep

        qp.setBrush(self.color)

        for i in range(height//step):
            for j in range(width // step):
                if self.grid[j, i]:
                    qp.drawRect(i * step, j * step, step, step)

    def drawLines(self, qp):
        pen = QPen(self.color, 2, Qt.SolidLine)
        qp.setPen(pen)
        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep
        for i in range(step, height+1, step):
            qp.drawLine(0, i, width, i)
        for i in range(step, width, step):
            qp.drawLine(i, 0, i, height)

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
        self.is_start = True
        self.go()

    def stop(self):
        self.is_start = False

    def next(self):
        self.is_start = False
        self.go()


    def settings(self):
        self.sett = Settings(self)

    def clear(self):
        self.is_start = False
        self.grid = np.zeros([(self.size().height() - self.height_button) // self.gridstep,
                              self.size().width() // self.gridstep], dtype=bool)
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

        for i in range(gheight):
            for j in range(gwidth):
                s = 0
                for k in range(-1, 2):
                    for n in range(-1, 2):
                        x = j + n if j + n < gheight else 0
                        y = i + k if i + k < gwidth else 0
                        if self.grid[y, x]:
                            s += 1
                if self.grid[i, j]:
                    s -= 1
                    if s != 2 and s != 3:
                        new_grid[i, j] = False
                else:
                    if s == 3:
                        new_grid[i, j] = True

        if (self.grid == new_grid).all():
            return False

        self.grid = new_grid
        return True



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    sys.exit(app.exec_())
