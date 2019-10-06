#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
import keyboard
import os
from PyQt5 import QtWidgets, QtGui, QtCore


class Options:
    board_width = 10
    board_height = 24
    window_size = (400, 960)
    time_gap = 0.2

    shapes = [
        #[(0, 0)], # Single block
        [(0, 0), (1, 0), (1, 1)] # Large Square
    ]

    colors = {
        'dead': '#555555',
        'active': '#FF0000',
        'empty': '#FFFFFF'
    }

class Board(dict):
    def __init__(self):
        super(Board, self).__init__()
        self.running = True
        self.dead = []
        self.active = []
        self.center = (0, 0)

        self.setup()
        self.ui = None

    def setup(self):
        self.fill()

        keyboard.add_hotkey('a', lambda: self.check_move((-1, 0)))
        keyboard.add_hotkey('d', lambda: self.check_move((1, 0)))
        keyboard.add_hotkey('w', lambda: self.rotate())
        keyboard.add_hotkey('s', lambda: self.down())
        self.new_piece()

    def mainloop(self):
        while self.running:
            self.tick()
            if self.running:
                self.display()
                self.update_ui()
                time.sleep(Options.time_gap)

    def fill(self):
        for y in range(Options.board_height):
            for x in range(Options.board_width):
                self[x, y] = Empty()

    def new_piece(self):
        self.active = []
        shape = random.choice(Options.shapes)
        self.center = (int(Options.board_width/2), 0)
        for shape_coord in shape:
            coord = coord_add(shape_coord, self.center)
            if type(self[coord]) != Empty:
                self.game_over()
                return None
            else:
                self[coord] = Piece()
                self.active.append(coord)

    def tick(self):
        if self.check((0, 1)):
            self.move((0, 1))
        else:
            self.kill_piece()
            for row in self.check_rows():
                self.clear_row(row)
            self.new_piece()

    def check(self, direction):
        for c in self.active:
            new = coord_add(c, direction)
            if not(-1 < new[0] < Options.board_width and -1 < new[1] < Options.board_height):
                return False
            if new not in self.active and not type(self[new]) == Empty :
                return False
        return True

    def kill_piece(self):
        for c in self.active:
            self.dead.append(self[c])
            self[c].die()
        self.active = []

    def move(self, direction):
        new_active = []
        # Find out new positions
        for c in self.active:
            new = coord_add(c, direction)
            new_active.append(new)

        # Add new pieces
        for n in new_active:
            if n not in self.active:
                self[n] = Piece()

        # Remove old pieces
        for c in self.active:
            if c not in new_active:
                self[c] = Empty()
                self[c].state = "empty"

        # Update self.active
        self.active = new_active
        self.center = coord_add(self.center, direction)

    def down(self):  # Moves piece downwards until it hits the bottom
        clear = self.check((0, 1))
        while clear:
            self.move((0, 1))
            self.display()
            clear = self.check((0, 1))

    def check_move(self, direction):
        if self.check(direction):
            self.move(direction)
            self.display()

    def display(self):
        os.system('cls')
        print('--------------------')
        for y in range(Options.board_height):
            line = ''
            for x in range(Options.board_width):
                item = self[x, y]
                line += str(item)
            print(line)

    def check_rows(self):
        rows = []
        for y in range(Options.board_height):
            full = True
            for x in range(Options.board_width):
                if type(self[x, y]) == Empty:
                    full = False
                elif not self[x, y].dead:
                    full = False
            if full:
                rows.append(y)
        return rows

    def clear_row(self, row):
        for y in range(row, 0, -1):
            for x in range(Options.board_width):
                if (x, y) not in self.active:
                    self[x, y] = self[x, y - 1]
                    if (x, y - 1) in self.dead:
                        self.dead.remove((x, y - 1))
                        self.dead.append((x, y))
        for x in range(Options.board_width):
            self[x, 0] = Empty()

    def rotate(self):
        clear = True
        cx, cy = self.center
        for (x, y) in self.active:
            newx, newy = -(y-cy)+cx, (x-cx)+cy
            if not(0 <= newx < Options.board_width and 0 <= newy < Options.board_height):
                clear = False
            elif type(self[newx, newy]) != Empty and (newx, newy) not in self.active:
                clear = False
        if clear:
            # Find out new positions
            new_active = []
            for (x, y) in self.active:
                newx, newy = -(y-cy)+cx,  (x-cx)+cy
                new_active.append((newx, newy))

            # Add new pieces
            for n in new_active:
                if n not in self.active:
                    self[n] = Piece()

            # Remove old pieces
            for c in self.active:
                if c not in new_active:
                    self[c] = Empty()
                    self[c].state = "empty"
            self.display()
            self.active = new_active

    def update_ui(self):
        for y in range(Options.board_height):
            for x in range(Options.board_width):
                print("{}{}bing".format(x, y))
                state = self[x, y].state
                self.ui.update((x, y), state)

    def game_over(self):
        self.running = False
        print('DEAD')


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



class Empty():
    def __init__(self):
        self.state = "empty"

    def __str__(self):
        return '▢'

    def die(self):
        pass


class Piece():
    def __init__(self):
        super(Piece, self).__init__()
        self.dead = False
        self.state = "active"

    def __str__(self):
        if self.dead:
            return '▩'
        else:
            return '▣'

    def die(self):
        self.dead = True
        self.state = "dead"


def coord_add(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]


b = Board()

'''from PyQt5 import QtWidgets
from sys import argv

import tetris
import tetris_ui as Ui


def main():
    app = QtWidgets.QApplication(argv)
    t = tetris.Board()
    ui = Ui.Ui(tetris.Options)
    t.ui = ui
    t.mainloop()
    app.exec_()


if __name__ == '__main__':
    main()'''