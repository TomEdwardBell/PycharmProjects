import random
from sys import argv
from PySide2 import QtCore, QtGui, QtWidgets
import time


class Simulation(QtWidgets.QMainWindow):
    def __init__(self, width, height):
        super(Simulation, self).__init__()
        p = .5
        self.actives = []
        self.die_list = []
        self.add_list = []
        print(self.board)
        self.resize(1000, 1000)
        self.cell_width = self.width() / len(self.board[0])
        self.cell_height = self.height() / len(self.board[0])
        self.setStyleSheet('background-color: #FFFFFF;')
        self.show()

        while True:
            self.repaint()
            self.tick()

    def get_nears(self, x, y):
        nears = []
        h = len(self.board)
        w = len(self.board[0])

        for (dx, dy) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = dx + x, dy + y
            if 0 <= nx < w and 0 <= ny < h:
                nears.append((nx, ny))
        return nears

    def check(self, x, y):
        live_count = 0
        for (nx, ny) in self.get_nears(x, y):
            if self.board[nx][ny]:
                live_count += 1
        if self.board[x][y]:
            if live_count != 2 and live_count != 3:
                self.die_list.append((x, y))
        else:
            if live_count == 3:
                self.add_list.append((x, y))

    def tick(self):
        self.add_list = []
        self.die_list = []

        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                self.check(x, y)

        for (dx, dy) in self.die_list:
            self.board[dx][dy] = False

        for (ax, ay) in self.add_list:
            self.board[ax][ay] = True


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))
        h = len(self.board)
        w = len(self.board[0])
        cw = self.cell_width
        ch = self.cell_height
        for y in range(h):
            for x in range(w):
                if self.board[x][y]:
                    qp.drawRect(int(x*cw), int(y*ch), int(cw), int(ch))
        qp.end()


class Run():
    def __init__(self):
        self.s = Simulation(40, 40)


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    r = Run()
    app.exec_()

