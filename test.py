from PySide2 import QtWidgets, QtCore, QtGui
from sys import argv
import time


class Win(QtWidgets.QMainWindow):
    def __init__(self):
        super(Win, self).__init__()
        self.thang = Thang(self)
        self.show()

class Thang(QtWidgets.QToolButton):
    def __init__(self):
        super(Thang, self).__init__()
        self.resize(150, 150)
        self.show()

        self.clicked.connect(self.wide)

    def wide(self):
        self.resize(self.width() * 1.1, self.height())


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)

        colors = ['#FF0000', '#00FF00', '#0000FF']
        w = int(self.width() / len(colors))
        for c in range(len(colors)):
            col = QtGui.QColor(colors[c])
            qp.setPen(col)

            qp.setBrush(col)
            qp.setPen(col)

            qp.setBrush(QtGui.QColor(col))
            qp.drawRect(c*w, 0, w, 140)

        qp.end()


def main():
    app = QtWidgets.QApplication(argv)
    thang = Thang()
    app.exec_()

if __name__ == '__main__':
    main()