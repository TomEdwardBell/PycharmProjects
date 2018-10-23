from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv
import random
import time


class Options:
    def __init__(self):
        self.window_size = (800, 800)
        # ^ Window size
        #   Pixels

        self.visual_size = 80
        # ^ Size of the "visuals" that appear
        #   As a percentage of the width and height of each piece

        self.pieces = {
            "pawn": "♟",
            # "pawn": "♙",
            "knight": "♞",
            # "knight": "♘",
            "bishop": "♗",
            # "bishop_b": "♝",
            "rook": "♜",
            # "rook_w": "♖",
            "queen": "♛",
            # "queen_w": "♕",
            "king": "♚",
            # "king_w": "♔",
        }

        self.chessboardcolors = ["#a56f3a", "#f9e093"]
        self.teamcolors = {"b": "#000000", "w": "#FFFFFF"}


class MainGame:
    def __init__(self):
        print("Game Initialising...")

        self.options = Options()

        self.ui = Grid()
        self.mouse_mode = "normal"
        self.ui.show()
        print("Game Loaded")

        self.ui.keyPressEvent = self.keyPressEvent
        # ^^^ keyPressEvent mussed be defined in the UI
        # ^^^ So I defined it here and then just added it to the UI

        self.thingo = Visual(self.ui)
        self.thingo.show()
        self.thingo.goto((4,4))

        self.thinga = Visual(self.ui)
        self.thinga.show()
        self.thinga.goto((3,3))

        self.testp = Piece(self.ui, "b", "queen")
        self.testp.goto((2,2))

        self.thinga.clicked.connect(self.thinga_click)
        self.thingo.clicked.connect(self.thingo_click)



    def thingo_click(self):
        self.testp.goto_smooth(self.thingo.chessboard_pos)
        self.thingo.goto_smooth((random.randint(0, 7), random.randint(0, 7)))

    def thinga_click(self):
        self.testp.goto_smooth(self.thinga.chessboard_pos)
        self.thinga.goto_smooth((random.randint(0, 7), random.randint(0, 7)))


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F:
            self.testp.goto_smooth(self.thingo.chessboard_pos)
            self.thingo.goto_smooth((random.randint(0, 7), random.randint(0, 7)))


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.options = Options()
        self.window_size = self.options.window_size
        self.chessboard = {}

        class Widgets:
            pass

        self.widgets = Widgets()

        self.init_ui()

    def init_ui(self):
        boardx = self.window_size[0]
        boardy = self.window_size[1]
        margintop = 0
        borderx = 0
        bordery = 0
        xcount = 8
        ycount = 8

        self.setStyleSheet("background-color: #222222")

        self.resize((boardx + borderx * (xcount + 1)), (boardy + bordery * (ycount + 1)) + margintop)
        for x in range(xcount):
            for y in range(ycount):
                self.chessboard[x, y] = Coord(self)
                self.chessboard[x, y].coordinates = [x, y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x * xpercoord + (x + 1) * borderx)
                yloc = (y * ypercoord + (y + 1) * bordery + margintop)
                self.chessboard[x, y].move(xloc, yloc)
                self.chessboard[x, y].resize(boardx / xcount, boardy / ycount)

                if (x + y) % 2 == 0:
                    color = self.options.chessboardcolors[0]
                    self.chessboard[x, y].set_color(color)
                else:

                    color = self.options.chessboardcolors[1]
                    self.chessboard[x, y].set_color(color)


class Visual(QtWidgets.QPushButton):
    def __init__(self, ui):
        super(Visual, self).__init__(ui)
        self.ui = ui
        size = 0  # Percentage from 0 to 100, based off percentage of width / height compared to parent

        self.chessboard_pos = (0, 0)

        self.options = Options()

        self.setStyleSheet(''' QWidget
        {
        background-color: rgba(0,255,0, 160);
        }

        ''')

        self.show()

    def goto(self, coord):
        self.chessboard_pos = coord

        corner = self.ui.chessboard[coord].pos()
        self.move(corner)

        self.do_resize()

        mini_border_w = self.ui.chessboard[0, 0].width() * (1 - (self.options.visual_size / 100)) / 2
        mini_border_h = self.ui.chessboard[0, 0].height() * (1 - (self.options.visual_size / 100)) / 2
        self.move(corner.x() + mini_border_w, corner.y() + mini_border_h)

    def do_resize(self):
        width = self.ui.chessboard[0, 0].width()
        width = width * (self.options.visual_size / 100)

        height = self.ui.chessboard[0, 0].height()
        height = height * (self.options.visual_size / 100)
        self.resize(width, height)

    def goto_smooth(self, new_coord):
        self.chessboard_pos = new_coord

        old_pos = (self.pos())
        old_pos = old_pos.x(), old_pos.y()

        new_pos_corner = self.ui.chessboard[new_coord].pos()

        mini_border_w = self.ui.chessboard[0, 0].width() * (1 - (self.options.visual_size / 100)) / 2
        mini_border_h = self.ui.chessboard[0, 0].height() * (1 - (self.options.visual_size / 100)) / 2

        new_pos = (new_pos_corner.x() + mini_border_w, new_pos_corner.y() + mini_border_h)

        frames = 20
        npx, npy = new_pos
        opx, opy = old_pos
        for i in range(frames):
            f = (i + 1) / (frames)
            s = 1 - f
            frame_pos = (int(s*opx+ f*npx), int(s*opy + f*npy))
            self.move(frame_pos[0], frame_pos[1])

            time.sleep(0.02)
            QtGui.QGuiApplication.processEvents()


class Piece(Visual):
    def __init__(self, ui, team, piece_type):
        super(Piece, self).__init__(ui)

        self.team = team
        self.piece_type = piece_type
        self.piece_char = self.options.pieces[piece_type]
        self.piece_color = self.options.teamcolors[team]

        self.setText(self.piece_char)

        self.setStyleSheet(''' QWidget
        {
        background-color: rgba(0,0 ,0, 0);
        color:''' + self.piece_color + ''';
        font-size: 50pt;
        }


        ''')

        self.goto((0, 0))


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.piece = " "
        self.font_size = "10"

    def set_color(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)

        self.setStyleSheet("background-color:" + color + ";font-size: 50pt; font-family: \"Arial\"")

    def set_value(self, tochangeto):
        self.setText(tochangeto)


def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
