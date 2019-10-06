from PyQt5 import QtWidgets
from sys import argv
import random

class Options: # Use this to change the options
    grid_size = (10, 10)
    window_size = (400, 400)
        # ^ Window Size (pixels)


class MainGame:
    def __init__(self):
        self.ui = Grid()
        self.set_slots()

        self.ui.init_ui()
        self.ui.show()

    def set_slots(self):
        for (x, y) in self.ui.board:
            self.ui.board[x, y].clicked.connect(lambda state, c=(x, y): self.clicked((x, y)))

    def clicked(self, coords):
        x, y = coords
        print("X:{} Y:{}".format(x, y))

    def game_over(self):
        print("DEAD")


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.board = {}
        self.widgets = {}

        self.window_size = Options.window_size
        self.grid_size = Options.grid_size

        self.margin = (0, 0, 0, 0) # Top margin, Bottom margin, Left Margin, Right Margin
        self.borders = (0, 0)


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