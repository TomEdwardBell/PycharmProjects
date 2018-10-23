from PyQt5 import QtWidgets, QtTest
import sys
import random

class Options:
    def __init__(self):
        self.window_size = (500, 500)
        # ^ Window size
        #   (width / height)
        #   Pixels

        self.grid_size = (10, 10)
        # ^ Grid size

        self.ships_list = [[5, "Aircraft carrier"], [4, "Battleship"], [3, "Cruiser"], [3, "Submarine"], [2, "Destroyer"]]
        # ^ Each ship
        #   Length, then name
        #   Make sure lengths are less than the grid size


class MainGame:
    def __init__(self):
        print("Game Initialising...")
        self.ui = Grid()
        self.options = Options()

        self.clicks = 0
        self.set_boats()
        self.set_slots()
        self.ui.show()

    def set_boats(self):
        shipslist = self.options.ships_list
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[1]):
                self.ui.board[x, y].set_value("•")  # Sets blank board

        random.shuffle(shipslist)  # Randomising order of setting ships
        for ship in shipslist:  # For every ship
            shipplaced = False  # Validation shizzle
            while not shipplaced:
                shipplaced = True
                shipdirection = random.choice(["H","V"])  # Randomly makes a ship verticle or horizontal
                shiplength = ship[0]  #Ship has a length then a name

                shiporiginx = random.randint(0, self.options.grid_size[0] - 1)
                shiporiginy = random.randint(0, self.options.grid_size[1] - 1)
                shiporigin = [shiporiginx , shiporiginy]
                # Randomly sets an "origin point" for each boat
                # Even if it's ivalid (that gets sortedlater)

                if shipdirection == "H":
                    if shiporigin[0] + shiplength > self.options.grid_size[0]: # If its to long
                        shipplaced = False

                if shipdirection == "V":
                    if shiporigin[1] + shiplength > self.options.grid_size[1]: # If it's too long
                        shipplaced = False

                if shipplaced == True:
                    if shipdirection == "H":  # Collision detection
                        for i in range(shiplength):
                            if self.ui.board[shiporigin[0] + i, shiporigin[1]].hidden_value != "•":
                                # All of the pieces it's replacing must be blank
                                shipplaced = False

                    if shipdirection == "V": # Collision detection
                        for i in range(shiplength - 1):
                            if self.ui.board[shiporigin[0], shiporigin[1] + i].hidden_value != "•":
                                # All of the pieces it's replacing must be blank
                                shipplaced = False


            # If ship placed is true
            if shipdirection == "H":
                for a in range(shiplength):
                    self.ui.board[shiporigin[0] + a, shiporigin[1]].set_value("═")
                    # Pieces now set

            if shipdirection == "V":
                for a in range(shiplength):
                    self.ui.board[shiporigin[0], shiporigin[1] + a].set_value("║")
                    # Pieces now set

        # End of that massive method (ugh)

    def set_slots(self):
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[0]):
                self.ui.board[x, y].clicked.connect(lambda state, c=(x, y): self.clicked(c))

    def clicked(self, coords):
        x = coords[0]
        y = coords[1]

        if self.ui.board[x, y].hidden_value == "║" or self.ui.board[x, y].hidden_value == "═":
            self.ui.board[x, y].set_value("x")
            self.checkwon()
        elif self.ui.board[x, y].hidden_value == "•":
            self.ui.board[x, y].set_value(" ")
        self.clicks += 1

    def checkwon(self):
        won = True
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[1]):
                if self.ui.board[x, y].hidden_value == "═" or self.ui.board[x, y].hidden_value == "║":
                    won = False

        if won:
            print("WON", self.clicks)
            self.ui.win()


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.options = Options()
        self.board = {}
        self.init_ui()

    def init_ui(self):
        boardx = self.options.window_size[0]
        boardy = self.options.window_size[1]
        border = 0
        xcount = self.options.grid_size[0]
        ycount = self.options.grid_size[1]

        self.resize(boardx + border * (xcount + 1), boardy + border * (xcount + 1))
        for x in range(xcount):
            for y in range(ycount):
                self.board[x, y] = Coord(self)
                self.board[x, y].coordinates = [x, y]
                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x*xpercoord + (x+1)*border)
                yloc = (y*ypercoord + (y+1)*border)
                self.board[x, y].move(xloc, yloc)
                self.board[x, y].resize(boardx/xcount, boardy/ycount)

    def print_coord(self, coord):
        print(coord.coordinates)

    def win(self):
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[1]):
                toerase = ["•", "O", " "]
                if self.board[x, y].hidden_value in toerase:
                    self.board[x, y].set_value(" ")
                    self.board[x, y].setStyleSheet('''
                    font-size: 35pt;
                    background-color: #22DD11;
                    ''')
                else:
                    self.board[x, y].setStyleSheet('''
                    background-color: #FFFFFF;
                    font-size: 35pt;
                    ''')


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.hidden_value = " "
        self.shown_value = " "
        self.styleSheet = " "
        self.acceptable_values = ["x", "X", "O", "•", "═", "║", " "]

    def set_color(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.setStyleSheet("background-color:" + color)

    def set_value(self, tochangeto):
        self.hidden_value = tochangeto
        if self.hidden_value == "║" or self.hidden_value == "═":
            self.shown_value = "•"
        elif self.hidden_value not in self.acceptable_values:
            self.shown_value = "?"
        else:
            self.shown_value = self.hidden_value

        self.setText(self.shown_value)
        self.setStyleSheet("font-size: 30pt")

        #Setting board Colors

        if self.shown_value == "•":
            self.setStyleSheet("font-size: 30pt; background-color: #3333DD")
        if self.shown_value == "x":
            self.setStyleSheet("font-size: 30pt; background-color: #EE1111")
        if self.shown_value == " ":
            self.setStyleSheet("font-size: 30pt; background-color: #EEEEEE")


def main():
    app = QtWidgets.QApplication(sys.argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
