from shapes import *

class Game(QWidget):
    def __init__(self, width=50, height=50, gridstep=10):
        super().__init__()

        self.setWindowTitle("Игра в жизнь")

        self.color = QBrush(QColor(0, 0, 0))
        self.delay = 10

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
        but_start = QPushButton('Старт', self)
        but_start.setGeometry(0,
                              height,
                              self.width_button,
                              self.height_button)
        self.is_start = False

        but_stop = QPushButton('Стоп', self)
        but_stop.setGeometry(self.width_button,
                             height,
                             self.width_button,
                             self.height_button)
        self.is_stop = False

        but_next = QPushButton('Далее', self)
        but_next.setGeometry(self.width_button * 2,
                             height,
                             self.width_button,
                             self.height_button)

        but_clear = QPushButton('Очистить', self)
        but_clear.setGeometry(self.width_button * 3,
                              height,
                              self.width_button,
                              self.height_button)

        but_boundar = QPushButton('Границы', self)
        but_boundar.setGeometry(self.width_button * 4,
                                height,
                                self.width_button,
                                self.height_button)

        but_start.clicked.connect(self.start)
        but_stop.clicked.connect(self.stop)
        but_next.clicked.connect(self.next)
        but_clear.clicked.connect(self.clear)
        but_boundar.clicked.connect(self.boundar)

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

        for j in range(height // step):
            for i in range(width // step):
                if self.grid[j, i]:
                    qp.drawRect(i * step, j * step, step, step)

    def drawLines(self, qp):
        pen = QPen(self.color, 2, Qt.SolidLine)
        qp.setPen(pen)
        height = self.size().height() - self.height_button
        width = self.size().width()
        step = self.gridstep

        for i in range(0, height + 1, step):
            qp.drawLine(0, i, width, i)
        for i in range(0, width + 1, step):
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
                if x >= 0 and y >= 0 and event.x() < self.width() and \
                        event.y() < self.height() - self.height_button:
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

    def boundar(self):
        self.has_boundaries = not self.has_boundaries
        self.update()

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

        height, width = self.size().height() - self.height_button, self.size().width()
        step = self.gridstep
        gheight, gwidth = height // step, width // step

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
