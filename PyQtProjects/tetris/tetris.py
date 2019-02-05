from PyQt5 import QtWidgets, QtCore, QtGui
from sys import argv
import random


class Options: # Use this to change the options
    def __init__(self):
        self.grid_size = (10, 20)
        self.window_size = (360, 720)
        # ^ Window Size (pixels)

        self.margin = (0,0,0,0)

        self.borders = (0, 0)


class MainGame:
    def __init__(self):
        self.options = Options()

        self.window = Window(self.options.window_size, self.options.margin)

        self.dead_pieces = self.make_dead_pieces()

        self.current_shape = ()
        self.window.show()
        self.new_shape()

        self.window.keyPressEvent = self.keyPressEvent
        # ^^^ keyPressEvent mussed be defined in the UI
        # ^^^ So I defined it here and then just added it to the UI

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_S:
            self.current_shape.move_down()
        if e.key() == QtCore.Qt.Key_A:
            self.current_shape.move_left()
        if e.key() == QtCore.Qt.Key_D:
            self.current_shape.move_right()
        if e.key() == QtCore.Qt.Key_W:
            self.current_shape.rotate()

    def make_dead_pieces(self):
        dead = {}
        w, h = self.options.grid_size
        for i in range(w):
            for j in range(h):
                dead[i, j] = 0
        return dead

    def kill_shape(self):
        self.current_shape.moving = False
        for piece in self.current_shape:
            x, y = piece.board_pos
            self.dead_pieces[x, y] = piece
        del self.current_shape

        self.new_shape()

    def new_shape(self):
        self.current_shape = Shape(self.window, self)

    def check_rows(self):
        for y in range(self.options.grid_size[1]):
            full = True
            for x in range(self.options.grid_size[0]):
                if self.dead_pieces[x, y] == 0:
                    full = False
            if full:
                for x in range(self.options.grid_size[0]):
                    self.dead_pieces[x, y].hide()
                    del self.dead_pieces[x, y]
                    self.dead_pieces[x, y] = 0

                for y2 in range(y, -1, -1):
                    print(y2)
                    for x2 in range(self.options.grid_size[0]):
                        print(x2, y2)
                        print(self.dead_pieces[x2, y2])
                        if self.dead_pieces[x2, y2] != 0:
                            self.dead_pieces[x2, y2].move_down()
                            self.dead_pieces[x2, y2 + 1] = self.dead_pieces[x2, y2]
                            self.dead_pieces[x2, y2] = 0


class Window(QtWidgets.QMainWindow):  # The actual window of the program
    def __init__(self, window_size, margin):
        super(Window, self).__init__()
        self.resize(window_size[0], window_size[1])
        self.show()



class GridPiece(QtWidgets.QPushButton):  # One square piece on the board
    def __init__(self, parent, window):
        super(GridPiece, self).__init__(window)
        self.options = Options()
        self.color = '#008800'
        self.board_pos = (5, 3)
        self.window_pos = (0, 0)

        r, g, b = parent.color
        self.setStyleSheet('background-color: rgba({},{} ,{},255);'.format(r, g, b))
        self.do_resize()
        self.show()

    def set_pos(self, x, y):
        self.board_pos = (x, y)
        self.do_resize()

    def do_resize(self):
        x, y = self.board_pos
        if not(x < 0 or y < 0 or x >= self.options.grid_size[0] or y >= self.options.grid_size[1]):
            boardx , boardy = self.options.window_size
            xcount , ycount = self.options.grid_size
            borderx, bordery = self.options.borders

            xloc = int(x * (boardx / xcount) + self.options.margin[2] + (borderx / 4))
            yloc = int(y * (boardy / ycount) + self.options.margin[0] + (bordery / 4))

            width = boardx / xcount - borderx / 2
            height = boardy / ycount - bordery / 2

            self.move(xloc, yloc)
            self.resize(width, height)


    def move_down(self):
        x, y = self.board_pos
        y += 1
        self.set_pos(x, y)
        self.do_resize()


    def move_left(self):
        x, y = self.board_pos
        x += -1
        self.set_pos(x, y)
        self.do_resize()


    def move_right(self):
        x, y = self.board_pos
        x += 1
        self.set_pos(x, y)
        self.do_resize()


class Shape(list):
    # The shape that's currently falling
    # Only one of these should exist at a time
    # When the shape stops moving, all of its pieces are moved to the dead pieces array
    # It is a list off all of the pieces that are falling
    def __init__(self, window, parent):
        super(Shape, self).__init__()
        self.moving = True
        self.window = window
        self.parent = parent
        self.options = Options()

        self.color = self.get_color()

        self.center_loc = (int((self.options.grid_size[0] + 1) / 2), 0)
        self.rotation = 0

        shapes = [
            [[(0, 0), (0, 1), (0, 2), (1, 2)],
             [(0, 1), (0, 0), (1, 0), (2, 0)],
             [(0, 0), (1, 0), (1, 1), (1, 2)],
             [(0, 1), (1, 1), (2, 1), (2, 0)]],
            # L Piece

            [[(1, 0), (1, 1), (1, 2), (0, 2)],
             [(1, 0), (1, 1), (1, 2), (0, 2)],
             [(1, 0), (1, 1), (1, 2), (0, 2)],
             [(1, 0), (1, 1), (1, 2), (0, 2)],
             [(1, 0), (1, 1), (1, 2), (0, 2)],],
            # Reverse L Piece

            [[(0, 0), (1, 0), (2, 0), (3, 0)],
             [(0, 0), (0, 1), (0, 2), (0, 3)],
             [(0, 0), (1, 0), (2, 0), (3, 0)],
             [(0, 0), (0, 1), (0, 2), (0, 3)]],
            # Line Piece

            [[(0, 0), (0, 1), (1, 1), (1, 0)],
             [(0, 0), (0, 1), (1, 1), (1, 0)],
             [(0, 0), (0, 1), (1, 1), (1, 0)],
             [(0, 0), (0, 1), (1, 1), (1, 0)]],
            # Block Piece

            [[(0, 0), (1, 0), (1, 1), (2, 1)],
             [(0, 0), (1, 0), (1, 1), (2, 1)],
             [(0, 0), (1, 0), (1, 1), (2, 1)],
             [(0, 0), (1, 0), (1, 1), (2, 1)],],
            # Z Piece

            [[(0, 1), (1, 1), (1, 0), (2, 0)],
             [(0, 1), (1, 1), (1, 0), (2, 0)],
             [(0, 1), (1, 1), (1, 0), (2, 0)],
             [(0, 1), (1, 1), (1, 0), (2, 0)]],
             # S Piece

            [[(0, 0), (1, 0), (1, 1), (2, 0)],
             [(0, 0), (1, 0), (1, 1), (0, 2)],
             [(0, 1), (1, 1), (1, 0), (1, 2)],
             [(1, 0), (1, 1), (0, 1), (1, 2)]]
            # T Piece
            ]

        shlapes = [[[(0,0), (1,0), (2, 0), (3, 0), (4, 0)], [(0,0)],[(0,0)],[(0,0)]]]

        shapjes = [
            [  # L Piece
                [],  # . L   L piece no rotation
                [],  # |▔▔ L piece rotate clockwise 90*
                [],  # . ┓   L piece rotate 180*
                []],  # |▁▁ L piece rotate clockwise 270*

            [  # Reverse L Piece
                [],  # L     Reserve L piece no rotation
                [],  # |▔▔ Reserve L piece rotate clockwise 90*
                [],  # ┓     Reserve L piece rotate 180*
                []],  # |▁▁ Reserve L piece rotate clockwise 270*

            [  # Block Piece
                [(0, 0), (0, 1), (1, 0), (1, 1)],  # ▉ no rotation
                [(0, 0), (0, 1), (1, 0), (1, 1)],  # ▉ no rotation
                [(0, 0), (0, 1), (1, 0), (1, 1)],  # ▉ no rotation
                [(0, 0), (0, 1), (1, 0), (1, 1)]], # ▉ no rotation

            [  # T Piece
                [(-1, 0), (0, 0), (0, 1), (1, 0)],  # T
                [(0, -1), (0, 0), (0, 1), (1, 0)],  # |-
                [(0, 0)],  # -|
                [0]]  # _|_
        ]


        self.shape_info = shapes[random.randint(0, len(shapes) -1)]
        c = 0
        for x, y in self.shape_info[self.rotation]:
            self.append(GridPiece(self, self.window))
            self[c].set_pos(self.center_loc[0] + x, self.center_loc[1] + y)
            c += 1

    def rotate(self):

        can_rotate = True
        cx, cy = self.center_loc
        for x, y in self.shape_info[self.rotation]:
            if (cx + x, cy + y) in self.parent.dead_pieces:
                if self.parent.dead_pieces[cx + x, cy + y] != 0:
                    can_rotate = False
            else: can_rotate = False

        if can_rotate:
            self.rotation = (self.rotation + 1) % 4
            for p in range(len(self)):
                self[0].hide()
                o = self[0]
                print(p,"O1")
                self.pop(0)
                print(p,"O2")
                del o
                print(p,"O3")
            c = 0
            print(self)
            for lx, ly in self.shape_info[self.rotation]:
                print("C1")
                x, y = cx + lx, cy + ly
                self.append(GridPiece(self, self.window))
                print("C2")
                self[c].set_pos(x, y)
                c += 1

    def get_color(self):
        rgb = [255, 0, random.randint(0, 255)]
        random.shuffle(rgb)

        return rgb[0], rgb[1], rgb[2]


    def die(self):
        for piece in self:
            self.parent.dead_pieces[piece.board_pos] = piece
        self.parent.new_shape()
        self.parent.check_rows()

    def move_down(self):
        if self.moving:
            for piece in self:
                x, y = piece.board_pos
                if y >= self.options.grid_size[1] - 1:
                    self.moving = False
                elif self.parent.dead_pieces[x, y + 1] != 0:
                    self.moving = False
            if self.moving:
                for piece in self:
                    piece.move_down()
                    cx, cy = self.center_loc
                self.center_loc = cx, cy + 1
            else:
                self.die()

    def move_left(self):
        if self.moving:
            can_move = True
            for piece in self:
                x, y = piece.board_pos
                if x <= 0:
                    can_move = False
                elif self.parent.dead_pieces[x - 1, y] != 0:
                    can_move = False

            if can_move and self.moving:
                for piece in self:
                    piece.move_left()

                cx, cy = self.center_loc
                self.center_loc = cx -1, cy


    def move_right(self):
        if self.moving:
            can_move = True
            for piece in self:
                x, y = piece.board_pos
                if x >= self.options.grid_size[0] - 1:
                    can_move = False
                elif self.parent.dead_pieces[x + 1, y] != 0:
                    can_move = False
            if can_move and self.moving:
                for piece in self:
                    piece.move_right()
                cx, cy = self.center_loc
                self.center_loc = cx + 1, cy

    def nothing(self): pass


def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()