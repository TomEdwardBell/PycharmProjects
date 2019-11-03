from PySide2 import QtCore, QtGui, QtWidgets
from sys import argv
import random
import time

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
        pol = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.RL_Contents.setSizePolicy(pol)
        self.setSizePolicy(pol)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.RL_VLayout = QtWidgets.QVBoxLayout(self.RL_Contents)
        #self.RL_VLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
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
        for wid in self.widgets: wid.resize(w -10, wid.height())


    def clear(self): # Removes all the widgets in the list
        for widget in self.widgets:
            widget.destroy()

    def __getitem__(self, item):
        return self.widgets[item]


class RepsList(WidgetList):
    def __init__(self, reps = [], ui = None):
        super(RepsList, self).__init__()
        if ui is not None:
            self.setParent(ui)

        self.reps = reps

    def init_ui(self):
        super(RepsList, self).init_ui()
        self.views = [RepView(self, rep) for rep in self.reps]
        for v in self.views:
            v.init_ui()
            v.show()
        self.append(self.views)


class PartyEdit(QtWidgets.QWidget):
    font = QtGui.QFont()
    font.setPointSize(12)
    font.setFamily('Bahnschrift Light')

    def __init__(self, party=None, ui = None):
        super(PartyEdit, self).__init__()
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
        self.show()


    def init_ui(self):
        self.setGeometry(QtCore.QRect(0, 0, 300, 300))

        self.namelabel = QtWidgets.QLabel('Name:')
        self.layout.setWidget(0, self.layout.LabelRole, self.namelabel)
        self.nameedit = QtWidgets.QLineEdit(self.party.name)
        self.layout.setWidget(0, self.layout.FieldRole, self.nameedit)

        self.leaninglabel = QtWidgets.QLabel('Leaning:')
        self.layout.setWidget(1, self.layout.LabelRole, self.leaninglabel)

        self.leaninglayout = QtWidgets.QHBoxLayout()
        self.leaningedit0 = QtWidgets.QLineEdit(str(round(self.party.leaning[0], 3)))
        self.leaningedit1 = QtWidgets.QLineEdit(str(round(self.party.leaning[1], 3)))
        self.leaninglayout.addWidget(self.leaningedit0)
        self.leaninglayout.addWidget(self.leaningedit1)
        self.layout.setLayout(1, self.layout.FieldRole, self.leaninglayout)

        self.relevancelabel = QtWidgets.QLabel('Relevance: ')
        self.layout.setWidget(2, self.layout.LabelRole, self.relevancelabel)
        self.relevanceedit = QtWidgets.QLineEdit(str(round(self.party.relevance, 3)))
        self.layout.setWidget(2, self.layout.FieldRole, self.relevanceedit)

        self.colorlabel = QtWidgets.QLabel('Color: ')
        self.layout.setWidget(3, self.layout.LabelRole, self.colorlabel)

        self.coloredit = QtWidgets.QPushButton(self.party.color)
        self.coloredit.clicked.connect(self.setcolor)
        if QtGui.QColor(self.party.color).lightness() < 100:
            self.coloredit.setStyleSheet(f'background-color:{self.party.color}; color:#FFFFFF')
        else:
            self.coloredit.setStyleSheet(f'background-color:{self.party.color}; color:#000000')
        self.layout.setWidget(3, self.layout.FieldRole, self.coloredit)

        self.donebutton = QtWidgets.QPushButton('Done')
        self.donebutton.clicked.connect(self.save)
        self.layout.setWidget(4, self.layout.FieldRole, self.donebutton)

    def setcolor(self):
        color = QtWidgets.QColorDialog.getColor()
        self.coloredit.setText(color.name())
        self.coloredit.setStyleSheet('background-color:' + color.name())
        if color.lightness() < 100:
            self.coloredit.setStyleSheet(f'background-color:{color.name()}; color:#FFFFFF')
        else:
            self.coloredit.setStyleSheet(f'background-color:{color.name()}; color:#000000')

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
            self.party.name = self.nameedit.text()
            self.party.leaning = self.leaningedit0.text(), self.leaningedit1.text()
            self.party.relevance = self.relevanceedit.text()
            self.destroy()
        else:
            for widget in invalids:
                widget.setStyleSheet('color: #FF0000')


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
        self.candidate = candidate
        self.layout = QtWidgets.QFormLayout()
        self.setLayout(self.layout)
        self.init_ui()
        self.show()


    def init_ui(self):

        self.setGeometry(QtCore.QRect(0, 0, 300, 300))

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

        self.partylabel = QtWidgets.QLabel('Party: ')
        self.layout.setWidget(3, self.layout.LabelRole, self.partylabel)

        self.donebutton = QtWidgets.QPushButton('Done')
        self.donebutton.clicked.connect(self.save)
        self.layout.setWidget(4, self.layout.FieldRole, self.donebutton)

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
        self.setRegionName(self.rep.region.name)

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
    class CandidateElectionOptions(QtWidgets.QWidget):
        def __init__(self, election):
            super(RegionElectionRunner.CandidateElectionOptions, self).__init__()
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

            self.candslabel = QtWidgets.QLabel("Candidates")
            self.layout.setWidget(2, self.layout.LabelRole, self.candslabel)
            self.candsbutton = QtWidgets.QPushButton("Click to view candidates")
            self.candsbutton.clicked.connect(self.loadcandslist)
            self.layout.setWidget(2, self.layout.FieldRole, self.candsbutton)

            self.runbutton = QtWidgets.QPushButton('Run')
            self.runbutton.clicked.connect(self.runelection)
            self.layout.setWidget(3, self.layout.FieldRole, self.runbutton)

            self.resize(100, 100)
            self.show()

        def runelection(self):
            self.done = True
            self.election.region.seat_count = self.repsnumspinbox.value()
            self.election.run(self.election.voting_system, self.election.candidates)
            ElectionTable(self.election)
            self.destroy()


        def loadcandslist(self):
            self.candslist = self.CandsList(self.election)
            for candidate in self.election.candidates:
                self.candslist.append(self.CandButton(candidate))

        class CandButton(QtWidgets.QPushButton):
            def __init__(self, candidate):
                super(RegionElectionRunner.CandidateElectionOptions.CandButton, self).__init__()
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
                self.edit.donebutton.clicked.connect(lambda candidate=self.candidate: [self.edit.save(), self.setText(candidate.name)])
                self.setText(self.candidate.name)

        class CandsList(WidgetList):
            def __init__(self, election):
                super(RegionElectionRunner.CandidateElectionOptions.CandsList, self).__init__()
                self.outer_size = (320, 500)
                self.init_ui()
                self.election = election
                self.addbutton = QtWidgets.QPushButton('Add Candidate')
                self.addbutton.clicked.connect(self.addcand)
                self.append(self.addbutton)

            def addcand(self):
                candidate = e.Candidate()
                self.election.candidates.append(candidate)
                candbutton = RegionElectionRunner.CandidateElectionOptions.CandButton(candidate)
                self.append(candbutton)

    class DivisorElectionOptions(QtWidgets.QWidget):
        pass

    class voting_systemButton(QtWidgets.QPushButton):
        def __init__(self, vs, widgetlist):
            super(RegionElectionRunner.voting_systemButton, self).__init__(widgetlist)
            self.setText(vs)
            self.resize(500, 100)
            self.clicked.connect(lambda: widgetlist.clicked(vs))

    class voting_systemChooser(WidgetList):
        def __init__(self, parent_ui, election):
            super(RegionElectionRunner.voting_systemChooser, self).__init__()
            self.init_ui()
            self.done = False
            vs_names = list(election.candidatesystems.keys()) + list(election.partylistsystems.keys())
            self.resize(500, 700)
            buttons = []
            for vs in vs_names:
                buttons.append(RegionElectionRunner.voting_systemButton(vs, self))
                self.append(buttons[-1])

        def clicked(self, vs):
            self.vs = vs
            self.done = True

    def __init__(self, **kwargs):
        if 'region' in kwargs:
            self.election = e.RegionElection(region=kwargs['region'])
        else:
            self.election = e.RegionElection()

        self.vs = ""
        self.vs_chooser = RegionElectionRunner.voting_systemChooser(self, self.election)
        while not self.vs_chooser.done:
            QtWidgets.QApplication.processEvents()
            time.sleep(0.05)

        self.election.voting_system = self.vs_chooser.vs
        if self.election.voting_system in self.election.candidatesystems:
            self.vs_chooser.destroy()
            self.election_options = RegionElectionRunner.CandidateElectionOptions(self.election)
            self.election_options.done = False
            while not self.election_options.done:
                QtWidgets.QApplication.processEvents()
                time.sleep(0.05)


class NationalElectionRunner():
    pass


class RegionScroller(WidgetList):
    # A list of all the regions
    # When you click a region the region viewer window changes to show the info about that region
    def __init__(self, parent = None):
        super(RegionScroller, self).__init__(parent)
        self.RegionViewer = None
        # The pointer to the thing that lets you view the details of a region
        self.init_ui()
        self.resize(400, 300)
        self.addButton = QtWidgets.QPushButton(self)

    def add(self, region):
        regionbutton = QtWidgets.QPushButton(self)
        regionbutton.setText(region.name)
        regionbutton.resize(self.width(), 30)

        self.append(regionbutton)
        regionbutton.clicked.connect(lambda c = region: self.RegionViewer.set_region(c))


class RegionViewer(QtWidgets.QWidget):
    c1_width = 700
    # Width of column one (Contains basic info and list of elections)
    c2_width = 700

    basic_info_height = 250
    electionlist_height = 400
    replist_height = basic_info_height + electionlist_height

    font = QtGui.QFont()
    font.setPointSize(12)
    font.setFamily('Bahnschrift Light')

    class BasicInfo(QtWidgets.QFormLayout):
        def __init__(self, region, ui):
            super(RegionViewer.BasicInfo, self).__init__(ui)
            self.setGeometry(QtCore.QRect(0, 0, RegionViewer.c1_width, RegionViewer.basic_info_height))

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
            self.pop_edit.setMaximum(10000)
            self.pop_edit.setMinimum(1)
            self.pop_edit.setValue(region.population())
            self.pop_edit.setFont(RegionViewer.font)
            self.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pop_edit)

            self.bias_label = QtWidgets.QLabel()
            self.bias_label.setText("Bias")
            self.bias_label.setFont(RegionViewer.font)
            self.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.bias_label)
            self.bias_field = QtWidgets.QLabel()
            self.bias_field.setText(str((round(region.bias[0], 2), round(region.bias[1], 2))))
            self.bias_field.setFont(RegionViewer.font)
            self.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.bias_field)

    class ElectionButton(QtWidgets.QPushButton):
        def __init__(self, election, num,ui):
            super(RegionViewer.ElectionButton, self).__init__(ui)
            self.election = election
            #self.setText(str(num + 1) + ". " + election.voting_system)
            self.setText(". ")
            self.setFont(RegionViewer.font)

            self.clicked.connect(self.showtable)
            self.resize(ui.width() - 10, 100)

        def showtable(self):
            self.table = ElectionTable(self.election)
            self.table.load()


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
            self.show()
            self.resize(RegionViewer.c1_width, RegionViewer.electionlist_height)

        def add_election(self):
            runner = RegionElectionRunner(region=self.region)
            election = runner.election
            self.append(RegionViewer.ElectionButton(election, 0, self))



    def __init__(self, region, ui = None):
        super(RegionViewer, self).__init__()
        self.region = region
        self.ui = ui
        self.init_ui()

    def init_ui(self):
        self.resize(self.c1_width + self.c2_width, self.replist_height)

        self.basicinfo = RegionViewer.BasicInfo(self.region, self)
        self.replist = RepsList(self.region.reps, self)
        self.replist.init_ui()
        self.replist.move(self.c1_width, 0)
        self.replist.resize(self.c2_width, self.replist_height)

        self.electionlist = RegionViewer.ElectionList(self.region, self)
        self.electionlist.init_ui()
        self.electionlist.resize(self.c1_width, self.electionlist_height)


        if self.ui is not None:
            self.setParent(self.ui)
        self.show()


class RegionList(QtWidgets.QWidget):
    def __init__(self):
        super(RegionList, self).__init__()
        self.current_region = None

        self.Region_Form = QtWidgets.QFormLayout(self)
        self.Region_Form.setContentsMargins(0, 0, 0, 0)
        self.Region_Form.setObjectName('Region_Form')

        self.NameLbl = QtWidgets.QLabel(self)
        self.NameLbl.setText('Name: ')
        self.Region_Form.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.NameLbl)

        self.PopLbl = QtWidgets.QLabel(self)
        self.PopLbl.setText('Population: ')
        self.Region_Form.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.PopLbl)

        self.NameEdit = QtWidgets.QLineEdit(self)
        self.Region_Form.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.NameEdit)

        self.PopEdit = QtWidgets.QSpinBox(self)
        self.PopEdit.setMinimum(1)
        self.PopEdit.setMaximum(100000)
        self.Region_Form.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.PopEdit)

        self.UpdateButton = QtWidgets.QPushButton(self)
        self.Region_Form.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.UpdateButton)
        self.UpdateButton.setText('Update')
        self.UpdateButton.clicked.connect(self.update_region)

        self.showElectionResultsButton = QtWidgets.QPushButton(self)
        self.showElectionResultsButton.setText('Show Election Results')

    def set_region(self, region):
        # Change the current region
        self.current_region = region
        self.NameEdit.setText(region.name)
        self.PopEdit.setProperty('value', (len(region)))

    def update_region(self):
        self.current_region.setName(self.NameEdit.text())
        self.current_region.setPopulation(self.PopEdit.value())


class ElectionTable(QtWidgets.QTableWidget):
    def __init__(self, election):
        super(ElectionTable, self).__init__()

        self.winner_color = '#80DA80'
        self.loser_color =  '#E39494'

        # Set the column headers
        if election.voting_system in ['av', 'stv', 'dhont', 'webster']:
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
            for p in range(len(election.parties)):
                party = election.parties[p]

                item = QtWidgets.QTableWidgetItem()
                item.setText(party.name)

                icon = QtGui.QIcon()
                pixmap = QtGui.QPixmap(50, 50)
                pixmap.fill(QtGui.QColor(party.color))
                icon.addPixmap(pixmap)
                item.setIcon(icon)

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

        elif election.voting_system in ['av', 'stv']:
            for c in range(len(election.order)):
                candidate = election.order[c]
                item = QtWidgets.QTableWidgetItem()
                item.setText(f'{candidate.name}\n({candidate.party.name})')

                icon = QtGui.QIcon()
                pixmap = QtGui.QPixmap(50, 50)
                pixmap.setDevicePixelRatio(100)
                pixmap.fill(QtGui.QColor(candidate.party.color))
                icon.addPixmap(pixmap)
                item.setIcon(icon)

                self.setVerticalHeaderItem(c, item)

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


        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.adjustSize()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.show()


class VoterGraph(QtWidgets.QWidget):
    def __init__(self, region, window = None):
        super(VoterGraph, self).__init__()
        self.region = region

        self.Alphascale = 500
        # Higher the Alphascale, the less transparent
        self.Sizescale = 40
        # Higher the Sizescale, the larger

        self.initUI(window)


    def initUI(self, window):
        if not window is None:
            self.setParent(window)



    def show_figure(self, figure):
        self.canvas = FigureCanvas(figure)
        self.figure = figure
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.canvas.draw()


    def show_leaning(self):

        xleaning = [voter.leaning[0] for voter in self.region]
        yleaning = [voter.leaning[1] for voter in self.region]

        pop = len(xleaning)
        alpha = 1/(pop/self.Alphascale) if pop > self.Alphascale else 1
        size = 1/(pop/self.Sizescale) if pop > self.Sizescale else 1

        self.figure = Figure(dpi=100)
        ax = self.figure.add_subplot(111)
        ax.plot(xleaning, yleaning, 'ro', alpha=alpha, color='#DD0000', linewidth=size)

        self.draw()
        self.show()

    def show_favourite(self, candidates):
        candvotes = {candidate:[[],[]] for candidate in candidates}
        # {candidate:[[Voters x leaning],[Voters' y leaning]]}

        for voter in self.region:
            candvotes[voter.rank(candidates)[0]][0].append(voter.leaning[0])
            candvotes[voter.rank(candidates)[0]][1].append(voter.leaning[1])

        pop = len(self.region)
        alpha = 1/(pop/self.Alphascale) if pop > self.Alphascale else 1
        size = 1/(pop/self.Sizescale) if pop > self.Sizescale else 1

        self.figure = Figure(dpi=100)
        ax = self.figure.add_subplot(111)
        for candidate in candvotes:
            x = candvotes[candidate][0]
            y = candvotes[candidate][1]
            ax.plot(x, y, 'rx', alpha=alpha, color=candidate.color, linewidth=size)

            candx = candidate.leaning[0]
            candy = candidate.leaning[1]
            ax.plot(candx,candy, 'ro', alpha=1, color=candidate.color, linewidth=size*4, markeredgecolor='black')

        self.draw()
        self.show()

    def show_election(self, election):
        if election.voting_system == 'av':
            self.show_av(election)

    def show_av(self, election):
        nextround_btn = QtWidgets.QPushButton(self)
        lastround_btn = QtWidgets.QPushButton(self)

        nextround_btn.resize(100, 100)

        nextround_btn.show()
        lastround_btn.show()

        self.show()


class Runn():
    def __init__(self):
        self.r = e.Region()
        self.r.add_voters(20000)
        self.r.seat_count = 1
        self.r.create_local_parties(10)
        self.re = e.RegionElection(region=self.r, voting_system='fptp')
        self.re.print_rounds()
        self.t = ElectionTable(self.re)



def main():
    app = QtWidgets.QApplication(argv)
    t = Runn()
    app.exec_()


if __name__ == '__main__':
    main()

