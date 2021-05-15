import sys
import os
import numpy

sys.path.append(os.getcwd())


class Game(object):
    def __init__(self, W = 20, H = 20):
        # Инициализация переменных
        self.WIDTH = W
        self.HEIGHT = H
        self.prevState = numpy.zeros((self.HEIGHT, self.WIDTH))
        self.nextState = numpy.zeros((self.HEIGHT, self.WIDTH))
        numpy.copyto(self.prevState, self.nextState)

    def tick(self):
        # Смена состояния
        self.applyRules()
        numpy.copyto(self.prevState, self.nextState)

    def applyRules(self):
        # Правила игры
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                count = self.countNeighbors(i, j)
                # Живые
                if self.prevState[i, j] == 1:
                    # Субпопуляция
                    if count < 2:
                        self.nextState[i, j] = 0
                    # Перенаселение
                    elif count > 3:
                        self.nextState[i, j] = 0
                    # Застой
                    else:
                        self.nextState[i, j] = 1
                # Мертвые
                else:
                    # Размножение
                    if count == 3:
                        self.nextState[i, j] = 1

    def countNeighbors(self, i, j):
        # Подсчет числа живых соседей
        ctr = 0
        if i - 1 >= 0 and j - 1 >= 0 and self.prevState[i - 1, j - 1] == 1:
            ctr += 1
        if i - 1 >= 0 and self.prevState[i - 1, j] == 1:
            ctr += 1
        if i - 1 >= 0 and j + 1 < self.WIDTH and self.prevState[i - 1, j + 1] == 1:
            ctr += 1
        if j - 1 >= 0 and self.prevState[i, j - 1] == 1:
            ctr += 1
        if j + 1 < self.WIDTH and self.prevState[i, j + 1] == 1:
            ctr += 1
        if i + 1 < self.HEIGHT and j - 1 >= 0 and self.prevState[i + 1, j - 1] == 1:
            ctr += 1
        if i + 1 < self.HEIGHT and self.prevState[i + 1, j] == 1:
            ctr += 1
        if i + 1 < self.HEIGHT and j + 1 < self.WIDTH and self.prevState[i + 1, j + 1] == 1:
            ctr += 1

        return ctr
