from PyQt5 import QtWidgets, QtTest, QtGui
import sys
import random

class Options:
    def __init__(self):
        self.window_size = (1920, 960)
        # ^ Window size
        #   Pixels

        self.grid_size = (4, 2)


class MainGame:
    def __init__(self):
        self.ui = Grid()
        self.ui.show()
        self.options = Options()


        maxx, maxy = self.options.grid_size
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[1]):
                self.ui.board[x, y].set_rgba((255,0,0,1))
        while True:
            x, y = random.randint(0,maxx - 1), random.randint(0,maxy - 1)
            color = list(self.ui.board[x, y].color)
            change = random.choice([1,-1])
            c = random.randint(0,2)
            color[c] = color[c] + change
            if color[c] > 255:
                color[c] = 255
            elif color[c] < 0:
                color[c] = 0
            self.ui.board[x, y].set_rgba(tuple(color))
            QtGui.QGuiApplication.processEvents()




class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.options = Options()
        self.board = {}
        self.widgets = {}

        self.window_size = self.options.window_size
        self.grid_size = self.options.grid_size

        self.margin = (0, 0, 0, 0) # Top margin, Bottom margin, Left Margin, Right Margin
        self.borders = (0, 0)

        self.init_ui()

    def init_ui(self):
        boardx , boardy = self.window_size
        xcount , ycount = self.grid_size
        borderx, bordery = self.borders

        self.resize(boardx + self.margin[2] + self.margin[3], boardy + self.margin[0] + self.margin[1])
        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y] = Coord(self)
                self.board[x, y].coordinates = [x, y]

                xloc = x*(boardx / xcount) + self.margin[2] + (borderx / 4)
                yloc = y*(boardy / ycount) + self.margin[0] + (bordery / 4)

                width = boardx/xcount - borderx/2
                height = boardy/ycount - bordery/2

                self.board[x, y].move(xloc, yloc)
                self.board[x, y].resize(width, height)

                self.board[x, y].set_font_size()


class Coord(QtWidgets.QLabel):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.font_size = "10"
        self.color = ()

        self.show()

    def set_font_size(self):
        self.font_size = ((self.height() + self.width())**1.3) * 0.1
        self.font_size = str(int(self.font_size))

    def set_rgba(self, color):
        self.color = color
        self.setStyleSheet('''
        QWidget{
            background-color:rgba'''+str(color)+''';
            }
        ''')

    def set_value(self, tochangeto):
        self.setText(str(tochangeto))


def main():
    app = QtWidgets.QApplication(sys.argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
