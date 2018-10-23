from PyQt5 import QtWidgets
from sys import argv

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.show()

def main():
    app = QtWidgets.QApplication(argv)
    game = MainWindow()
    app.exec_()


if __name__ == '__main__':
    main()