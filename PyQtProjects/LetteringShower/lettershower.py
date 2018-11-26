from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv
import random

class Options:
    def __init__(self):
        self.letter_size = 60
        #  Average font size
        #  In pt

        self.letter_size_mod = 50
        #  How much the font size can vary
        #  As a percentage of the average size

        self.window_size = (800, 800)


class SimUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(SimUi, self).__init__()
        self.setStyleSheet('''
            background-color: #FFFFFF;            
        ''')

        self.resize(800, 800)

        self.show()


class Simulation:
    def __init__(self):
        self.ui = SimUi()
        self.ui.keyPressEvent = self.keyPressEvent

        self.letters = []

    def keyPressEvent(self, e):
        if (64 < e.key() < 91) or (47 < e.key() < 59):
            self.add_letter(chr(e.key()).upper())
        else:
            print(e.key())

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

        self.font_size += int((random.randint(-self.options.letter_size_mod*self.font_size,self.options.letter_size_mod*self.font_size)) / 100)


        self.setStyleSheet('''
        color:''' + self.get_bright_color() + ''';
        font-size: '''+str(self.font_size)+'''pt;
        font-family: Arial Black;
        background-color: rgba(0,0 ,0, 0);
        ''')


        #self.
        self.resize(150,150)
        x = random.randint(0, self.options.window_size[0] - self.width()/2)
        y = random.randint(0, self.options.window_size[1] - self.height()/2)


        self.move(x, y)
        self.show()

    def get_bright_color(self):
        colors = ["0", "255", str(random.randint(0, 255))]
        random.shuffle(colors)

        toreturn = "rgba(" + colors[0]+","+colors[1]+","+colors[2]+ ",0.4 )"
        return toreturn



def main():
    app = QtWidgets.QApplication(argv)
    game = Simulation()
    app.exec_()


if __name__ == '__main__':
    main()