from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv
import random


class Options:
    def __init__(self):
        self.grid_size = (30, 30)
        self.window_size = (600, 600)

        self.run_speed = "max"


class Simulation:
    def __init__(self):
        print("Loading Simulation")
        self.options = Options()

        self.ui = Grid()

        self.ui.show()

        self.running = False
        self.run_speed = 1000
        # ^^^ When running - how many ticks per second
        self.timer_available = True

        self.step()

        self.ui.keyPressEvent = self.keyPressEvent
        # ^^^ keyPressEvent mussed be defined in the UI
        # ^^^ So I defined it here and then just added it to the UI


    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_E:
            self.step()
        if e.key() == QtCore.Qt.Key_F:
            self.all_alive()
        if e.key() == QtCore.Qt.Key_Q:
            if self.running:
                self.running = False
            else:
                self.running = True
                if self.options.run_speed == "max":
                    self.super_run()
                else:
                    self.run()

    def super_run(self):
        while self.running:
            self.step()
            QtGui.QGuiApplication.processEvents()

    def run(self):
        tick_count = 0
        tick_speed = 1 / self.options.run_speed
        while self.running:
            tick_count += 1
            if self.timer_available:
                self.timer_available = False
                timer = QtCore.QTimer()
                timer.timeout.connect(self.run_timer_done)
                timer.start(tick_speed)
                QtGui.QGuiApplication.processEvents()

    def run_timer_done(self):
        self.step()
        self.timer_available = True

    def all_alive(self):
        for coordcode in self.ui.board:
            coord = self.ui.board[coordcode]
            if random.randint(0, 2) == 0:
                coord.make_alive()
            else:
                coord.make_dead()

    def step(self):
        alive_list, dead_list = [], []

        for coordcode in self.ui.board:
            coord = self.ui.board[coordcode]
            locals = self.get_locals(coordcode)
            alive_count = 0
            for l in locals:
                if self.ui.board[l].alive:
                    alive_count += 1
            if alive_count < 2:
                dead_list.append(coord)
            elif alive_count == 3:
                alive_list.append(coord)
            elif alive_count > 3:
                dead_list.append(coord)


        for alive in alive_list:
            alive.make_alive()
        for dead in dead_list:
            dead.make_dead()

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
                self.board[x, y] = Coord(self)
                self.board[x, y].coordinates = [x, y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*borderx)
                yloc = (y*ypercoord + (y+1)*bordery + margintop)
                self.board[x, y].move(xloc, yloc)
                self.board[x, y].resize(boardx/xcount, boardy/ycount)


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)

        self.make_dead()

        self.clicked.connect(self.switch_state)

    def make_dead(self):
        self.alive = False
        self.set_color("#FFFFFF")

    def make_alive(self):
        self.alive = True
        self.set_color("#000000")

    def switch_state(self):
        if self.alive:
            self.make_dead()
        else:
            self.make_alive()

    def set_color(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.setStyleSheet("background-color:" + color)


def main():
    app = QtWidgets.QApplication(argv)
    game = Simulation()
    app.exec_()


if __name__ == '__main__':
    main()
