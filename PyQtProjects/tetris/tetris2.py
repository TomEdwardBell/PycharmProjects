from PySide2 import QtGui, QtCore, QtWidgets
from sys import argv
import random
import time


class FallingPiece:
    pass


class DeadPiece:
    pass


class BlankSpace:
    pass


class UI(QtWidgets.QMainWindow):
    def __init__(self, board):
        super(UI, self).__init__()
        self.resize(1000, 2000)
        self.board = board
        self.rows_to_hide = 4

        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.do_tick)
        self.timer.start(100)

    def do_tick(self):
        self.board.tick()
        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            self.board.rotate()
        elif e.key() == QtCore.Qt.Key_D:
            self.board.move_right()
        elif e.key() == QtCore.Qt.Key_A:
            self.board.move_left()
        elif e.key() == QtCore.Qt.Key_S:
            self.board.scan_down()

    def paintEvent(self, e):
        rth = self.rows_to_hide
        pw = self.width() / self.board.w
        ph = self.height() / (self.board.h - rth)

        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor('#000000'))
        dead_brush = QtGui.QColor('#00FF22')
        active_brush = QtGui.QColor('#FF0000')

        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(pen)

        for y in range(self.board.h):
            for x in range(self.board.w):
                if self.board[x][y] == FallingPiece:
                    qp.setBrush(active_brush)
                    qp.drawRect(int(x * pw), int((y - rth) * ph), int(pw), int(ph))
                elif self.board[x][y] == DeadPiece:
                    qp.setBrush(dead_brush)
                    qp.drawRect(int(x * pw), int((y - rth) * ph), int(pw), int(ph))

        if self.board.dead:
            print('deathtext')
            qp.setPen(QtGui.QPen(QtGui.QColor('#FF0000')))
            font = QtGui.QFont()
            font.setPointSize(100)
            font.setFamily('papyrus')
            qp.setFont(font)
            qp.drawText(0, 0, self.width(), self.height(), 0, 'YOU\nARE\nDEAD\nRIP')
        qp.end()


class Board(list):
    def __init__(self, w, h):
        super(Board, self).__init__()

        self.w = w
        self.h = h

        self.piece_center = (0, 0)
        self.piece_index = 0
        self.piece_rotation = 0
        self.dead = False

        for x in range(w):
            self.append([BlankSpace for y in range(h)])


        self.pieces = [
            [ # T
                [(-1, 0), (0, 0), (1, 0), (0, 1)], # T
                [(0, -1), (0, 1), (0, 0), (-1, 0)],  # -|
                [(-1, 0), (0, 0), (1, 0), (0, -1)],  # Upside down T
                [(0, -1), (0, 1), (0, 0), (1, 0)]  # |-

            ],
            [ # Line
                [(0, -1), (0, 0), (0, 1), (0, 2)],  # |
                [(-1, -1), (0, -1), (1, -1), (2, -1)],  # -
                [(1, -1), (1, 0), (1, 1), (1, 2)],  # |
                [(-1, 0), (0, 0), (1, 0), (2, 0)],  # -
            ],
            [ # Square
                [(-1, 0), (0, 0), (-1, 1), (0, 1)],  # Square
                [(-1, 0), (0, 0), (-1, 1), (0, 1)],
                [(-1, 0), (0, 0), (-1, 1), (0, 1)],
                [(-1, 0), (0, 0), (-1, 1), (0, 1)]
            ]

        ]

        self.new_piece()

    def __repr__(self):
        return str(self)

    def __str__(self):
        string_key = {FallingPiece: '▣ ', DeadPiece: '◼ ', BlankSpace: '◻ '}
        string = ""
        for y in range(self.h):
            for x in range(self.w):
                try:
                    string += string_key[self[x][y]]
                except:
                    string += '?'
            string += "\n"

        return string

    def active_coords(self):
        c = []
        for x in range(self.w):
            for y in range(self.h):
                if self[x][y] == FallingPiece:
                    c.append((x, y))
        return c

    def tick(self):
        if not self.check_if_can_move((0, 1)):
            self.kill_piece()

            if not self.new_piece():
                print('KILL')
                self.end_game()
                return
        else:
            self.move_active((0, 1))

        for row in self.check_rows():
            self.remove_row(row)

    def kill_piece(self):
        actives = self.active_coords()
        for (ax, ay) in actives:
            self[ax][ay] = DeadPiece

    def end_game(self):
        self.dead = True
        print('KILL')

    def new_piece(self):
        self.piece_index = random.randint(0, len(self.pieces) - 1)
        self.piece_rotation = 0
        new_piece_coords = self.pieces[self.piece_index][self.piece_rotation]
        top_coord = (self.w//2, 2)
        self.piece_center = top_coord

        for (px, py) in new_piece_coords:
            tx, ty = tuple_add(top_coord, (px, py))
            if self[tx][ty] != BlankSpace:
                return False
            else:
                self[tx][ty] = FallingPiece
        return True

    def check_if_can_move(self, direction):
        return self.check_if_can_go_to([tuple_add(active, direction) for active in self.active_coords()])

    def move_right(self):
        if self.check_if_can_move((1, 0)):
            self.move_active((1, 0))

    def move_left(self):
        if self.check_if_can_move((-1, 0)):
            self.move_active((-1, 0))

    def scan_down(self):
        while self.check_if_can_move((0, 1)):
            self.move_active((0, 1))

    def move_active(self, direction):
        new_actives = [tuple_add((ax, ay), direction) for ax, ay in self.active_coords()]
        self.piece_center = tuple_add(self.piece_center, direction)

        self.set_new_actives(new_actives)

    def set_new_actives(self, new_actives):
        old_actives = self.active_coords()
        for nx, ny in new_actives:
            self[nx][ny] = FallingPiece

        for ox, oy in old_actives:
            if (ox, oy) not in new_actives:
                try:
                    self[ox][oy] = BlankSpace
                except:
                    pass

    def rotate(self, dir=1):
        self.piece_rotation = (self.piece_rotation + dir) % 4
        new_actives = [tuple_add(self.piece_center, active_coord) for active_coord in self.pieces[self.piece_index][self.piece_rotation]]
        if self.check_if_can_go_to(new_actives):
         self.set_new_actives(new_actives)

    def check_rows(self):
        rows_to_remove = []
        for y in range(self.h):
            self.delete_row = True
            for x in range(self.w):
                if self[x][y] == BlankSpace or self[x][y] == FallingPiece:
                    self.delete_row = False
            if self.delete_row:
                rows_to_remove.append(y)
        return rows_to_remove

    def remove_row(self, row):
        for y in range(row, 0, -1):
            for x in range(self.w):
                self[x][y] = self[x][y - 1]

        for x in range(self.w):
            self[x][y] = BlankSpace

    def check_if_can_go_to(self, new_actives):
        for ax, ay in new_actives:
            if not (0 <= ax < self.w and 0 <= ay < self.h):
                return False
            if self[ax][ay] == DeadPiece:
                return False
        return True



def tuple_add(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]

def main():
    app = QtWidgets.QApplication(argv)
    t = UI(Board(10, 24))
    app.exec_()


if __name__ == '__main__':
    main()