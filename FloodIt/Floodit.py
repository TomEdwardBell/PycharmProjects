from PyQt5 import QtWidgets
from sys import argv
import random
from math import ceil


class Options:  # Use this to change the options
    def __init__(self):
        self.grid_size = (8, 8)
        self.window_size = (512, 512)
        # ^ Window Size (pixels)

        self.colors = ["#FFFFFF", "#004225", "#E8000D", "#0444A4", "#F9A602", "#D86B93", "#87794E"]

        # ^ All of the colors that could appear on the board


class MainGame:
    def __init__(self):
        self.options = Options()

        self.ui = Grid(self)

        self.ui.init_ui()
        self.color_pieces()
        self.click_color = "#000000"
        self.territory = [(0, 0)]

        self.ui.show()

    def color_pieces(self):
        for (x, y) in self.ui.board:
            color = random.choice(self.options.colors)
            self.ui.board[x, y].set_color(color)

    def color_click(self, new_color, coords):
        old_color = self.click_color
        new_ters = []


        for tcoord in self.territory:
            for near in self.get_locals(tcoord):
                if near not in self.territory:
                    if self.ui.board[near].color == new_color:
                        new_ters.append(near)

        self.territory = self.remove_duplicates(self.territory)

        for newcoord in new_ters:
            self.territory.append(newcoord)
            self.color_click(new_color, newcoord)

        for tcoord in self.territory:
            self.ui.board[tcoord].set_color(new_color)


    def remove_duplicates(self, values):
        output = []
        seen = set()
        for value in values:
            # If value has not been encountered yet,
            # ... add it to both list and set.
            if value not in seen:
                output.append(value)
                seen.add(value)
        return output

    def get_locals(self, coords):  # Taken from my minesweeper code
        localcoords = []
        relative_locals = [[-1, 0], [0, -1], [0, 1], [1, 0]]

        for i in relative_locals:
            rel_x = i[0]
            rel_y = i[1]
            loc_x = coords[0] + rel_x
            loc_y = coords[1] + rel_y
            if -1 not in [loc_x, loc_y] and loc_x < self.options.grid_size[0] and loc_y < self.options.grid_size[1]:
                localcoords.append((loc_x, loc_y))
        return (localcoords)

    def set_click_color(self, color):
        self.click_color = color

    def game_over(self):
        print("DEAD")


class Grid(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super(Grid, self).__init__()
        self.options = Options()
        self.parent = parent
        self.board = {}
        self.widgets = self.Widgets()

        self.window_size = self.options.window_size
        self.grid_size = self.options.grid_size

        self.margin = (30, int(self.window_size[0] / len(self.options.colors)), 0, 0)
        # ^ Top margin, Bottom margin, Left Margin, Right Margin
        self.borders = (0, 0)

    class Widgets:
        pass

    def init_ui(self):
        boardx, boardy = self.window_size
        xcount, ycount = self.grid_size
        borderx, bordery = self.borders

        self.resize(boardx + self.margin[2] + self.margin[3], boardy + self.margin[0] + self.margin[1])
        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y] = Coord(self)
                self.board[x, y].coordinates = [x, y]

                xloc = x * (boardx / xcount) + self.margin[2] + (borderx / 4)
                yloc = y * (boardy / ycount) + self.margin[0] + (bordery / 4)

                width = boardx / xcount - borderx / 2
                height = boardy / ycount - bordery / 2

                self.board[x, y].move(xloc, yloc)
                self.board[x, y].resize(width, height)

                self.board[x, y].set_font_size()

        self.place_color_selection_buttons()

    def place_color_selection_buttons(self):
        square_sizes = self.width() / len(self.options.colors)
        square_sizes = ceil(square_sizes)

        self.widgets.colorblocks = []
        for color in range(len(self.options.colors)):
            self.widgets.colorblocks.append(QtWidgets.QPushButton(self))
            c = self.widgets.colorblocks[color]
            c.resize(square_sizes, square_sizes)
            newx = color * square_sizes

            newy = self.height() - square_sizes
            c.move(newx, newy)

            c.setStyleSheet("background-color:" + self.options.colors[color])

            c.clicked.connect(lambda state, b=self.options.colors[color]: self.parent.color_click(b, (0,0)))


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.font_size = "10"

        self.color = "#000000"

    def set_font_size(self):
        self.font_size = ((self.height() + self.width()) ** 1.3) * 0.1
        self.font_size = str(int(self.font_size))

    def set_color(self, new_color):
        self.color = new_color

        self.setStyleSheet("background-color: " + new_color)


def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()