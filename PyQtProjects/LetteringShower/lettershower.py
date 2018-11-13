from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv
import random

class Options:
    def __init__(self):
        self.letter_size = 50
        #  Average font size
        #  In pt

        self.letter_size_mod = 30
        #  How much the font size can vary
        #  As a percentage of the average size

        self.window_size = (800, 800)


class SimUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SimUi, self).__init__()

        print("H")
        self.setStyleSheet('''
            background-color: #FFFFFF;            
        ''')

        self.resize(800,800)

        self.show()


class Simulation:
    def __init__(self):
        self.ui = SimUi()
        self.ui.keyPressEvent = self.keyPressEvent

        self.letters = []

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_A:
            self.add_letter("a")

    def add_letter(self, letter):
        l = Letter(self.ui, letter)
        self.letters.append(l)
        l.decorate()



class Letter(QtWidgets.QLabel):
    def __init__(self,ui, text):
        super(Letter, self).__init__(ui)
        self.options = Options()

        self.setText(text)

    def decorate(self):
        self.font_size = self.options.letter_size

        print("JIO")
        self.font_size += int((random.randint(-self.options.letter_size_mod*self.font_size,self.options.letter_size_mod*self.font_size)) / 100)

        print(self.font_size)

        self.setStyleSheet('''
        color: rgba(255,0,0,0.5);
        font-size: '''+str(self.font_size)+'''pt;
        background-color: rgba(0,0 ,0, 0);
        ''')


        #self.
        self.resize(100,100)
        x = random.randint(0, self.options.window_size[0] - self.width())
        y = random.randint(0, self.options.window_size[1] - self.height())


        self.move(x, y)
        self.show()


def main():
    app = QtWidgets.QApplication(argv)
    game = Simulation()
    app.exec_()


if __name__ == '__main__':
    main()