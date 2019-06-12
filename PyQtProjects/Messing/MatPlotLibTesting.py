import sys

from PyQt5 import QtWidgets, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 400)
        canvas = PlotCanvas(self, width = 5, height = 4)


class PlotCanvas(FigureCanvas):