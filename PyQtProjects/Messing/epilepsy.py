from PyQt5 import QtWidgets, QtTest, QtGui
import sys
import random


class Coord:
    def __init__(self, game):
        self.btn = QtWidgets.QPushButton(game)

    def setcolor(self, r,g,b):
        color = '#%02x%02x%02x' % (r, g ,b)
        self.btn.setStyleSheet("background-color:"+color)

class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.initUI()

    def initUI(self):
        boardx = 800
        boardy = 800
        border = 0
        xcount = 20
        ycount = 20
        self.resize(boardx+border*(xcount+1), boardy+border*(ycount+1))
        board = {}

        for x in range(xcount):
            for y in range(ycount):
                board[x, y] = Coord(self)
                board[x, y].coordinates = [x,y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*border)
                yloc = (y*ypercoord + (y+1)*border)
                board[x, y].btn.move(xloc, yloc)
                board[x, y].btn.resize(boardx/xcount, boardy/ycount)
                #board[x, y].btn.setText(str(x) + "," + str(y))
        self.show()
        xc = xcount - 1
        yc = ycount - 1
        while True:
            x = random.randint(0,xc)
            y = random.randint(0,yc)
            r = 0
            g = random.choice([0,0,0,255])
            b = 0

            board[x, y].setcolor(r, g, b)
            QtGui.QGuiApplication.processEvents()


    def printcoord(self, coord):
        print(coord.coordinates)

def main():
    app = QtWidgets.QApplication(sys.argv)
    game = Grid()
    game.show()
    app.exec_()


if __name__ == '__main__':
    main()
