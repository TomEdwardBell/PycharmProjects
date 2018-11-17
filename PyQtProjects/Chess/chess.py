from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv
import random
import time


class Options:
    def __init__(self):
        self.window_size = (800, 800)
        # ^ Window size
        #   Pixels

        self.visual_size = 85
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
        # ^ Colours of the checkeboard background of the game

        self.teamcolors = ["#FFFFFF", "#00000"]
        # ^ colours of the pieces in the game

        self.pixels_per_second = 100
        # ^ Speed at which the pieces in the game move


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

        self.pieces = [[],[]]

        self.place_board()
    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F:
            self.testp.goto_smooth(self.thingo.chessboard_pos)
            self.thingo.goto_smooth((random.randint(0, 7), random.randint(0, 7)))

    def place_board(self):
        #  White Pawns
        for i in range(8):
            self.pieces[0].append(None)
            self.pieces[0][i] = Piece(self.ui, 0, "pawn")
            self.pieces[0][i].show()
            self.pieces[0][i].goto((i, 1))


        #  Other white row

        #  Black Pawns
        for i in range(8):
            self.pieces[1].append(Piece(self.ui, 1, "pawn"))
            self.pieces[1][i].show()
            self.pieces[1][i].goto((i, 6))
        #  Other black row

        for piece in self.pieces[0]:
            piece.set_clickable(True)


class Grid(QtWidgets.QMdiSubWindow):
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


class Visual(QtWidgets.QToolButton):
    def __init__(self, ui):
        super(Visual, self).__init__(ui)

        self.ui = ui
        size = 0  # Percentage from 0 to 100, based off percentage of width / height compared to parent

        self.chessboard_pos = (0, 0)
        self.pixel_pos = (0, 0)


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
        self.pixel_pos = (corner.x(), corner.y())

        self.do_resize()

        mini_border_w = self.ui.chessboard[0, 0].width() * (1 - (self.options.visual_size / 100)) / 2
        mini_border_h = self.ui.chessboard[0, 0].height() * (1 - (self.options.visual_size / 100)) / 2
        newx = int(corner.x() + mini_border_w)
        newy = int(corner.y() + mini_border_h)
        self.move(newx, newy)
        self.pixel_pos = (newx, newy)

    def do_resize(self):
        width = self.ui.chessboard[0, 0].width()
        width = int(width * (self.options.visual_size / 100))

        height = self.ui.chessboard[0, 0].height()
        height = int(height * (self.options.visual_size / 100))
        self.resize(width, height)


    def goto_smooth(self, new_coord):
        self.chessboard_pos = new_coord

        old_pos = self.pixel_pos

        new_pos_corner = self.ui.chessboard[new_coord].pos()

        mini_border_w = self.ui.chessboard[0, 0].width() * (1 - (self.options.visual_size / 100)) / 2
        mini_border_h = self.ui.chessboard[0, 0].height() * (1 - (self.options.visual_size / 100)) / 2

        new_pos = new_pos_corner.x() + mini_border_w, new_pos_corner.y() + mini_border_h
        self.pixel_pos = new_pos

        pps = int(self.options.pixels_per_second)
        # ^ Speed of the visual, in pixels per second

        npx, npy = new_pos
        opx, opy = old_pos

        distance = ((npx - opx)**2+(npy - opy)**2) **0.5

        travel_time = int(distance) / pps

        self.frame = QtWidgets.QFrame(self)
        self.frame.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.frame.setGeometry(150, 30, 100, 100)

        self.move_anim =  QtCore.QPropertyAnimation(self, b"geometry")
        self.move_anim.setDuration(int(travel_time*1000))
        self.move_anim.setStartValue(QtCore.QRect(opx, opy, self.width(), self.height()))
        self.move_anim.setEndValue(QtCore.QRect(npx, npy, self.width(), self.height()))
        self.move_anim.start()

        QtGui.QGuiApplication.processEvents()


class Piece(Visual):
    def __init__(self, ui, team, piece_type):
        super(Piece, self).__init__(ui)

        self.team = team
        self.piece_type = piece_type
        self.piece_char = self.options.pieces[piece_type]
        self.piece_color = self.options.teamcolors[team]

        self.ui = ui
        self.setText(self.piece_char)

        self.setStyleSheet(''' QWidget
        {
        background-color: rgba(0, 0 ,0, 0);
        color:''' + self.piece_color + ''';
        font-size: 50pt;
        }
        ''')

        self.goto((0, 0))

        self.is_movable = False
        self.is_clickable = False
        self.piecemovers = []

    def movable(self):
        self.is_movable = not self.is_movable
        self.piecemovers.append(PieceMover(self.ui, self, (self.chessboard_pos[0], self.chessboard_pos[1] + 1)))

    def set_clickable(self, bol):
        print("Clickable:", self.is_clickable)
        if bol:
            self.setStyleSheet('''QWidget
            {
            background-color: rgba(200, 0 ,200, 0.8);
            color:''' + self.piece_color + ''';
            font-size: 50pt;
            }
            ''')
            self.clicked.connect(self.movable)
        elif not bol:
            self.setStyleSheet('''   
                QWidget
                {
                background-color: rgba(0, 0, 0, 0);
                color: ''' + self.piece_color + ''';
                font-size: 50pt;
                }
                ''')
            self.clicked.disconnect()

    def nothing(self):
        pass


class PieceMover(Visual):
    def __init__(self, ui, piece, pos):
        super(PieceMover, self).__init__(ui)
        self.piece = piece
        self.clicked.connect(self.move_piece)
        self.goto(piece.chessboard_pos)
        self.goto_smooth(pos)
        self.piece.set_clickable(False)



    def move_piece(self):
        self.piece.goto_smooth(self.chessboard_pos)
        self.setGeometry(0, 0, 1, 1)
        for mover in self.piece.piecemovers:
            mover.setGeometry(0, 0, 1, 1)


class Coord(QtWidgets.QLabel):
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
