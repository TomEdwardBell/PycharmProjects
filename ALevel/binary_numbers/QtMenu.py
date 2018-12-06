from PyQt5 import QtWidgets
from sys import argv
import random
import converter


class WelcomeScreen(QtWidgets.QMainWindow):
    def __init__(self, mainapp):
        super(WelcomeScreen, self).__init__()
        self.mainapp = mainapp

        self.resize(500, 500)
        self.setStyleSheet('''
            background-color:#FF00FF;
            color: #000000
        ''')

        self.title = QtWidgets.QLabel(self)
        self.title.resize(500, 300)
        self.title.move(0, 100)
        self.setStyleSheet('''
            font-size: 50px;
        ''')
        self.show()


class Menu(QtWidgets.QMainWindow):
    pass

class MainApp():
    def __init__(self):
        self.welcome = WelcomeScreen(self)

def main():
    app = QtWidgets.QApplication(argv)
    mainapp = MainApp()
    app.exec_()


if __name__ == '__main__':
    main()