from PyQt5 import QtWidgets
from sys import argv
import random

class Options: # Use this to change the options
    def __init__(self):
        self.grid_size = (10, 10)
        self.window_size = (400, 400)
        # ^ Window Size (pixels)


class MainGame:
    def __init__(self):
        self.ui = Grid()
        self.set_slots()

        self.ui.init_ui()
        self.ui.show()

    def set_slots(self):
        for (x, y) in self.ui.board:
            print(x, y)
            self.ui.board[x, y].clicked.connect(lambda state, c=(x, y): self.clicked((x, y)))

    def clicked(self, coords):
        x, y = coords
        print("X:{} Y:{}".format(x, y))

    def game_over(self):
        print("DEAD")


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.options = Options()
        self.board = {}
        self.widgets = {}

        self.window_size = self.options.window_size
        self.grid_size = self.options.grid_size

        self.margin = (1, 0, 0, 0) # Top margin, Bottom margin, Left Margin, Right Margin
        self.borders = (0, 0)

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


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.font_size = "10"

    def set_font_size(self):
        self.font_size = ((self.height() + self.width())**1.3) * 0.1
        self.font_size = str(int(self.font_size))

    def set_hex(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.setStyleSheet("background-color:" + color)

    def set_rgb(self, color):
        hex = '#%02x%02x%02x' % (color)
        self.setStyleSheet("background-color:" + hex)

    def set_value(self, tochangeto):
        self.setText(str(tochangeto))


def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()

if __name__ == '__main__':
    main()