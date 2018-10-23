from sys import argv
from PyQt5 import QtWidgets, QtCore
import socket


class MainGame:
    def __init__(self):
        self.server = ""
        self.username = ""
        self.chr = ""
        self.servercode = ""

        self.menu = Menu(self)

    def join_server(self):
        serverconnection = Client(self)
        serverconnection.join()
        self.menu.close()
        self.game_loop()


    def game_loop(self):
        running = True
        while running:
            command = input()
            serverconnection = Client(self)
            print("p")
            serverconnection.send(command)


class Menu:
    def __init__(self, maingame):
        self.maingame = maingame
        self.done = False
        self.username = ""
        self.welcome_screen = self.WelcomeScreen(self)

    class WelcomeScreen(QtWidgets.QMainWindow):
        def __init__(self,parent):
            super(Menu.WelcomeScreen, self).__init__()
            self.widgets = {}
            self.init_ui(parent)

        def init_ui(self, parent):
            self.resize(300, 300)

            self.widgets["title_lbl"] = QtWidgets.QLabel(self)
            self.widgets["title_lbl"].setText("Game")
            self.widgets["title_lbl"].setStyleSheet("font-size: 30pt")
            self.widgets["title_lbl"].setAlignment(QtCore.Qt.AlignCenter)
            self.widgets["title_lbl"].resize(300, 150)
            self.widgets["title_lbl"].move(0, 0)

            self.widgets["subtitle_lbl"] = QtWidgets.QLabel(self)
            self.widgets["subtitle_lbl"].setText("Client Version")
            self.widgets["subtitle_lbl"].setStyleSheet("font-size: 10pt")
            self.widgets["subtitle_lbl"].setAlignment(QtCore.Qt.AlignCenter)
            self.widgets["subtitle_lbl"].resize(300, 150)
            self.widgets["subtitle_lbl"].move(0,50)

            self.widgets["ok_btn"] = QtWidgets.QPushButton(self)
            self.widgets["ok_btn"].clicked.connect(lambda x: self.start_game_joiner(parent))
            self.widgets["ok_btn"].setText("Play")
            self.widgets["ok_btn"].setStyleSheet("font-size: 30pt")
            self.widgets["ok_btn"].resize(300, 150)
            self.widgets["ok_btn"].move(0, 150)

            self.show()

        def start_game_joiner(self, parent):
            self.hide()
            parent.gamejoiner = parent.GameJoiner(parent)

    class GameJoiner(QtWidgets.QMainWindow):
        def __init__(self, parent):
            super(Menu.GameJoiner, self).__init__()
            self.widgets = {}
            self.username = ""
            self.chr = ""
            self.servercode = 0
            self.parent = parent
            self.maingame = parent.maingame

            self.init_ui()

        def init_ui(self):
            self.resize(220, 380)

            self.widgets["title_lbl"] = QtWidgets.QLabel(self)
            self.widgets["title_lbl"].setText("Game Joiner")
            self.widgets["title_lbl"].setStyleSheet("font-size: 15pt")
            self.widgets["title_lbl"].move(10, 10)
            self.widgets["title_lbl"].resize(500, 30)

            self.widgets["username_lbl"] = QtWidgets.QLabel(self)
            self.widgets["username_lbl"].setText("Username:")
            self.widgets["username_lbl"].setStyleSheet("font-size: 10pt")
            self.widgets["username_lbl"].move(10, 50)
            self.widgets["username_lbl"].resize(500, 20)

            self.widgets["username_ln"] = QtWidgets.QLineEdit(self)
            self.widgets["username_ln"].setStyleSheet("font-size: 10pt")
            self.widgets["username_ln"].move(10, 70)
            self.widgets["username_ln"].resize(200, 30)

            self.widgets["chr_lbl"] = QtWidgets.QLabel(self)
            self.widgets["chr_lbl"].setText("Character:")
            self.widgets["chr_lbl"].setStyleSheet("font-size: 10pt")
            self.widgets["chr_lbl"].move(10, 130)
            self.widgets["chr_lbl"].resize(500, 20)

            self.widgets["chr_ln"] = QtWidgets.QLineEdit(self)
            self.widgets["chr_ln"].move(10, 150)
            self.widgets["chr_ln"].resize(50, 50)
            self.widgets["chr_ln"].setStyleSheet("font-size: 25pt")

            if False:
                self.widgets["server_lbl"] = QtWidgets.QLabel(self)
                self.widgets["server_lbl"].setText("Server:")
                self.widgets["server_lbl"].setStyleSheet("font-size: 10pt")
                self.widgets["server_lbl"].move(10, 240)
                self.widgets["server_lbl"].resize(500, 20)

                self.widgets["server_ln"] = QtWidgets.QLineEdit(self)
                self.widgets["server_ln"].move(10, 260)
                self.widgets["server_ln"].resize(200, 30)
                self.widgets["server_ln"].setStyleSheet("font-size: 10pt")

            self.widgets["finish_btn"] = QtWidgets.QPushButton(self)
            self.widgets["finish_btn"].move(60, 320)
            self.widgets["finish_btn"].resize(100, 50)
            self.widgets["finish_btn"].setText("Proceed")

            self.widgets["finish_btn"].clicked.connect(lambda x: self.submit())

            self.show()

        def submit(self):
            self.username = self.widgets["username_ln"].text()
            self.chr = self.widgets["chr_ln"].text()
            #self.servercode = self.widgets["server_ln"].text()

            self.pass_information()

        def pass_information(self):
            self.maingame.username = self.username
            self.maingame.chr = self.chr
            #self.maingame.servercode = self.servercode

            self.maingame.join_server()


class BoardUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(BoardUi, self).__init__()
        self.widgets = {}
        self.coords = {}
        self.dimensions = [900, 900]

        self.init_ui()

    def init_ui(self):
        self.resize(self.dimensions[0], self.dimensions[1])
        self.make_board(3,3)

    def make_board(self,xcount,ycount):
        xpercoord = (self.dimensions[0] / xcount)
        ypercoord = (self.dimensions[1] / ycount)
        for x in range(xcount):
            for y in range(ycount):
                self.coords[x, y] = Coord(self)
                self.coords[x, y].coordinates = [x, y]

                xloc = (x * xpercoord)
                yloc = (y * ypercoord)
                self.coords[x, y].move(xloc, yloc)
                self.coords[x, y].resize(self.dimensions[0] / xcount, self.dimensions[1] / ycount)

                self.coords[x, y].set_text("...")

        self.show()


class Client:
    def __init__(self, maingame):
        self.maingame = maingame
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.connect(("127.0.0.1", 12345))

    def send(self, clients_input):
        self.soc.send(clients_input.encode("utf8"))
        self.receive()

    def receive(self):
        result_bytes = self.soc.recv(4096)
        result_string = result_bytes.decode("utf8")

        return (result_string)

    def join(self):
        joincommand = "j"+ "." + self.maingame.username
        self.send(joincommand)


class Coord(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(Coord, self).__init__(parent)
        self.coordinates = []
        # Adding custom attributes to QtWidgets.QPushButton

    def set_text(self,text):
        self.setText(text)
        chrcount = str(int(200 / len(text)))
        self.setStyleSheet("font-size: "+chrcount+"pt ;")
        # This will set the text, and resize it appropriatly


def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()
