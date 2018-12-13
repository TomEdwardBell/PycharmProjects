from PyQt5 import QtWidgets, QtCore, QtGui
from sys import argv
import random
import converter

class Options():
    def __init__(self):
        self.options_menu_button_border = (10, 30)


class WelcomeScreen(QtWidgets.QStackedWidget):
    def __init__(self, mainapp):
        super(WelcomeScreen, self).__init__()
        self.mainapp = mainapp

        self.welcome = QtWidgets.QMainWindow()
        self.addWidget(self.welcome)

        self.gameModeMenu = QtWidgets.QMainWindow()
        self.addWidget(self.gameModeMenu)

        self.setWelcome()

        self.show()
    
    def setWelcome(self):
        self.setCurrentIndex(0)
        self.resize(500, 500)
        self.welcome.setStyleSheet('''
            background-color:#000000;
            color: #00FF00;
        ''')

        self.welcome.title = QtWidgets.QLabel(self.welcome)
        self.welcome.title.resize(500, 500)
        self.welcome.title.move(0, 0)
        self.welcome.title.setStyleSheet('''font-size: 50px''')
        self.welcome.title.setText('Super\nAwesome\nBinary\nEducation\nTool')
        self.welcome.title.setFont(QtGui.QFont("Consolas"))
        self.welcome.title.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)

        self.welcome.play_button = QtWidgets.QPushButton(self.welcome)
        self.welcome.play_button.resize(200, 70)
        self.welcome.play_button.move(int(500/2 - 200 / 2), 400)
        self.welcome.play_button.setStyleSheet('''
            background-color:#00AA00;
            color: #000000;
            font-size: 40px;
        ''')
        self.welcome.play_button.setText("Play")
        self.welcome.play_button.setFont(QtGui.QFont("Consolas"))
        style = QtWidgets.QStyleFactory.create('Fusion')
        self.welcome.play_button.setStyle(style)
        self.setStyle(style)

        self.welcome.play_button.clicked.connect(self.setGameModeMenu)

    def setGameModeMenu(self):
        self.setCurrentIndex(1)
        self.resize(700, 500)
        g = self.gameModeMenu
        g.setStyleSheet('''
            background-color:#000000;
            color: #00FF00;
        ''')
        g.text = QtWidgets.QLabel(g)
        g.text.move(0, 0)
        g.text.resize(700, 50)
        g.text.setStyleSheet('''font-size: 40px; color: #00FF00; background-color:#000000''')
        g.text.setText('Select Game Mode')
        g.text.setFont(QtGui.QFont("Consolas"))
        g.text.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
        g.text.show()

        gm_btns = []
        h = g.height() - g.text.height()
        hper = int(h / len(self.mainapp.gamemodes))
        for gm in range(len(self.mainapp.gamemodes)):
            gm_btns.append(QtWidgets.QPushButton(g))
            bh = int(hper * (2/3))
            by = int((gm)*hper) + g.text.height() + (hper - bh)
            gm_btns[gm].setGeometry(0, by, g.width(), bh)
            print(gm_btns[gm], gm, gm_btns[gm].x(), gm_btns[gm].y())

            btn_width = self.width


            gm_btns[gm].setStyleSheet("background-color: #00FF00;")
            gm_btns[gm].setText(str(gm))

            gm_btns[gm].show()





class Game:
    pass

class MainApp():
    def __init__(self):
        self.welcome = WelcomeScreen(self)
        self.main = Game()
        self.gamemodes = ["Binary --> Dec", "Dec --> Binary", "Binary --> Hexadecimal", "Hexadecimal --> Binary", "LOL"]

    def openMainGame(self):
        self.maingame

def main():
    app = QtWidgets.QApplication(argv)
    mainapp = MainApp()
    app.exec_()


if __name__ == '__main__':
    main()