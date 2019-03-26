from PyQt5 import QtCore, QtGui, QtWidgets
import electocalc_widgets
from sys import argv
from matplotlib import  pyplot

class View:
    def __init__(self):
        self.v = RepView()
        self.v.init_ui()
        self.v.show()

class RepList(QtWidgets.QScrollArea):
    # TODO: Add a filtering feature
    # TODO: Allow resizing
    def __init__(self):
        super(RepList, self).__init__()
        self.scroller_height = 0
        self.rep_panels = []
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
            self.rep_panels.append(widget)
            self.scroller_height += widget.height()
            widget.setFixedSize(widget.width(), widget.height())
            self.RL_VLayout.addWidget(widget)

            widget.setStyleSheet("background-color:"+widget.bg_colors[len(self.rep_panels) % 2])

        self.RL_Contents.setMinimumSize(300, self.scroller_height)
        self.RL_Layout.setGeometry(QtCore.QRect(0, 0, self.outer_size[0], self.scroller_height))


class RepView(QtWidgets.QWidget):
    # TODO: Rep's pictures
    # TODO: Make the label clickable buttons that take you to that parties page
    def __init__(self, window = None):
        if window is None:
            super(RepView, self).__init__()

        else:
            super(RepView, self).__init__(window)
        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setFamily('Bahnschrift Light')
        self.bg_colors = ["#FFFFFF", "#EEEEEE"]
        self.block_size = (450, 100)
    
    def init_ui(self):
        self.resize(self.block_size[0], self.block_size[1])

        self.PartyColor = QtWidgets.QLabel(self)
        self.PartyColor.setGeometry(QtCore.QRect(0, 0, 25, self.block_size[1]))
        #self.PartyColor.setFrameShape(QtWidgets.QFrame.WinPanel)
        #self.PartyColor.setFrameShadow(QtWidgets.QFrame.Raised)

        self.verticalLayoutWidget = QtWidgets.QWidget(self)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.NameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.NameLabel.setFont(self.font)

        self.verticalLayout.addWidget(self.NameLabel)
        self.PartyLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PartyLabel.setFont(self.font)

        self.verticalLayout.addWidget(self.PartyLabel)
        self.RegionLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.RegionLabel.setFont(self.font)
        self.verticalLayout.addWidget(self.RegionLabel)

        self.Picture = QtWidgets.QLabel(self)
        self.Picture.setGeometry(QtCore.QRect(25, 0, 100, self.block_size[1]))
        self.Picture.setStyleSheet("background-color: #333333")

        self.Line = QtWidgets.QFrame(self)
        self.Line.setGeometry(QtCore.QRect(0, 99, self.block_size[0], 1))
        self.Line.setFrameShape(QtWidgets.QFrame.HLine)

        self.setStyleSheet("background-color:" + self.bg_colors[0])


        self.verticalLayoutWidget.setGeometry(QtCore.QRect(130, 0, self.block_size[0] - self.PartyColor.width() - self.Picture.width(), self.block_size[1]))


    def setPartyColor(self, color):
        self.PartyColor.setStyleSheet("background-color:" + color)

    def setName(self, name):
        self.NameLabel.setText(name)

    def setPartyName(self, name):
        self.PartyLabel.setText(name)

    def setRegionName(self, name):
        self.RegionLabel.setText(name)

    def setPicture(self, filename):
        pixmap = QtGui.QPixmap(filename)
        self.Picture.setPixmap(pixmap)

def view_rep(rep, window = None):
    if window is None:
        repview = RepView()
    else:
        repview = RepView(window)
    repinfo = {}
    repinfo["name"] = rep.name
    repinfo["party_name"] = rep.party.name
    repinfo["party_color"] = rep.party.color
    repinfo["region_name"] = rep.region.name

    repview.init_ui()
    repview.setName(repinfo["name"])
    repview.setPartyName(repinfo["party_name"])
    repview.setPartyColor(repinfo["party_color"])
    repview.setRegionName(repinfo["region_name"])
    repview.show()
    return repview

def view_house(house):
    houseview = RepList()
    houseview.init_ui()
    rep_views = [view_rep(region.winner, houseview) for region in house]
    houseview.append(rep_views)
    return houseview
