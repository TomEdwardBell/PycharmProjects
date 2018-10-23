from gspread import authorize
from sys import argv, exit
from PyQt5 import QtWidgets, QtCore, QtGui
from oauth2client.service_account import ServiceAccountCredentials
import random
import asyncio


class Menu(QtWidgets.QMainWindow):
    def __init__(self):
        super(Menu, self).__init__()
        self.widgets = {}
        self.initUI()
        self.show()

    def initUI(self):
        self.resize(512, 256)

        self.widgets["title_lbl"] = QtWidgets.QLabel(self)
        self.widgets["title_lbl"].setText("Noughts and Crosses!")
        self.widgets["title_lbl"].resize(512,60)
        self.widgets["title_lbl"].setStyleSheet("font-size: 50px")
        self.widgets["title_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["subtitle_lbl"] = QtWidgets.QLabel(self)
        self.widgets["subtitle_lbl"].setText("Online")
        self.widgets["subtitle_lbl"].move(0,60)
        self.widgets["subtitle_lbl"].resize(512, 40)
        self.widgets["subtitle_lbl"].setStyleSheet("font-size: 35px; font-style: italic")
        self.widgets["subtitle_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["start_btn"] = QtWidgets.QPushButton(self)
        self.widgets["start_btn"].move(0,128)
        self.widgets["start_btn"].resize(256,128)
        self.widgets["start_btn"].setText("Start")
        #self.widgets["start_btn"].clicked.connect(lambda:self.widgets["title_lbl"].setText("Loading"))
        self.widgets["start_btn"].clicked.connect(self.gameload)

        self.widgets["quit_btn"] = QtWidgets.QPushButton(self)
        self.widgets["quit_btn"].move(256, 128)
        self.widgets["quit_btn"].resize(256, 128)
        self.widgets["quit_btn"].setText("Quit")
        self.widgets["quit_btn"].clicked.connect(exit)

    def gameload(self):
        self.hide()
        game = MainGame()
        #
        # load.hide()


class Loading(QtWidgets.QMainWindow):
    def __init__(self):
        super(Loading, self).__init__()
        self.widgets = {}
        self.widgets["title_lbl"] = QtWidgets.QLabel(self)
        self.widgets["title_lbl"].resize(512, 60)
        self.widgets["title_lbl"].setStyleSheet("font-size: 50px")
        self.widgets["title_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["subtitle_lbl"] = QtWidgets.QLabel(self)
        self.widgets["subtitle_lbl"].move(0, 60)
        self.widgets["subtitle_lbl"].resize(512, 40)
        self.widgets["subtitle_lbl"].setStyleSheet("font-size: 35px; font-style: italic")
        self.widgets["subtitle_lbl"].setAlignment(QtCore.Qt.AlignCenter)

        self.widgets["title_lbl"].setText("Loading")
        self.widgets["subtitle_lbl"].setText("Please wait")
        self.resize(512, 128)
        self.show()
        QtGui.QGuiApplication.processEvents()


class MainGame:
    def __init__(self):
        #creating objects
        load = Loading()
        self.board = Grid()
        self.server = Server()
        load.hide()
        newboard = self.server.grabboard()

        self.board.setboard(newboard)
        self.board.show()

        QtGui.QGuiApplication.processEvents()
        self.mainloop()

    def mainloop(self):
        servercheck = self.server.grabboard()

        running = True
        while running == True:
            QtGui.QGuiApplication.processEvents()
            if self.board.busy != False:
                x = self.board.busy[0]
                y = self.board.busy[1]
                self.server.newvalue(x,y,"@")
                self.board.refresh = True
                self.board.busy = False

            if self.board.refresh:
                if servercheck != self.server.grabboard():
                    self.board.setboard(self.server.grabboard())
                    servercheck = self.server.grabboard()
                self.board.refresh = False

            if self.board.wipe:
                for x in range(3):
                    for y in range(3):
                        self.server.newvalue(x, y, "")
                self.board.refresh = True
                self.board.wipe = False


class Grid(QtWidgets.QMainWindow):
    def __init__(self):
        super(Grid, self).__init__()
        self.widgets = {}
        self.coords = {}
        self.initUI()
        self.busy = False
        self.refresh = False
        self.wipe = False

    def initUI(self):
        boardx = 650
        boardy = 650
        header = 60
        border = 0
        xcount = 3
        ycount = 3

        self.widgets["servernamelbl"] = QtWidgets.QLabel(self)
        self.widgets["servernamelbl"].setText("blankserver")
        self.widgets["servernamelbl"].resize(90, 30)
        self.widgets["servernamelbl"].move(0, 0)

        self.widgets["changeserverln"] = QtWidgets.QLineEdit(self)
        self.widgets["changeserverln"].move(0, 30)
        self.widgets["changeserverln"].resize(90, 30)

        self.widgets["changeserverbtn"] = QtWidgets.QPushButton(self)
        self.widgets["changeserverbtn"].move(90, 30)
        self.widgets["changeserverbtn"].resize(100, 30)
        self.widgets["changeserverbtn"].setText("Change Server")

        self.widgets["refreshbtn"] = QtWidgets.QPushButton(self)
        self.widgets["refreshbtn"].move(605,0)
        self.widgets["refreshbtn"].resize(45,45)
        self.widgets["refreshbtn"].setText("Refresh")
        self.widgets["refreshbtn"].clicked.connect(self.dorefresh)

        self.widgets["wipebtn"] = QtWidgets.QPushButton(self)
        self.widgets["wipebtn"].move(560,0)
        self.widgets["wipebtn"].resize(45,45)
        self.widgets["wipebtn"].setText("Wipe Board")
        self.widgets["wipebtn"].clicked.connect(self.dowipe)


        self.resize(boardx + border * (xcount + 1), boardy + border * (xcount + 1) + header)
        self.makeboard(xcount, ycount, border, header, boardx, boardy)

    def dorefresh(self):
        if self.refresh == False and self.busy == False and self.wipe == False:
            self.refresh = True

    def dowipe(self):
        if self.refresh == False and self.busy == False and self.wipe == False:
            self.wipe = True

    def makeboard(self, xcount, ycount, border, header, boardx, boardy):
        for x in range(xcount):
            for y in range(ycount):
                self.coords[x, y] = Coord(self)
                self.coords[x, y].coordinates = [x, y]

                xpercoord = (boardx / xcount)
                ypercoord = (boardy / ycount)
                xloc = (x * xpercoord + (x + 1) * border)
                yloc = (y * ypercoord + (y + 1) * border + header)
                self.coords[x, y].btn.move(xloc, yloc)
                self.coords[x, y].btn.resize(boardx / xcount, boardy / ycount)

                self.coords[x, y].btn.clicked.connect(lambda state, c = [x, y]: self.btnclicked(c))

                self.coords[x, y].setvalue("Loading")

        #self.show()

    def btnclicked(self,coords):
        self.busy = (coords)

    def setboard(self, newboard):
        for x in range(3):
            for y in range(3):
                newvalue = newboard[x, y]
                self.coords[x, y].btn.setText(newvalue)



class Server:
    def __init__(self):
        servername = "start"
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_access.json', scope)
        client = authorize(creds)
        self.sheet = client.open("NAConline").worksheet(servername)
        self.board = {}

    def changeboard(self, severname):
        scope = ['https://spreadsheets.google.com/feeds']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_access.json', scope)
        client = authorize(creds)
        self.sheet = client.open("NAConline").worksheet(severname)

    def grabboard(self):
        fullboard = {}
        for x in range(3):
            for y in range(3):
                fullboard[x, y] = self.getvalue(x, y)
        return(fullboard)

    def getvalue(self, x, y):
        value = self.sheet.cell((y + 1), (x + 1)).value
        return value

    def newvalue(self, x, y, change):
        self.sheet.update_cell((y + 1), (x + 1), str(change))


class Coord:
    def __init__(self, game):
        self.btn = QtWidgets.QPushButton(game)
        self.active = False
        self.btn.setStyleSheet("font-size: 100pt")

    def setcolor(self, color):
        if color == "rand":
            hexes = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
            color = "#"
            for q in range(6):
                color = color + random.choice(hexes)
        self.btn.setStyleSheet("background-color:" + color)

    def setvalue(self, newtext):
        self.btn.setText(str(newtext))
        #self.btn.setStyleSheet("font-size: 300%")


def main():
    app = QtWidgets.QApplication(argv)
    menu = Menu()
    app.exec_()


if __name__ == '__main__':
    main()
