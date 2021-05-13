import sys
from PyQt5 import QtCore, QtWidgets, QtGui

from window import Board

class BoardGUI(QtWidgets.QWidget, QtCore.QObject):

    def __init__(self, n = 20, m = 30, color = 'Black', grid = True):
        super(BoardGUI, self).__init__(None)
        self.setBackgroundRole(QtGui.QPalette.Base)
        self.setAutoFillBackground(True)
        self.board = Board(n, m)

        self.n = n
        self.m = m
        self.color = color
        self.square_size = min(self.width() / m, self.height() / n)

        self.grid = grid

        self.started = False

    def minimumSizeHint(self):
        return QtCore.QSize(300, 300)

    def resizeEvent(self, event):
        self.square_size = int(min(self.width() / self.m, self.height() / self.n))
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
                    painter.fillRect(QtCore.QRect(self.left + j * self.square_size, self.top + i * self.square_size, self.square_size, self.square_size), QtGui.QColor(self.color))

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
    def __init__(self, width, height, color):
        super(Controls, self).__init__(None)

        self.field = BoardGUI(width, height, color)
        expanding = QtWidgets.QSizePolicy.Expanding
        policy = QtWidgets.QSizePolicy(expanding, expanding)
        self.field.setSizePolicy(policy)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.field.step)

        self.field.finished.connect(self.pause)

        self.layoutB = QtWidgets.QHBoxLayout()

        self.start_button = QtWidgets.QPushButton('Start')
        self.pause_button = QtWidgets.QPushButton('Pause')
        self.clear_button = QtWidgets.QPushButton('Clear')

        self.start_button.clicked.connect(self.start)
        self.pause_button.clicked.connect(self.pause)
        self.clear_button.clicked.connect(self.clear)

        self.layoutB.addWidget(self.start_button)
        self.layoutB.addWidget(self.pause_button)
        self.layoutB.addWidget(self.clear_button)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.field)
        layout.addItem(self.layoutB)

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

        width, _ = QtWidgets.QInputDialog.getInt(self, "Get integer", "Width:", 30, 0, 100, 1)
        height, _ = QtWidgets.QInputDialog.getInt(self, "Get integer", "Height:", 50, 0, 100, 1)

        colors = ("red", "blue", "green", "black")
        color, _ = QtWidgets.QInputDialog.getItem(self, "Get item", "Color:", colors, 0, False)

        self.controls = Controls(width, height, color)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.controls)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())