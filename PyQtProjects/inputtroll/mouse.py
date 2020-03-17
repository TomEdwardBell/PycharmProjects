from PySide2 import QtGui, QtCore, QtWidgets
from sys import argv
import random


class FallingMouse(QtWidgets.QWidget):
    def __init__(self):
        super(FallingMouse, self).__init__()
        self.show()
        self.t = QtCore.QTimer(self)
        self.t.setInterval(1)
        self.t.timeout.connect(self.keymove)
        self.t.start()
        self.ay = 0.004
        self.e = 0.8
        self.ax = 0.00
        self.vy = 45
        self.vx = 0
        self.x = QtGui.QCursor.pos().x()
        self.y = QtGui.QCursor.pos().y()

    def keymove(self):
        w = QtWidgets.QApplication.desktop().width()
        h = QtWidgets.QApplication.desktop().height()

        self.vx = self.vx + self.ax
        self.vy = self.vy + self.ay

        nx = self.x + self.vx
        ny = self.y + self.vy

        if ny >= h:
            ny = h
            self.vy = - self.vy * self.e

        if ny < 0:
            ny = 0
            self.vy = - self.vy * self.e

        if nx >= w:
            nx = w
            self.vx = - self.vx * self.e

        if nx < 0:
            nx = 0
            self.vx = - self.vx * self.e

        self.x = nx
        self.y = ny

        QtGui.QCursor.setPos(int(self.x), int(self.y))


class ShakeyMouse(QtWidgets.QWidget):
    def __init__(self):
        super(ShakeyMouse, self).__init__()
        self.t = QtCore.QTimer(self)
        self.t.setInterval(1)
        self.t.timeout.connect(self.keymove)
        self.t.start()


    def keymove(self):
        w = QtWidgets.QApplication.desktop().width()
        h = QtWidgets.QApplication.desktop().height()
        x = QtGui.QCursor.pos().x()
        y = QtGui.QCursor.pos().y()
        dx = random.randint(-3, 3)
        dy = random.randint(-3, 3)
        QtGui.QCursor.setPos((x + dx) % w, (y + dy) % h)


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    c = FallingMouse()
    #s = ShakeyMouse()
    app.exec_()