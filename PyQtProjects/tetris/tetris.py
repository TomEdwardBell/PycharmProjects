from PyQt5 import QtWidgets, QtCore, QtGui
from sys import argv
import random


class Options: # Use this to change the options
    def __init__(self):
        self.grid_size = (10, 20)
        self.window_size = (360, 720)
        # ^ Window Size (pixels)

        self.margin = (5,5,5,200)

        self.borders = (-5, -5)


class MainGame:
    def __init__(self):
        self.ui = Window()

        self.ui.init_ui()
        self.ui.show()

        self.timer_available = True
        self.new_shape = True
        self.shapes = []

        self.shapes.append(Shape(4, self.ui))

        self.main_loop()

    def main_loop(self):
        self.dead = False
        tick_count = 0
        while not self.dead:
            tick_count += 1
            if self.timer_available:
                self.timer_available = False
                tick_speed = 200
                timer = QtCore.QTimer()
                timer.timeout.connect(self.main_loop_timer_done)
                timer.start(tick_speed)
            QtGui.QGuiApplication.processEvents()

    def main_loop_timer_done(self):
        print("BANG")
        if self.shapes[-1].moving:
            self.shapes[-1].move((0,1))
        else:
            self.shapes.append(Shape(random.randint(0, 6), self.ui))

    def new_shape(self):
        self.shapes.append(Shape(3,self.ui))

    def clicked(self, coords):
        x, y = coords
        print("X:{} Y:{}".format(x, y))

    def game_over(self):
        print("DEAD")


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.options = Options()
        self.board = {}
        self.widgets = {}

        self.window_size = self.options.window_size
        self.grid_size = self.options.grid_size

        self.margin = self.options.margin # Top margin, Bottom margin, Left Margin, Right Margin
        self.borders = self.options.borders

    def init_ui(self):
        boardx , boardy = self.window_size
        xcount , ycount = self.grid_size
        borderx, bordery = self.borders

        self.resize(boardx + self.margin[2] + self.margin[3], boardy + self.margin[0] + self.margin[1])


    def place_coord(self, coord, coord_x, coord_y,):
        boardx , boardy = self.window_size
        xcount , ycount = self.grid_size
        borderx, bordery = self.borders

        xloc = coord_x*(boardx / xcount) + self.margin[2] + (borderx / 4)
        yloc = coord_y*(boardy / ycount) + self.margin[0] + (bordery / 4)
        width = boardx/xcount - borderx/2
        height = boardy/ycount - bordery/2
        coord.move(xloc, yloc)
        coord.resize(width, height)


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


class Shape:
    def __init__(self,shapenum,window):
        self.possible_shapes = self.get_shapes()
        self.shape_coords = [(0, 0)]
        self.base_pos = (5, 0)
        self.moving = True

        self.shape = []
        self.shape_num = shapenum
        self.shape_coords = self.possible_shapes[shapenum]
        self.window = window

        self.possible_colors = ["#FF0000","#00FF00","#0000FF","#FFFF00","#00FFFF","#FF00FF"]
        self.color = random.choice(self.possible_colors)

        self.create_shape()

    def create_shape(self):
        for shape_pos in self.shape_coords:
            self.shape.append(Coord(self.window))
            self.window.place_coord(self.shape[-1],shape_pos[0],shape_pos[1])
            self.shape[-1].set_hex(self.color)
            self.shape[-1].rel_pos = shape_pos

            self.shape[-1].show()
            print ("done")

    def move(self, direction):
        dir_x, dir_y = direction
        self.base_pos = (self.base_pos[0] + dir_x,  self.base_pos[1] + dir_y)
        for piece in self.shape:
            new_x = self.base_pos[0] + piece.rel_pos[0]
            new_y = self.base_pos[1] + piece.rel_pos[1]
            self.window.place_coord(piece,new_x, new_y)


    def get_shapes(self):
        z_shape = [
            [(-1,-1),(0,-1),(0,0),(1,0)],
            [(1,-1),(1,0),(0,0),(0,1)],
            [(-1,0),(0,0),(0,1),(1,1)],
            [(),(),(),()]
        ]

        all_shapes = [z_shape]

        return(all_shapes)


def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()