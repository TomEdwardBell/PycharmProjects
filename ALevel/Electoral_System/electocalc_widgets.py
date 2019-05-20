from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv
from matplotlib import  pyplot
import electocalc as e

class WidgetList(QtWidgets.QScrollArea):
    def __init__(self, parent = None):
        if parent is None:
            super(WidgetList, self).__init__()
        else:
            super(WidgetList, self).__init__(parent)
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

           # widget.setStyleSheet("background-color:" + widget.bg_colors[len(self.widgets) % 2])

        self.RL_Contents.setMinimumSize(300, self.scroller_height)
        self.RL_Layout.setGeometry(QtCore.QRect(0, 0, self.outer_size[0], self.scroller_height))

    def _resize(self, w, h):
        self.resize(w, h)
        self.RL_Layout.resize(w, self.RL_Layout.height())
        self.RL_Contents.resize(w, self.RL_Contents.height())
        [wid.resize(w, wid.height()) for wid in self.widgets]

    def clear(self): # Removes all the widgets in the list
        for widget in self.widgets:
            widget.destroy()


class RepView(QtWidgets.QWidget):
    # TODO: Rep's pictures
    # TODO: Make the label clickable buttons that take you to that parties page
    def __init__(self, window = None, rep = None):
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
    houseview = WidgetList()
    houseview.init_ui()
    rep_views = [view_rep(region.winner, houseview) for region in house]
    houseview.append(rep_views)
    return houseview

class RegionScroller(WidgetList):
    # A list of all the regions
    # When you click a region the region viewer window changes to show the info about that region
    def __init__(self, parent = None):
        super(RegionScroller, self).__init__(parent)
        self.RegionViewer = None
        # The pointer to the thing that lets you view the details of a region
        self.init_ui()
        self._resize(400, 300)
        self.addButton = QtWidgets.QPushButton(self)

    def add(self, region):
        regionbutton = QtWidgets.QPushButton(self)
        regionbutton.setText(region.name)
        regionbutton.resize(self.width(), 30)

        self.append(regionbutton)
        regionbutton.clicked.connect(lambda state, c = region: self.RegionViewer.set_region(region))

    def setHouse(self, house):
        # Sets all the widgets to those in the new house
        self.clear()
        for region in house:
            self.add(region)


class HouseCreator(QtWidgets.QTableWidget):
    def __init__(self):
        super(HouseCreator, self).__init__()
        self.show()

class RegionViewer(QtWidgets.QWidget):
    def __init__(self):
        super(RegionViewer, self).__init__()
        self.current_region = None

        self.Region_Form = QtWidgets.QFormLayout(self)
        self.Region_Form.setContentsMargins(0, 0, 0, 0)
        self.Region_Form.setObjectName("Region_Form")

        self.NameLbl = QtWidgets.QLabel(self)
        self.NameLbl.setText("Name: ")
        self.Region_Form.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.NameLbl)

        self.PopLbl = QtWidgets.QLabel(self)
        self.PopLbl.setText("Population: ")
        self.Region_Form.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.PopLbl)

        self.NameEdit = QtWidgets.QLineEdit(self)
        self.Region_Form.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.NameEdit)

        self.PopEdit = QtWidgets.QSpinBox(self)
        self.PopEdit.setMinimum(1)
        self.PopEdit.setMaximum(100000)
        self.Region_Form.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.PopEdit)

        self.UpdateButton = QtWidgets.QPushButton(self)
        self.Region_Form.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.UpdateButton)
        self.UpdateButton.setText("Update")
        self.UpdateButton.clicked.connect(self.update_region)

    def set_region(self, region):
        # Change the current region
        self.current_region = region
        self.NameEdit.setText(region.name)
        self.PopEdit.setProperty("value", (len(region)))

    def update_region(self):
        self.current_region.setName(self.NameEdit.text())
        self.current_region.setPopulation(self.PopEdit.value())

class Runn():
    def __init__(self):
        self.regions = RegionScroller()
        [self.regions.add(e.gen_region(500, 3)) for i in range(20)]

        self.region_viewer = RegionViewer()
        self.region_viewer.show()
        self.regions.RegionViewer = self.region_viewer


def main():
    app = QtWidgets.QApplication(argv)
    t = Runn()
    app.exec_()

if __name__ == '__main__':
    main()
