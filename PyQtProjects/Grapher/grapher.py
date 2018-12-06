from PyQt5 import QtWidgets
from sys import argv

class Grapher:
    def __init__(self):
        vis = []
        eq = ""
        while eq != "-1":
            eq = input("Equation: ")
            vis.append(Visualiser(eq))

class Visualiser(QtWidgets.QMainWindow):
    def __init__(self, equation):
        super(Visualiser, self).__init__()
        print(equation, equation[:2], equation[2:])
        nums = ["0", "1" "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        current_number = ""
        gradient = 0
        for char in equation[2:]:
            print(".."+ char)
            if char in nums:
                current_number += char
            elif char == "-" and current_number != "":
                current_number += "-"
            elif char == "x":
                print("OP")
                if current_number == "":
                    gradient = 1
                elif current_number == "-":
                    gradient = -1
                else:
                    gradient = int(current_number)
            elif char not in nums:
                current_number = ""
        print("cur" + str(current_number), "gra" + str(gradient))


def main():
    app = QtWidgets.QApplication(argv)
    game = Grapher()
    app.exec_()


if __name__ == '__main__':
    main()