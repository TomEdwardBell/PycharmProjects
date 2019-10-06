from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv

Options = None


class Ui():
    def __init__(self, options):
        global Options
        Options = options
        self.board = Board()
        self.board.init_ui()

    def update(self, coord, state):
        x, y = coord
        self.board.board[x, y].display(state)


class Board(QtWidgets.QWidget):
    def __init__(self):
        super(Board, self).__init__()
        self.board = {}
        self.board_width = Options.board_width
        self.board_height = Options.board_height

        self.window_width, self.window_height = Options.window_size

        self.borders = (0, 0)


    def init_ui(self):
        windowx , windowy = self.window_width, self.window_height
        xcount , ycount = self.board_width, self.board_height
        borderx, bordery = self.borders

        self.resize(windowx, windowy)
        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y] = Coord(self)
                self.board[x, y].coordinates = [x, y]

                xloc = x*(windowx / xcount) + (borderx / 4)
                yloc = y*(windowy / ycount) + (bordery / 4)

                width = windowx/xcount - borderx/2
                height = windowy/ycount - bordery/2

                self.board[x, y].move(xloc, yloc)
                self.board[x, y].resize(width, height)
                self.board[x, y].display('empty')

        self.show()


class Coord(QtWidgets.QLabel):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.state = ""

    def set_hex(self, color):
        self.setStyleSheet("background-color:" + color)

    def set_rgb(self, color):
        hex = '#%02x%02x%02x' % (color)
        self.setStyleSheet("background-color:" + hex)

    def display(self, state):
        if state != self.state:
            self.state = state
            self.set_hex(Options.colors[state])
            QtGui.QGuiApplication.processEvents()


def make_board(options):
    global Options
    Options = options
    main()


def update(coord, state):
    global board
    board.board[coord].display(state)


def main():
    app = QtWidgets.QApplication(argv)
    app.exec_()


if __name__ == '__main__':
    main()