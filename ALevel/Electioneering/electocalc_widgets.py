from PySide2 import QtCore, QtGui, QtWidgets
from sys import argv
import random
import time
from collections import Counter

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import electioneering as e

class WidgetList(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(WidgetList, self).__init__()
        if parent is not None:
            self.setParent(parent)
        self.scroller_height = 0
        self.widgets = []
        self.outer_size = (10, 20)

    def init_ui(self):
        super(WidgetList, self).resize(self.outer_size[0], self.outer_size[1])
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setWidgetResizable(True)
        self.RL_Contents = QtWidgets.QWidget(self)
        self.RL_Contents.setMinimumSize(QtCore.QSize(0, 0))
        pol = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.RL_Contents.setSizePolicy(pol)
        self.setSizePolicy(pol)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.RL_VLayout = QtWidgets.QVBoxLayout(self.RL_Contents)
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

            #widget.setStyleSheet('background-color:' + widget.bg_colors[len(self.widgets) % 2])

    def resize(self, w, h):
        super(WidgetList, self).resize(w, h)
        self.outer_size = (w, h)
        self.RL_Contents.resize(w, self.RL_Contents.height())
        for wid in self.widgets: wid.resize(w - 10, wid.height())

    def clear(self): # Removes all the widgets in the list
        for widget in self.widgets:
            widget.destroy()

    def __getitem__(self, item):
        return self.widgets[item]


class PartiesList(WidgetList):
    def __init__(self, mode, local_parties, national_parties, region=None):
        super(PartiesList, self).__init__()
        self.outer_size = (700, 600)
        self.mode = mode
        self.region = region

        self.init_ui()
        self.move(500, 500)

        if mode == 'edit':
            self.addbutton = QtWidgets.QPushButton(self)
            self.addbutton.setText('+')
            self.addbutton.setFont(QtGui.QFont('Arial', 60))
            self.addbutton.resize(100, 100)
            self.append(self.addbutton)
            self.addbutton.clicked.connect(self.addparty)
        elif mode == 'select':
            self.selected_party = False

        national_parties_label = QtWidgets.QLabel("National Parties: ")
        national_parties_label.setFont(QtGui.QFont('Arial', 20))
        self.append(national_parties_label)
        for party in national_parties:
            self.append(PartiesList.PartyButton(party, self))

        local_parties_label = QtWidgets.QLabel("Local Parties: ")
        local_parties_label.setFont(QtGui.QFont('Arial', 20))
        self.append(local_parties_label)
        for party in local_parties:
            self.append(PartiesList.PartyButton(party, self))

    def addparty(self):
        party = e.Party(region=self.region)
        self.region.local_parties.append(party)
        self.append(PartiesList.PartyButton(party, self))

    class PartyButton(QtWidgets.QPushButton):
        def __init__(self, party ,ui):
            super(PartiesList.PartyButton, self).__init__(ui)
            self.party = party
            self.setText(party.name)

            self.setIcon(ColorIcon(party.color))
            self.region = ui.region
            self.ui = ui

            if ui.mode == "edit":
                self.clicked.connect(self.editparty)
            elif ui.mode == "select":
                self.clicked.connect(self.selectparty)

        def editparty(self):
            self.edit = PartiesList.PartyEdit(self.party)
            self.edit.donebutton.clicked.connect(self.update_button)

        def update_button(self):
            self.setText(self.party.name)
            self.setIcon(ColorIcon(self.party.color))
            self.edit.destroy()

        def selectparty(self):
            self.ui.selected_party = self.party
            self.ui.done = True


    class PartyEdit(QtWidgets.QWidget):
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setFamily('Bahnschrift Light')

        def __init__(self, party=None, ui=None):
            super(PartiesList.PartyEdit, self).__init__()
            if ui is not None:
                self.setParent(ui)
            if party is None:
                party = e.Party()
                party.name = ""
                party.leaning = (0, 0)
                party.color = "#FFFFFF"
                party.relevance = 1
            self.party = party

            self.layout = QtWidgets.QFormLayout()
            self.setLayout(self.layout)
            self.init_ui()

        def init_ui(self):
            self.setGeometry(QtCore.QRect(0, 0, 300, 300))

            self.namelabel = QtWidgets.QLabel('Name:')
            self.layout.setWidget(0, self.layout.LabelRole, self.namelabel)
            self.nameedit = QtWidgets.QLineEdit(self.party.name)
            self.layout.setWidget(0, self.layout.FieldRole, self.nameedit)

            self.leaninglabel = QtWidgets.QLabel('Leaning:')
            self.layout.setWidget(1, self.layout.LabelRole, self.leaninglabel)

            self.leaninglayout = QtWidgets.QHBoxLayout()
            self.leaningedit0 = QtWidgets.QDoubleSpinBox()
            self.leaningedit0.setMinimum(-5)
            self.leaningedit0.setMaximum(5)
            self.leaningedit0.setDecimals(3)
            self.leaningedit0.setValue(self.party.leaning[0])
            self.leaninglayout.addWidget(self.leaningedit0)
            self.leaningedit1 = QtWidgets.QDoubleSpinBox()
            self.leaningedit1.setMinimum(-5)
            self.leaningedit1.setMaximum(5)
            self.leaningedit1.setDecimals(3)
            self.leaningedit1.setValue(self.party.leaning[1])
            self.leaninglayout.addWidget(self.leaningedit1)
            self.layout.setLayout(1, self.layout.FieldRole, self.leaninglayout)

            self.relevancelabel = QtWidgets.QLabel('Relevance: ')
            self.layout.setWidget(2, self.layout.LabelRole, self.relevancelabel)
            self.relevanceedit = QtWidgets.QDoubleSpinBox()
            self.relevanceedit.setMinimum(0)
            self.relevanceedit.setMaximum(5)
            self.relevanceedit.setDecimals(3)
            self.relevanceedit.setValue(self.party.relevance)
            self.layout.setWidget(2, self.layout.FieldRole, self.relevanceedit)

            self.colorlabel = QtWidgets.QLabel('Color: ')
            self.layout.setWidget(3, self.layout.LabelRole, self.colorlabel)

            self.coloredit = QtWidgets.QPushButton(self.party.color)
            self.coloredit.clicked.connect(self.setcolor)
            if QtGui.QColor(self.party.color).lightness() < 150:
                self.coloredit.setStyleSheet(f'background-color:{self.party.color}; color:#FFFFFF')
            else:
                self.coloredit.setStyleSheet(f'background-color:{self.party.color}; color:#000000')
            self.layout.setWidget(3, self.layout.FieldRole, self.coloredit)

            self.donebutton = QtWidgets.QPushButton('Done')
            self.donebutton.clicked.connect(self.save)
            self.layout.setWidget(4, self.layout.SpanningRole, self.donebutton)

            self.show()

        def setcolor(self):
            color = QtWidgets.QColorDialog.getColor(QtGui.QColor(self.party.color))
            self.coloredit.setText(color.name())
            self.coloredit.setStyleSheet('background-color:' + color.name())
            if color.lightness() < 100:
                self.coloredit.setStyleSheet(f'background-color:{color.name()}; color:#FFFFFF')
            else:
                self.coloredit.setStyleSheet(f'background-color:{color.name()}; color:#000000')

        def save(self):
            self.party.name = self.nameedit.text()
            self.party.leaning = float(self.leaningedit0.text()), float(self.leaningedit1.text())
            self.party.relevance = float(self.relevanceedit.text())
            self.party.color = str(self.coloredit.text())
            self.destroy()


class RepsList(WidgetList):
    def __init__(self, reps = [], ui = None):
        super(RepsList, self).__init__()
        if ui is not None:
            self.setParent(ui)

        self.reps = reps

    def init_ui(self):
        super(RepsList, self).init_ui()
        self.setStyleSheet('background-color: #777777')
        self.views = [RepView(self, rep) for rep in self.reps]
        for v in self.views:
            v.init_ui()
            v.show()
        self.append(self.views)


class ColorIcon(QtGui.QIcon):
    def __init__(self, color):
        pixmap = QtGui.QPixmap(100, 100)
        pixmap.fill(QtGui.QColor(color))
        super(ColorIcon, self).__init__(pixmap)


class CandEdit(QtWidgets.QWidget):
    font = QtGui.QFont()
    font.setPointSize(12)
    font.setFamily('Bahnschrift Light')

    def __init__(self, candidate=None, ui = None):
        super(CandEdit, self).__init__()
        if ui is not None:
            self.setParent(ui)
        if candidate is None:
            self.candidate = e.Candidate()
        self.ui = ui
        self.candidate = candidate
        self.layout = QtWidgets.QFormLayout()
        self.setLayout(self.layout)
        self.init_ui()
        self.show()


    def init_ui(self):
        if self.ui is None:
            self.setGeometry(QtCore.QRect(800, 500, 300, 300))
        else:
            self.setGeometry(QtCore.QRect(self.ui.x(), self.ui.y(), 300, 300))

        self.namelabel = QtWidgets.QLabel('Name:')
        self.layout.setWidget(0, self.layout.LabelRole, self.namelabel)
        self.nameedit = QtWidgets.QLineEdit(self.candidate.name)
        self.layout.setWidget(0, self.layout.FieldRole, self.nameedit)


        self.leaninglabel = QtWidgets.QLabel('Leaning:')
        self.layout.setWidget(1, self.layout.LabelRole, self.leaninglabel)

        self.leaninglayout = QtWidgets.QHBoxLayout()
        self.leaningedit0 = QtWidgets.QLineEdit(str(round(self.candidate.leaning[0], 3)))
        self.leaningedit1 = QtWidgets.QLineEdit(str(round(self.candidate.leaning[1], 3)))
        self.leaninglayout.addWidget(self.leaningedit0)
        self.leaninglayout.addWidget(self.leaningedit1)
        self.layout.setLayout(1, self.layout.FieldRole, self.leaninglayout)

        self.relevancelabel = QtWidgets.QLabel('Relevance: ')
        self.layout.setWidget(2, self.layout.LabelRole, self.relevancelabel)
        self.relevanceedit = QtWidgets.QLineEdit(str(round(self.candidate.relevance, 3)))
        self.layout.setWidget(2, self.layout.FieldRole, self.relevanceedit)

        self.partylabel = QtWidgets.QLabel('Party')
        self.layout.setWidget(3, self.layout.LabelRole, self.partylabel)
        self.partybutton = QtWidgets.QPushButton(self.candidate.party.name)
        self.partybutton.setIcon(ColorIcon(self.candidate.party.color))
        self.layout.setWidget(3, self.layout.FieldRole, self.partybutton)
        self.partybutton.clicked.connect(self.select_party)

        self.donebutton = QtWidgets.QPushButton('Done')
        self.donebutton.clicked.connect(self.save)
        self.layout.setWidget(4, self.layout.SpanningRole, self.donebutton)

    def save(self):
        invalids = []
        if self.nameedit.text() == "":
            invalids.append(self.nameedit)
        try:
            float(self.leaningedit0.text())
        except:
            invalids.append(self.leaningedit0)

        try:
            float(self.leaningedit1.text())
        except:
            invalids.append(self.leaningedit0)

        try:
            float(self.relevanceedit.text())
        except:
            invalids.append(self.relevanceedit)

        if not invalids:
            self.candidate.name = self.nameedit.text()
            self.candidate.leaning = float(self.leaningedit0.text()), float(self.leaningedit1.text())
            self.candidate.relevance = float(self.relevanceedit.text())
            self.destroy()
        else:
            for widget in invalids:
                widget.setStyleSheet('color: #FF0000')

    def select_party(self):
        if self.candidate.region.nation is not None:
            partylist = PartiesList('select', self.candidate.region.local_parties, self.candidate.region.nation.parties)
        else:
            partylist = PartiesList('select', self.candidate.region.local_parties, [])
        while not partylist.selected_party:
            time.sleep(0.05)
            QtWidgets.QApplication.processEvents()
        partylist.destroy()
        self.candidate.party = partylist.selected_party
        self.partybutton.setText(self.candidate.party.name)
        self.partybutton.setIcon(ColorIcon(self.candidate.party.color))


class RepView(QtWidgets.QWidget):
    # TODO: Make the label clickable buttons that take you to that parties page
    def __init__(self, window = None, rep = None):
        if window is None:
            super(RepView, self).__init__()
        else:
            super(RepView, self).__init__(window)

        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setFamily('Bahnschrift Light')
        self.bg_colors = ['#FFFFFF', '#EEEEEE']
        self.block_size = (800, 200)

        if rep is not None or True:
            self.rep = rep
            self.init_ui()

    def init_ui(self):
        # self.resize(self.block_size[0], self.block_size[1])

        self.PartyColor = QtWidgets.QLabel(self)
        self.PartyColor.setGeometry(QtCore.QRect(0, 0, 40, self.block_size[1]))
        # self.PartyColor.setFrameShape(QtWidgets.QFrame.WinPanel)
        # self.PartyColor.setFrameShadow(QtWidgets.QFrame.Raised)

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

        self.Line = QtWidgets.QFrame(self)
        self.Line.setGeometry(QtCore.QRect(0, self.block_size[1] -1, self.block_size[0], 1))
        self.Line.setFrameShape(QtWidgets.QFrame.HLine)

        self.setStyleSheet('background-color:' + self.bg_colors[0])

        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(40, 0, self.block_size[0] - self.PartyColor.width(), self.block_size[1]))

        self.setName(self.rep.name)
        self.setPartyName(self.rep.party.name)
        self.setPartyColor(self.rep.party.color)
        try:
            self.setRegionName(self.rep.region.name)
        except:
            pass


    def setPartyColor(self, color):
        self.PartyColor.setStyleSheet('background-color:' + color)

    def setName(self, name):
        self.NameLabel.setText(name)

    def setPartyName(self, name):
        self.PartyLabel.setText(name)

    def setRegionName(self, name):
        self.RegionLabel.setText(name)


    def resize(self, x, y):
        super(RepView, self).resize(x, y)
        self.block_size = x, y
        self.init_ui()


class RegionElectionRunner():
    def __init__(self, **kwargs):
        if 'region' in kwargs:
            self.election = e.RegionElection(region=kwargs['region'])
        else:
            self.election = e.RegionElection()

        self.vs = ""
        self.vs_chooser = RegionElectionRunner.VotingSystemChooser(self, self.election)
        self.vs_chooser
        while not self.vs_chooser.done:
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)

        self.election.voting_system = self.vs_chooser.vs
        if self.election.voting_system in self.election.candidatesystems or self.election.voting_system in self.election.partylistsystems:
            self.vs_chooser.destroy()
            self.election_options = RegionElectionRunner.ElectionOptions(self.election)
            self.election_options.done = False
            self.election_options.show()
            while not self.election_options.done:
                QtWidgets.QApplication.processEvents()
                time.sleep(0.05)

    class ElectionOptions(QtWidgets.QWidget):
        def __init__(self, election):
            super(RegionElectionRunner.ElectionOptions, self).__init__()
            self.layout = QtWidgets.QFormLayout()
            self.setLayout(self.layout)
            self.election = election
            self.done = False

            self.voting_systemlabel = QtWidgets.QLabel("Voting System: ")
            self.layout.setWidget(0, self.layout.LabelRole, self.voting_systemlabel)
            self.voting_systemfield = QtWidgets.QLabel(self.election.voting_system)
            self.layout.setWidget(0, self.layout.FieldRole, self.voting_systemfield)

            self.repsnumlabel = QtWidgets.QLabel("Number of Seats")
            self.layout.setWidget(1, self.layout.LabelRole, self.repsnumlabel)
            self.repsnumspinbox = QtWidgets.QSpinBox(self)
            self.repsnumspinbox.setMinimum(1)
            self.repsnumspinbox.setMaximum(20)
            self.repsnumspinbox.setValue(self.election.region.seat_count)
            self.layout.setWidget(1, self.layout.FieldRole, self.repsnumspinbox)

            if election.voting_system in ['runoff', 'stv', 'borda', 'dowdall', 'fptp']:
                self.candslabel = QtWidgets.QLabel("Candidates")
                self.layout.setWidget(2, self.layout.LabelRole, self.candslabel)
                self.candsbutton = QtWidgets.QPushButton("Click to view candidates")
                self.candsbutton.clicked.connect(self.loadcandslist)
                self.layout.setWidget(2, self.layout.FieldRole, self.candsbutton)

            elif election.voting_system in ['dhont', 'webster']:
                self.partieslabel = QtWidgets.QLabel("Parties")
                self.layout.setWidget(2, self.layout.LabelRole, self.partieslabel)
                self.partiesbutton = QtWidgets.QPushButton("Click to edit Parties")
                self.partiesbutton.clicked.connect(self.loadpartieslist)
                self.layout.setWidget(2, self.layout.FieldRole, self.partiesbutton)

            self.runbutton = QtWidgets.QPushButton('Run')
            self.runbutton.clicked.connect(self.runelection)
            self.layout.setWidget(3, self.layout.FieldRole, self.runbutton)

            self.resize(100, 100)

        def runelection(self):
            if self.election.voting_system in self.election.candidatesystems:
                if len(self.election.candidates) < self.repsnumspinbox.value():
                    self.candsbutton.setStyleSheet('color: #FF0000')
                    self.candsbutton.setText('Not enough candidates')
                    return False
            self.done = True
            self.election.region.seat_count = self.repsnumspinbox.value()
            self.election.run()

            self.destroy()


        def loadcandslist(self):
            self.candslist = self.CandsList(self.election)
            for candidate in self.election.candidates:
                self.candslist.append(self.CandButton(candidate))

        def loadpartieslist(self):
            if self.region.nation is not None:
                self.partieslist = PartiesList('edit', self.region.local_parties, self.region.nation.parties, self.region)
            else:
                self.partieslist = PartiesList('edit', self.region.local_parties, [], self.region)

        class CandButton(QtWidgets.QPushButton):
            def __init__(self, candidate):
                super(RegionElectionRunner.ElectionOptions.CandButton, self).__init__()
                self.hide()
                self.candidate = candidate
                self.edit = None
                self.resize(300, 100)
                self.setText(candidate.name)
                self.clicked.connect(self.editcand)

            def editcand(self):
                if self.edit is not None:
                    self.edit.destroy()
                    self.edit = None
                self.edit = CandEdit(self.candidate)
                self.edit.donebutton.clicked.connect(lambda candidate=self.candidate: [
                    self.edit.save(),
                    self.setText(self.candidate.name)])
                self.setText(self.candidate.name)

        class CandsList(WidgetList):
            def __init__(self, election):
                super(RegionElectionRunner.ElectionOptions.CandsList, self).__init__()
                self.outer_size = (320, 500)
                self.init_ui()
                self.election = election
                self.addbutton = QtWidgets.QPushButton('Add Candidate')
                self.addbutton.clicked.connect(self.addcand)
                self.append(self.addbutton)

            def addcand(self):
                candidate = e.Candidate(region=self.election.region)
                self.election.candidates.append(candidate)
                candbutton = RegionElectionRunner.ElectionOptions.CandButton(candidate)
                self.append(candbutton)


    class VotingSystemButton(QtWidgets.QPushButton):
        def __init__(self, vs, widgetlist):
            super(RegionElectionRunner.VotingSystemButton, self).__init__(widgetlist)
            self.setText(vs)
            self.resize(500, 100)
            self.clicked.connect(lambda: widgetlist.clicked(vs))

    class VotingSystemChooser(WidgetList):
        def __init__(self, parent_ui, election):
            super(RegionElectionRunner.VotingSystemChooser, self).__init__()
            self.init_ui()
            self.done = False
            vs_names = list(election.candidatesystems.keys()) + list(election.partylistsystems.keys())
            self.resize(500, 700)
            buttons = []
            for vs in vs_names:
                buttons.append(RegionElectionRunner.VotingSystemButton(vs, self))
                self.append(buttons[-1])

        def clicked(self, vs):
            self.vs = vs
            self.done = True


class NationViewer(QtWidgets.QWidget):
    map_width = 1000
    map_height = 1000
    side_bar_width = 200

    class SideBar(WidgetList):
        def __init__(self):
            pass

    def __init__(self, nation=None):
        super(NationViewer, self).__init__()
        if nation is None:
            nation = e.Nation()

        self.nation = nation
        self.map = NationMap(nation.region_map)
        self.map.setParent(self)
        self.map.move(0, 0)
        self.map.setFixedSize(self.map_width, self.map_height)

        self.resize(self.map_width + self.side_bar_width, self.map_height)
        self.add_region_button = QtWidgets.QPushButton(self)
        self.add_region_button.setText('Add Region')
        self.add_region_button.setGeometry(self.map_width, 0, self.side_bar_width, 100)
        self.add_region_button.clicked.connect(self.add_region)

        self.show()

    def add_region(self):
        self.nation.create_regions(1)
        self.map.refresh()




class NationMap(QtWidgets.QScrollArea):
    width = 500
    height = 500

    def __init__(self, region_map):
        super(NationMap, self).__init__()
        self.layout = QtWidgets.QGridLayout()
        self.layout.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.layout.setSpacing(5)
        self.buttons = []
        self.region_map = region_map

        self.refresh()

        self.setLayout(self.layout)
        self.show()


    def refresh(self):
        for button in self.buttons:
            button.destroy()
        for (x, y) in self.region_map:
            if self.region_map[(x, y)] is not None:
                region = self.region_map[(x, y)]
                self.buttons.append(NationMap.RegionButton(region, self))
                self.layout.addWidget(self.buttons[-1], y, x)


    class RegionButton(QtWidgets.QPushButton):
        def __init__(self, region, ui):
            super(NationMap.RegionButton, self).__init__()
            self.view = None
            self.region = region

            policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            policy.setHeightForWidth(True)
            self.setSizePolicy(policy)

            name = region.name
            name = name.replace(' ', '\n')
            self.setText(name)

            self.setMinimumSize(100, 100)

            self.clicked.connect(self.view_region)

        def view_region(self):
            self.regionviewer = RegionViewer(self.region)

        def paintEvent(self, e):
            colors = [rep.party.color for rep in self.region.reps]
            total_rects = len(colors)
            color_count = dict(Counter(colors))

            qp = QtGui.QPainter()
            qp.begin(self)
            c = 0
            if total_rects != 0:
                w = int(self.width() / total_rects)
                for color in color_count.keys():
                    col = QtGui.QColor(color)
                    qp.setPen(col)

                    qp.setBrush(col)
                    qp.setPen(col)

                    qp.setBrush(QtGui.QColor(col))
                    qp.drawRect(c * w, 0, w * color_count[color], self.height())
                    c += color_count[color]

            text_pen = QtGui.QPen()
            if total_rects == 0:
                text_pen.setColor(QtGui.QColor('#000000'))
            else:
                text_pen.setColor(QtGui.QColor('#FFFFFF'))
            text_font = QtGui.QFont('Arial Black', int(min(self.width(), self.height())/20))
            qp.setFont(text_font)
            qp.setPen(text_pen)
            name = self.region.name
            name = name.replace(' ', '\n')
            self.setText(name)
            qp.drawText(e.rect(), QtGui.Qt.AlignCenter, name)

            black_pen = QtGui.QPen()
            black_pen.setColor(QtGui.QColor('#000000'))
            black_pen.setWidth(int(self.width()/10))
            qp.setPen(black_pen)
            qp.setBrush(QtGui.QColor(0, 0, 0, 0))
            qp.drawRect(0, 0, self.width(), self.height())
            qp.end()

    def do_resize(self, x, y):
        pass


class RegionViewer(QtWidgets.QWidget):
    c1_width = 700
    # Width of column one (Contains basic info and list of elections)
    c2_width = 700

    basic_info_height = 400
    electionlist_height = 450
    replist_height = basic_info_height + electionlist_height

    font = QtGui.QFont()
    font.setPointSize(12)
    font.setFamily('Bahnschrift Light')

    class BasicInfo(QtWidgets.QFormLayout):
        def __init__(self, region, ui):
            super(RegionViewer.BasicInfo, self).__init__(ui)
            self.region = region

            self.name_label = QtWidgets.QLabel()
            self.name_label.setText("Name")
            self.name_label.setFont(RegionViewer.font)
            self.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.name_label)
            self.name_edit = QtWidgets.QLineEdit()
            self.name_edit.setText(region.name)
            self.name_edit.setFont(RegionViewer.font)
            self.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_edit)

            self.pop_label = QtWidgets.QLabel()
            self.pop_label.setText("Population")
            self.pop_label.setFont(RegionViewer.font)
            self.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pop_label)
            self.pop_edit = QtWidgets.QSpinBox()
            self.pop_edit.setMaximum(999999)
            self.pop_edit.setMinimum(1)
            self.pop_edit.setValue(region.population())
            self.pop_edit.setFont(RegionViewer.font)
            self.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pop_edit)

            self.bias_label = QtWidgets.QLabel()
            self.bias_label.setText("Bias")
            self.bias_label.setFont(RegionViewer.font)
            self.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.bias_label)

            self.biaslayout = QtWidgets.QHBoxLayout()
            self.biasedit0 = QtWidgets.QDoubleSpinBox()
            self.biasedit0.setMinimum(-5)
            self.biasedit0.setMaximum(5)
            self.biasedit0.setDecimals(3)
            self.biasedit0.setValue(self.region.bias[0])
            self.biasedit0.setFont(RegionViewer.font)
            self.biaslayout.addWidget(self.biasedit0)
            self.biasedit1 = QtWidgets.QDoubleSpinBox()
            self.biasedit1.setMinimum(-5)
            self.biasedit1.setMaximum(5)
            self.biasedit1.setDecimals(3)
            self.biasedit1.setValue(self.region.bias[1])
            self.biasedit1.setFont(RegionViewer.font)
            self.biaslayout.addWidget(self.biasedit1)
            self.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.biaslayout)


            self.parties_label = QtWidgets.QLabel()
            self.parties_label.setText("Parties")
            self.parties_label.setFont(RegionViewer.font)
            self.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.parties_label)
            self.parties_field = QtWidgets.QPushButton()
            self.parties_field.setText('View')
            self.parties_field.setFont(RegionViewer.font)
            self.parties_field.clicked.connect(self.editparties)
            self.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.parties_field)

            self.done_button = QtWidgets.QPushButton()
            self.done_button.setText("Save")
            self.done_button.setFont(RegionViewer.font)
            self.done_button.clicked.connect(self.save_info)
            self.setWidget(4, QtWidgets.QFormLayout.SpanningRole, self.done_button)

        def editparties(self):
            if self.region.nation is None:
                self.partieslist = PartiesList('edit', self.region.local_parties, [], self.region)
            else:
                self.partieslist = PartiesList('edit', self.region.local_parties, self.region.nation.parties, self.region)

        def save_info(self):
            self.region.name = self.name_edit.text()
            self.region.set_bias((self.biasedit0.value(), self.biasedit1.value()))
            self.region.set_population(self.pop_edit.value())


    class ElectionButton(QtWidgets.QPushButton):
        def __init__(self, election, num, ui):
            super(RegionViewer.ElectionButton, self).__init__(ui)
            self.election = election
            self.setText(str(num + 1) + ". " + election.voting_system)
            self.setFont(RegionViewer.font)

            self.clicked.connect(self.showtable)
            self.resize(ui.width() - 10, 100)

        def showtable(self):
            self.table = ElectionTable(self.election)


    class ElectionList(WidgetList):
        def __init__(self, region, ui):
            super(RegionViewer.ElectionList, self).__init__()
            self.region = region
            self.ui = ui
            self.table = None


        def init_ui(self):
            self.outer_size = (RegionViewer.c1_width, RegionViewer.electionlist_height)
            super(RegionViewer.ElectionList, self).init_ui()
            self.resize(RegionViewer.c1_width, RegionViewer.electionlist_height)

            self.append(QtWidgets.QPushButton("Run Election"))
            self[-1].clicked.connect(self.add_election)


            for e in range(len(self.region.elections)):
                self.append(RegionViewer.ElectionButton(self.region.elections[e], e, self))

            self.setParent(self.ui)
            self.move(0, self.ui.basic_info_height)
            self.resize(RegionViewer.c1_width, RegionViewer.electionlist_height)

        def add_election(self):
            runner = RegionElectionRunner(region=self.region)
            election = runner.election
            self.append(RegionViewer.ElectionButton(election, 0, self))
            self.ui.load_replist()


    def __init__(self, region, ui = None):
        super(RegionViewer, self).__init__()
        self.region = region
        self.ui = ui
        self.init_ui()

    def load_replist(self):
        self.replist = RepsList(self.region.reps, self)
        self.replist.init_ui()
        self.replist.move(self.c1_width, 0)
        self.replist.resize(self.c2_width, self.replist_height)

    def init_ui(self):
        self.resize(self.c1_width + self.c2_width, self.replist_height)

        self.basicinfowidget = QtWidgets.QWidget(self)
        self.basicinfowidget.resize(self.c1_width, self.basic_info_height)
        self.basicinfowidget.setLayout(self.BasicInfo(self.region, self))
        self.load_replist()

        self.electionlist = RegionViewer.ElectionList(self.region, self)
        self.electionlist.init_ui()
        self.electionlist.resize(self.c1_width, self.electionlist_height)


        if self.ui is not None:
            self.setParent(self.ui)
        self.show()


class ElectionTable(QtWidgets.QTableWidget):
    def __init__(self, election):
        super(ElectionTable, self).__init__()

        self.winner_color = '#80DA80'
        self.loser_color =  '#E39494'

        # Set the column headers
        if election.voting_system in ['runoff', 'stv', 'dhont', 'webster']:
            self.setColumnCount(len(election.rounds))
            self.setRowCount(len(election.order))
            for r in range(len(election.rounds)):
                item = QtWidgets.QTableWidgetItem()
                item.setText('Round '+str(r + 1))
                self.setHorizontalHeaderItem(r, item)


        elif election.voting_system in ['borda', 'dowdall', 'fptp']:
            self.setColumnCount(2)
            self.setRowCount(len(election.candidates))
            self.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Votes'))
            self.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Percentages'))


        # Go through each round and put the information into the table
        if election.voting_system in ['dhont', 'webster']:
            for p in range(len(election.order)):
                party = election.order[p]

                item = QtWidgets.QTableWidgetItem()
                item.setText(party.name)
                item.setIcon(ColorIcon(party.color))

                self.setVerticalHeaderItem(p, item)


            for r in range(len(election.rounds)):
                this_round = election.rounds[r]
                for p in range(len(election.order)):
                    party = election.order[p]
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(this_round.votes[party]))
                    if party in this_round.winners:
                        item.setBackgroundColor(QtGui.QColor(self.winner_color))
                        item.setText(f'{str(this_round.votes[party])}\n({this_round.winners[0].name})')
                    self.setItem(p, r, item)


        elif election.voting_system in ['runoff', 'stv', 'borda', 'dowdall', 'fptp']:
            for c in range(len(election.order)):
                candidate = election.order[c]
                item = QtWidgets.QTableWidgetItem()
                item.setText(f'{candidate.name}\n({candidate.party.initials()})')

                item.setIcon(ColorIcon(candidate.party.color))

                self.setVerticalHeaderItem(c, item)

            if election.voting_system in ['runoff', 'stv']:
                for r in range(len(election.rounds)):
                        this_round = election.rounds[r]
                        for c in range(len(election.order)):
                            candidate = election.order[c]
                            item = QtWidgets.QTableWidgetItem()
                            if candidate in this_round.votes:
                                item.setText(str(round(this_round.votes[candidate], 2)))
                                if candidate in this_round.winners:
                                    item.setBackgroundColor(QtGui.QColor(self.winner_color))
                                if candidate in this_round.losers:
                                    item.setBackgroundColor(QtGui.QColor(self.loser_color))
                            else:
                                item.setText('0')
                            self.setItem(c, r, item)

            elif election.voting_system in ['fptp', 'borda', 'dowdall']:
                this_round = election.rounds[0]
                for c in range(len(election.order)):
                    candidate = election.order[c]
                    item = QtWidgets.QTableWidgetItem()
                    if candidate in this_round.votes:
                        item.setText(str(round(this_round.votes[candidate], 2)))
                        if candidate in this_round.winners:
                            item.setBackgroundColor(QtGui.QColor(self.winner_color))
                        if candidate in this_round.losers:
                            item.setBackgroundColor(QtGui.QColor(self.loser_color))
                    else:
                        item.setText('0')
                    self.setItem(c, 0, item)

        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.show()


class Runn():
    def __init__(self):
        self.n = e.Nation(map_width=6, map_height=6)
        self.n.create_regions(24, 1000)
        [self.n.add_party(e.Party()) for i in range(6)]
        self.n.set_seat_count(70)
        self.ne = e.NationElection(nation=self.n)
        self.ne.run('stv')
        self.map = NationViewer(self.n)



def main():
    app = QtWidgets.QApplication(argv)
    t = Runn()
    app.exec_()


if __name__ == '__main__':
    main()
