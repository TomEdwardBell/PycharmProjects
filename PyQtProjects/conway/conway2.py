import random
import os
from PyQt5 import QtWidgets, QtGui
from sys import argv
import time


class Options:
    def __init__(self):
        self.grid_size = (70, 70)
        self.window_size = (1000, 1000)

        self.run_speed = "max"


class Simulation:
    def __init__(self):
        print("Loading Simulation")
        self.options = Options()

        self.board = []
        self.ui = Grid()
        self.ui.show()

        self.running = True
        self.create_board()

        self.super_run()
        self.step()

    def create_board(self):
        for x in range(self.options.grid_size[0]):
            self.board.append([])
            for y in range(self.options.grid_size[1]):
                if random.randint(0, 1) == 0:
                    self.board[x].append(0)
                    self.ui.board[x, y].setStyleSheet("background-color: #FFFFFF")
                else:
                    self.board[x].append(1)
                    self.ui.board[x, y].setStyleSheet("background-color: #000000")

    def super_run(self):
        while self.running:
            self.step()

    def run_timer_done(self):
        self.step()
        self.timer_available = True

    def step(self):
        alive_list, dead_list = [], []
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[1]):
                locs = self.get_locals((x, y))
                alive_count = 0
                for lx, ly in locs:
                    if self.board[lx][ly] == 1:
                        alive_count += 1
                if alive_count < 2:
                    dead_list.append((x, y))
                elif alive_count == 3:
                    alive_list.append((x, y))
                elif alive_count > 3:
                    dead_list.append((x, y))

        for ax, ay in alive_list:
            if self.board[ax][ay] == 0:
                self.board[ax][ay] = 1
                self.ui.board[ax, ay].setStyleSheet("background-color: #000000")
        for dx, dy in dead_list:
            if self.board[dx][dy] == 1:
                self.board[dx][dy] = 0
                self.ui.board[dx, dy].setStyleSheet("background-color: #FFFFFF")

        QtGui.QGuiApplication.processEvents()

    def get_locals(self, coords):
        localcoords = []
        relative_locals = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        # These are the vectors of the nearest coordinates

        for i in relative_locals:
            rel_x, rel_y = i[0], i[1]
            loc_x, loc_y = coords[0] + rel_x, coords[1] + rel_y

            if -1 not in [loc_x, loc_y] and loc_x < self.options.grid_size[0] and loc_y < self.options.grid_size[1]:
                localcoords.append((loc_x, loc_y))

        return (localcoords)


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.options = Options()

        self.grid_size = self.options.grid_size
        self.window_size = self.options.window_size
        self.board = {}
        self.widgets = {}
        self.init_ui()

    def init_ui(self):
        boardx = self.window_size[0]
        boardy = self.window_size[1]
        margintop = 60
        borderx = 0
        bordery = 0
        xcount = self.grid_size[0]
        ycount = self.grid_size[1]

        self.setStyleSheet("background-color: #222222")

        self.resize((boardx + borderx * (xcount + 1)), (boardy + bordery * (ycount + 1)) + margintop)
        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y] = QtWidgets.QLabel(self)
                self.board[x, y].show()
                self.board[x, y].setStyleSheet("background-color: #FFFFFF")
                self.board[x, y].coordinates = [x, y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*borderx)
                yloc = (y*ypercoord + (y+1)*bordery + margintop)
                self.board[x, y].move(xloc, yloc)
                self.board[x, y].resize(boardx/xcount, boardy/ycount)




def main():
    app = QtWidgets.QApplication(argv)
    game = Simulation()
    app.exec_()


if __name__ == '__main__':
    main()
