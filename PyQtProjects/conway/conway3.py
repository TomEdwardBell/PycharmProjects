import random
from sys import argv
from PySide2 import QtCore, QtGui, QtWidgets
import time


class Simulation(QtWidgets.QMainWindow):
    def __init__(self):
        super(Simulation, self).__init__()
        p = .5
        self.actives = []
        self.die_list = []
        self.add_list = []

        self.randomise(-10, -10, 10, 10, 0.3)

        self.min_x = -100
        self.max_x = 100
        self.min_y = -100
        self.max_y = 100
        self.setStyleSheet('background-color: #FFFFFF;')
        self.resize(1000, 1000)
        self.show()

        while True:
            self.tick()
            self.repaint()

    def randomise(self, x1, y1, x2, y2, p):
        self.die_list = []
        self.add_list = []
        for x in range(x1, x2):
            for y in range(y1, y2):
                if random.random() < p:
                    self.actives.append((x, y))


    def check(self, x, y):
        live_count = 0
        nears = [(dx + x, dy + y) for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),(1, -1), (1, 0), (1, 1)]]
        for (nx, ny) in nears:
            if (nx, ny) in self.actives:
                live_count += 1

        if (x, y) in self.actives:
            if live_count != 2 and live_count != 3:
                self.die_list.append((x, y))
        else:
            if live_count == 3:
                self.add_list.append((x, y))

    def tick(self):
        print('Tick Started')
        checks = self.what_to_check()
        print('We Know what to check')
        for (cx, cy) in checks:
            self.check(cx, cy)
        print('We\'ve Checked them')
        for die in self.die_list:
            self.actives.remove(die)
        print('Baddies killed')
        for add in self.add_list:
            self.actives.append(add)
        print('Goodies added')
        self.die_list = []
        self.add_list = []
        print('Lists Reset')

    def what_to_check(self):
        checks = self.actives.copy()
        for (ax, ay) in self.actives:
            nears = [(dx + ax, dy + ay) for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1),(1, -1), (1, 0), (1, 1)]]
            for (nx, ny) in nears:
                if (nx, ny) not in checks:
                    checks.append((nx, ny))
        return checks

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QColor(0, 0, 0))
        qp.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0)))

        maxx = self.max_x
        minx = self.min_x
        maxy = self.max_y
        miny = self.min_y

        sw = self.width() / (maxx - minx)
        sh = self.height() / (maxy - miny)

        offsetx = sw*minx
        offsety = sh*miny

        for (ax, ay) in self.actives:
            qp.drawRect(int(ax * sw - offsetx), int(ay * sh - offsety), int(sw), int(sh))

        qp.end()

    def update(self):
        c = self.children()
        for child in c[1:]:
            child.setParent(None)
            child.destroy()
            child.hide()
        c = []

        maxx = self.max_x
        minx = self.min_x
        maxy = self.max_y
        miny = self.min_y

        sw = self.width() / (maxx - minx)
        sh = self.height() / (maxy - miny)

        self.widgets = []
        for (ax, ay) in self.actives:
            self.widgets.append(QtWidgets.QLabel(self))
            self.widgets[-1].setGeometry(int(ax * sw - sw*minx), int(ay * sh - sh*miny), int(sw), int(sh))
            self.widgets[-1].setStyleSheet('background-color: black')
            self.widgets[-1].hide()


class Run():
    def __init__(self):
        self.s = Simulation()


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    r = Run()
    app.exec_()

