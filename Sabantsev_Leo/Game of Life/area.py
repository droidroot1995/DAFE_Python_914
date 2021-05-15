import sys
import os
import game
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, uic

sys.path.append(os.getcwd())


class Window(QtGui.QMainWindow):
    def __init__(self):

        QtGui.QMainWindow.__init__(self)

        # константы
        self.columnSize = 20
        self.rowSize = 20
        self.state = game.Game(self.rowSize, self.columnSize)
        self.alive = 0
        self.aliveEvolution = []
        self.color1 = pg.mkBrush(255, 255, 255)
        self.color2 = pg.mkBrush(0, 0, 0)
        self.brushes = []
        self.pause = True
        self.generation = 0

        # загрузка пользовательского интерфейса
        self.ui = uic.loadUi('userInterface.ui', self)

        # подключаем сигналы
        self.ui.tick.clicked.connect(self.nextState)
        self.ui.buttonStartPause.clicked.connect(self.startPause)
        self.ui.buttonClean.clicked.connect(self.cleanState)
        self.ui.sizeOptions.valueChanged.connect(self.gridSize)
        self.ui.speedSlide.valueChanged.connect(self.changeSpeed)

        # создем график с помощью массива ячеек
        self.gfx = self.ui.PlotView.addPlot()
        self.restartPlot()
        self.createGrid()
        self.updateGrid()

        # теперь живые ячейки
        self.gfx2 = self.ui.PlotView2.addPlot(title='Живые клетки')
        self.restartPlot2()

        # Таймер
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.TIME_INTERVAL = 1000
        self.TIME_INTERVAL_MAX = 2000

    # Игровое поле
    def restartPlot(self):
        self.ui.PlotView.removeItem(self.gfx)
        self.gfx = self.ui.PlotView.addPlot()
        self.data = pg.ScatterPlotItem()
        self.gfx.addItem(self.data)
        self.gfx.hideAxis('bottom')
        self.gfx.hideAxis('left')
        self.gfx.setXRange(1, 0)
        self.gfx.setYRange(1, 0)
        self.gfx.setMouseEnabled(x=False, y=False)
        self.gfx.enableAutoRange(x=True, y=True)

    # График
    def restartPlot2(self):
        self.ui.PlotView2.removeItem(self.gfx2)
        self.gfx2 = self.ui.PlotView2.addPlot(title='Живые клетки по поколениям')
        self.gfx2.setLabel('left', 'Живые клетки')
        self.gfx2.setLabel('bottom', 'Поколение')
        self.data2 = self.gfx2.plot(pen='y')
        self.data2.setData(self.aliveEvolution)
        self.gfx2.enableAutoRange(x=True, y=True)

    # задаем цвета сетки
    def createGrid(self):
        self.pause = True
        self.generation = 0
        self.cells = []
        self.brushes = []
        self.data.clear()
        self.state = game.Game(self.rowSize, self.columnSize)

        for i in range(self.rowSize):
            for j in range(self.columnSize):
                if self.state.prevState[i, j] == 0:
                    self.brushes.append(self.color1)
                else:
                    self.brushes.append(self.color2)
                self.cells.append({'pos': (j + 0.5, self.rowSize - i + 0.5),
                                   'size': 300 / self.rowSize,
                                   'symbol': 's',
                                   'brush': self.brushes[-1],
                                   'pen': {'color': (0, 0, 0),
                                           'width': 0.5},
                                   })

        self.data.addPoints(self.cells)
        self.data.sigClicked.connect(self.clicked)

    # обновляем цвета сетки
    def updateGrid(self):
        ctr = 0
        self.alive = 0
        for i in range(self.rowSize):
            for j in range(self.columnSize):
                if self.state.prevState[i, j] == 0:
                    self.brushes[ctr] = self.color1
                else:
                    self.brushes[ctr] = self.color2
                    self.alive += 1
                ctr += 1
        self.data.setBrush(self.brushes, mask=None)

    def gridSize(self, N):
        self.columnSize = N
        self.rowSize = N
        self.restartPlot()
        self.createGrid()

    def updateTimer(self):
        if self.pause == False:
            self.nextState()
            self.timer.start(self.TIME_INTERVAL)

    def changeSpeed(self, speed):
        self.TIME_INTERVAL = self.TIME_INTERVAL_MAX - speed

    # пауза/старт игры
    def startPause(self):
        if self.pause:
            self.pause = False
            self.updateTimer()
        else:
            self.pause = True

    def nextState(self):
        self.state.tick()
        self.updateGrid()
        linea = '# Поколение: ' + str(self.generation) + '     # Живые клетки: ' + str(self.alive)
        self.ui.infoBox.append(linea)
        self.aliveEvolution.append(self.alive)
        self.restartPlot2()
        self.generation += 1

    # Создаем событие клика на клетку
    def clicked(self, plot, points):
        x, y = points[0].pos()
        x = int(x - 0.5)
        y = int(y - 1.5)
        if self.state.prevState[self.rowSize - 1 - y, x] == 1:
            self.state.prevState[self.rowSize - 1 - y, x] = 0
        else:
            self.state.prevState[self.rowSize - 1 - y, x] = 1
        self.updateGrid()

    # Событие очистки поля
    def cleanState(self):
        self.pause = True
        self.aliveEvolution = []
        self.restartPlot()
        self.createGrid()
        self.updateGrid()


App = QtGui.QApplication(sys.argv)
win = Window()
win.show()
sys.exit(App.exec_())
