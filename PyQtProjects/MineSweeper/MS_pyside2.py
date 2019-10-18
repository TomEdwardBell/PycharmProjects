from PySide2 import QtWidgets, QtGui, QtCore
from sys import argv

import random


class Options:
    def __init__(self):
        self.grid_size = (15, 15)
        # ^ Grid size
        #   (Width, Height)

        self.window_size = (720, 720)
        # ^ Window size
        #   Pixels

        self.mine_count = 30
        # ^ Number of mines on the board


class MainGame:
    def __init__(self):
        print("Game Initialising...")

        self.options = Options()

        self.clicks = 0
        self.mine_count = self.options.mine_count
        self.ui = Grid()
        self.set_mines()
        self.set_slots()
        self.mouse_mode = "normal"
        self.ui.show()
        print("Game Loaded")

        self.ui.keyPressEvent = self.keyPressEvent
        # ^^^ keyPressEvent mussed be defined in the UI
        # ^^^ So I defined it here and then just added it to the UI

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_F:
            self.flag_switch()

    def set_mines(self):
        for i in range(self.mine_count):
            mine_placed = False
            mine_x = 0
            mine_y = 0  # This line and the one above just make PyCharm happier
            while not mine_placed:
                mine_placed = True
                mine_x = random.randint(0, self.options.grid_size[0] - 1)
                mine_y = random.randint(0, self.options.grid_size[1] - 1)

                if self.ui.board[mine_x, mine_y].hidden_value == "x":
                    mine_placed = False

            self.ui.board[mine_x, mine_y].set_value("x")

    def set_slots(self):
        pos = []
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[1]):
                pos.append((x, y))
                self.ui.board[x, y].clicked.connect(lambda x=x, y=y: self.clicked((x, y), True))
        self.ui.widgets.flag_btn.clicked.connect(self.flag_switch)

    def clicked(self, coords, realclick):
        #time.sleep(0.05)
        x, y = coords
        ignore_realclick = False
        QtGui.QGuiApplication.processEvents()

        if self.mouse_mode == "flag":
                self.flag_click(coords)

        elif self.mouse_mode == "nor[mal":
            pass

        elif self.mouse_mode == "normal" and not self.ui.board[x, y].been_clicked:
            #time.sleep(0.001)
            ignore_realclick = True
            if self.ui.board[x, y].shown_value != "⚑":  # Makes sure it's not flagged. No accidental clicking!
                ignore_realclick = False

                if not self.ui.board[x, y].been_clicked:
                    self.ui.board[x, y].been_clicked = True

                if self.ui.board[x, y].hidden_value == "x":
                    ignore_realclick = True
                    self.game_over()

                else:
                    minecount = self.get_minecount(coords)
                    self.ui.board[x, y].set_value(minecount)
                    self.ui.board[x, y].been_clicked = True

                    if minecount == 0:  # The thing where if you click one of "0" it also removes the other nearby 0s
                        for loc_x, loc_y in self.get_locals((x, y)):  # Gets local coords
                            if not self.ui.board[loc_x, loc_y].been_clicked:  # If they've not been clicked
                                self.clicked((loc_x, loc_y), False)  # Oh sorry, is that recursion
                                # HELL YEAH IT IS!!!
                                # No but that function basically will click the nearby coord for you.

            if realclick and not ignore_realclick:
                self.clicks += 1
                self.ui.widgets.clicks_lbl.setText("Clicks: "+str(self.clicks))

        if realclick:
            self.checkwon()

    def flag_click(self, coords):
        x, y = coords
        if not self.ui.board[x, y].been_clicked:
            if self.ui.board[x, y].shown_value == " ":
                self.ui.board[x, y].set_value("⚑")
                ignore_realclick = True
            elif self.ui.board[x, y].shown_value == "⚑":
                self.ui.board[x, y].set_value("/⚑")
                ignore_realclick = False

    def flag_switch(self):
        if self.mouse_mode == "normal":
            self.mouse_mode = "flag"
            self.ui.widgets.flag_btn.setText("🏴󠁧󠁢󠁥󠁮󠁧󠁿")
            self.ui.widgets.flag_btn.setStyleSheet("background-color: #5555DD ;font-size: 20pt; color: #FFFFFF")
        elif self.mouse_mode == "flag":
            self.mouse_mode = "normal"
            self.ui.widgets.flag_btn.setText("⛏")
            self.ui.widgets.flag_btn.setStyleSheet("background-color: #333333 ;font-size: 20pt; color: #888888")

    def get_locals(self, coords):
        localcoords = []
        relative_locals = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        # These are the vectors of the nearest coordinates

        for i in relative_locals:
            rel_x = i[0]
            rel_y = i[1]
            loc_x = coords[0] + rel_x
            loc_y = coords[1] + rel_y
            if -1 not in [loc_x, loc_y] and loc_x < self.options.grid_size[0] and loc_y < self.options.grid_size[1]:
                localcoords.append([loc_x, loc_y])
        return(localcoords)

    def get_minecount(self, coords):
        localcoords = self.get_locals(coords)

        minecount = 0

        for coord in localcoords:
            if self.ui.board[coord[0], coord[1]].hidden_value == "x":
                minecount += 1

        return(minecount)

    def checkwon(self):
        won = True
        for coordnum in self.ui.board:
            if won:  # If it knows you haven't won it won't bother checking the rest of the coords
                coord = self.ui.board[coordnum]
                if coord.hidden_value == "x" and (coord.hidden_value + coord.shown_value) != "x⚑":
                    # ^^^ If you haven't found every bomb and marked it
                    won = False  # You haven't

                if coord.hidden_value + coord.shown_value in ["⚑", " ⚑"]:
                    # ^^^ If you marked a piece that isn't a bomb
                    won = False  # You lose
        if won:
            self.mouse_mode = "won"
            for coordnum in self.ui.board:
                coord = self.ui.board[coordnum]
                coord.win()

    def game_over(self):
        for x in range(self.options.grid_size[0]):
            for y in range(self.options.grid_size[1]):
                self.ui.board[x, y].die()
        self.mouse_mode = "dead"


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.options = Options()

        self.grid_size = self.options.grid_size
        self.window_size = self.options.window_size
        self.board = {}
        self.setStyle(QtWidgets.QStyleFactory.create('Windows'))


        class Widgets:
            pass

        self.widgets = Widgets()

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

        self.widgets.flag_btn = QtWidgets.QPushButton(self)
        self.widgets.flag_btn.setText("⛏")
        self.widgets.flag_btn.resize(60, 60)
        self.widgets.flag_btn.setStyleSheet("background-color: #333333 ;font-size: 20pt; color: #888888")

        self.widgets.clicks_lbl = QtWidgets.QLabel(self)
        self.widgets.clicks_lbl.setText("Clicks: 0")
        self.widgets.clicks_lbl.move(200, 0)
        self.widgets.clicks_lbl.resize(150, 60)
        self.widgets.clicks_lbl.setStyleSheet("font-size: 20pt; color: #888888")

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
                self.board[x, y].set_font_size()

                self.board[x, y].set_value(" ")


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.been_clicked = False
        self.hidden_value = " "
        self.shown_value = " "
        self.font_size = "10"
        self.color_numbers = {
            0: "#333333",
            1: "#EE1111",
            2: "#DDDD11",
            3: "#11EE22",
            4: "#1155FF",
            5: "#EE00EE",
            6: "#FF0000",
            7: "#EE6600",
            8: "#6611AA"
        }

    def set_font_size(self):
        self.font_size = ((self.height() + self.width())**1.3) * 0.1
        self.font_size = str(int(self.font_size))

    def set_color(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.setStyleSheet("background-color:" + color)

    def process_values(self, new_value, hidden_old):
        default_style_sheet = "font-size: "+self.font_size+"; background-color: #444444;"

        if new_value == "x":  # If its secretly being set to "x"
            shown_value = " " # Show nothing
            hidden_value = "x" # But secretly it's and x (bomb)
            style_sheet = default_style_sheet
            been_clicked = False

        elif new_value == "⚑":  # If you're flagging It
            shown_value = "⚑"
            hidden_value = hidden_old # Don't change the hidden value
            style_sheet = "font-size: "+self.font_size+"px; color: #DDDDDD; background-color: #5555DD"
            been_clicked = False

        elif new_value == "/⚑":  # If its secretly being set to "x"
            shown_value = " " # Show nothing
            hidden_value = hidden_old # But secretly it's and x (bomb)
            style_sheet = default_style_sheet
            been_clicked = False

        elif new_value == "" or new_value == " ":  # If its secretly being set to "x"
            shown_value = " " # Show nothing
            hidden_value = hidden_old # But secretly it's and x (bomb)
            style_sheet = default_style_sheet
            been_clicked = False

        elif new_value == 10:  # If it is 0
            shown_value = ""  # Leave it blank
            hidden_value = hidden_old
            style_sheet = 'background-color: #555555;'
            been_clicked = True  # The button has now been clicked

        elif new_value in [0, 1, 2, 3, 4, 5, 6, 7, 8]:  # If it is a number
            shown_value = str(new_value)  # Show the value on the button
            hidden_value = hidden_old
            style_sheet = '''
            background-color: #666666;
            font-size: '''+self.font_size+'''px;
            font-weight: 900;
            color: ''' + self.color_numbers[new_value]

            #  ^^^ Sets the colour of the text depending on what the color_numbers constant is
            been_clicked = True # The button has now been clicked

        else:  # If it is not a valid value
            shown_value = "?"
            hidden_value = "?"
            style_sheet = default_style_sheet
            been_clicked = False

        return (shown_value, hidden_value, style_sheet, been_clicked)

    def set_value(self, tochangeto):
        shown_value, hidden_value, style_sheet, been_clicked = self.process_values(tochangeto, self.hidden_value)
        # ^^ Processes the new value

        self.shown_value = shown_value
        self.hidden_value = hidden_value
        self.setStyleSheet(style_sheet)
        self.been_clicked = been_clicked
        self.setText(str(self.shown_value))
        # Sets then new values and changes the text

    def die(self):
        if self.hidden_value == "x":
            if self.shown_value == "⚑":
                self.setText("⚑")
                self.setStyleSheet("font-size:"+self.font_size+"px; color: #FFFFFF; background-color: #DD0000")
            else:
                self.setText("⛌")
                self.setStyleSheet("font-size:"+self.font_size+"px; color: #000000; background-color: #FF0000")

    def win(self):
        if self.hidden_value == "x" and self.shown_value != "⚑":
            self.setText("?")  # Should not occur
        if self.hidden_value == "x" and (self.shown_value == "⚑" or self.shown_value == " "):
            self.setStyleSheet("font-size:"+self.font_size+"px; color: #000000; background-color: #00FF00")


def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
