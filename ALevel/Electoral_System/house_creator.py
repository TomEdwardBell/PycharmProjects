# TODO: A GUI that allows people to create a house, create parties, candidates etc
# TODO: Ability to "auto create"
# TODO: View everything that you've created
# TODO: Import / Export all the info

from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv

class WidgetList(QtWidgets.QScrollArea):
    def __init__(self):
        super(WidgetList, self).__init__()
        self.scroller_height = 0
        self.widgets = []
        self.outer_size = (470, 500)

    def init_ui(self):
        #self.setWindowModality(QtCore.Qt.WindowModal)
        self.resize(self.outer_size[0], self.outer_size[1])

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.RL_Contents = QtWidgets.QWidget()
        self.RL_Contents.setMinimumSize(QtCore.QSize(0, 0))

        self.RL_Layout = QtWidgets.QWidget(self.RL_Contents)
        self.RL_Layout.resize(self.outer_size[0], self.outer_size[1])

        self.RL_VLayout = QtWidgets.QVBoxLayout(self.RL_Layout)
        self.RL_VLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.RL_VLayout.setContentsMargins(0, 0, 0, 0)
        self.RL_VLayout.setSpacing(0)

        self.setWidget(self.RL_Contents)
        self.show()

    def append(self, widgets):
        if type(widgets) != list:
            widgets = [widgets]
        for widget in widgets:
            widget.show()
            self.widgets.append(widget)
            self.scroller_height += widget.height()
            widget.setFixedSize(widget.width(), widget.height())
            self.RL_VLayout.addWidget(widget)

            widget.setStyleSheet("background-color:" + widget.bg_colors[len(self.widgets) % 2])

        self.RL_Contents.setMinimumSize(300, self.scroller_height)
        self.RL_Layout.setGeometry(QtCore.QRect(0, 0, self.outer_size[0], self.scroller_height))

class RegionViewer(WidgetList):



