import sys
from PyQt5 import QtCore, QtWidgets, QtGui

from board import Board


class BoardGUI(QtWidgets.QWidget, QtCore.QObject):

    def __init__(self, n, m, grid = True, cyclic=True):
        super(BoardGUI, self).__init__(None)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.board = Board(n, m, cyclic=True)

        self.n = n
        self.m = m
        self.square_size = min(self.width() / m, self.height() / n)

        self.grid = grid

        self.started = False

    def minimumSizeHint(self):
        return QtCore.QSize(300, 300)

    def resizeEvent(self, event):

        self.square_size = int(min(self.width() / self.m, self.height() / self.n)) + 1
        self.left = int(self.width() / 2 - self.square_size * self.m / 2)
        self.top = int(self.height() / 2 - self.square_size * self.n / 2)

    def paintEvent(self, event=None):

        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.black, 0))

        painter.drawRect(QtCore.QRect(self.left, self.top, self.square_size * self.m, self.square_size * self.n))

        for i in range(self.n):
            for j in range(self.m):

                if self.grid:

                    painter.drawLine(QtCore.QPointF(self.left + j * self.square_size, self.top),
                                     QtCore.QPointF(self.left + j * self.square_size, self.top + self.square_size * self.n))

                    painter.drawLine(QtCore.QPointF(self.left, self.top + i * self.square_size),
                                     QtCore.QPointF(self.left + self.m * self.square_size, self.top + i * self.square_size))

                if self.board.board[i, j]:
                    painter.fillRect(QtCore.QRect(self.left + j * self.square_size, self.top + i * self.square_size, self.square_size, self.square_size), QtGui.QColor('black'))

    finished = QtCore.pyqtSignal()

    def mousePressEvent(self, event):

        j = int((event.x() - self.left) / self.square_size)
        i = int((event.y() - self.top) / self.square_size)

        if i < 0 or i >= self.n or j < 0 or j >= self.m:
            return

        self.board.change(i, j)

        self.repaint()

    def step(self):

        if not self.board.step():
            self.finished.emit()

        self.repaint()


class Controls(QtWidgets.QWidget):

    def __init__(self, main_field):
        super(Controls, self).__init__(None)

        self.field = main_field
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.field.step)

        self.field.finished.connect(self.pause)

        layout = QtWidgets.QVBoxLayout()

        self.start_button = QtWidgets.QPushButton('Start')
        self.pause_button = QtWidgets.QPushButton("Pause")
        self.clear_button = QtWidgets.QPushButton("Clear")

        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.clear_button.clicked.connect(self.clear)

        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.clear_button)

        self.setLayout(layout)

    def start(self):
        self.timer.start(300)

    def pause(self):
        self.timer.stop()

    def clear(self):
        self.field.board.clear()
        self.field.repaint()


class Window(QtWidgets.QWidget):

    def __init__(self):

        super(Window, self).__init__(None)

        self.drawing = BoardGUI(30, 50, True)
        expanding = QtWidgets.QSizePolicy.Expanding
        policy = QtWidgets.QSizePolicy(expanding, expanding)
        self.drawing.setSizePolicy(policy)

        self.controls = Controls(self.drawing)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.drawing)
        layout.addWidget(self.controls)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())

