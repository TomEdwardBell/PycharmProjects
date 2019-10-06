from PyQt5 import QtCore, QtGui, QtWidgets
from sys import argv
import random

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

class PartyEdit(QtWidgets.QFormLayout):
    font = QtGui.QFont()
    font.setPointSize(12)
    font.setFamily('Bahnschrift Light')

    def __init__(self, party = None, ui = None):
        super(PartyEdit, self).__init__()
        if ui is not None:
            self.setParent(ui)
        if party is None:
            party = e.Party()
            party.name = "name"
            party.leaning = (0, 0)
            party.color = "#666666"
            party.relevance = 1



    def init_ui(self):
        self.resize(300, 300)

        self.namelabel = QtWidgets.QLabel('Name:')


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
        self.block_size = (450, 100)

        if rep is not None or True:
            self.rep = rep
            self.init_ui()

    def init_ui(self):
        #self.resize(self.block_size[0], self.block_size[1])

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

        self.Line = QtWidgets.QFrame(self)
        self.Line.setGeometry(QtCore.QRect(0, 99, self.block_size[0], 1))
        self.Line.setFrameShape(QtWidgets.QFrame.HLine)

        self.setStyleSheet('background-color:' + self.bg_colors[0])


        self.verticalLayoutWidget.setGeometry(QtCore.QRect(25, 0, self.block_size[0] - self.PartyColor.width(), self.block_size[1]))

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

class ElectionRunner(QtWidgets.QWidget):
    def __init__(self, *kwargs):
        super(ElectionRunner, self).__init__()
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
        regionbutton.clicked.connect(lambda state, c = region: self.RegionViewer.set_region(region))

    def setHouse(self, house):
        # Sets all the widgets to those in the new house
        self.clear()
        for region in house:
            self.add(region)


class RegionViewer(QtWidgets.QWidget):
    c1_width = 350
    # Width of column one (Contains basic info and list of elections)
    c2_width = 350

    basic_info_height = 100
    electionlist_height = 200
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
            self.name_field = QtWidgets.QLabel()
            self.name_field.setText(region.name)
            self.name_field.setFont(RegionViewer.font)
            self.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_field)

            self.pop_label = QtWidgets.QLabel()
            self.pop_label.setText("Population")
            self.pop_label.setFont(RegionViewer.font)
            self.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pop_label)
            self.pop_field = QtWidgets.QLabel()
            self.pop_field.setText(str(region.population()))
            self.pop_field.setFont(RegionViewer.font)
            self.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.pop_field)

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
            self.setText(str(num + 1) + ". " + election.votingsystem)
            self.setFont(RegionViewer.font)

            self.clicked.connect(self.showtable)
            self.resize(ui.width() - 10, 50)

        def showtable(self):
            self.table = ElectionTable(self.election)
            self.table.load()


    class ElectionList(WidgetList):
        def __init__(self, region, ui):
            super(RegionViewer.ElectionList, self).__init__()
            self.region = region
            self.ui = ui


        def init_ui(self):
            self.outer_size = (RegionViewer.c1_width, RegionViewer.electionlist_height)
            super(RegionViewer.ElectionList, self).init_ui()
            self.resize(RegionViewer.c1_width, RegionViewer.electionlist_height)
            for e in range(len(self.region.elections)):
                self.append(RegionViewer.ElectionButton(self.region.elections[e], e, self))

            self.setParent(self.ui)
            self.move(0, self.ui.basic_info_height)
            self.show()
            self.resize(RegionViewer.c1_width, RegionViewer.electionlist_height)



    def __init__(self, region, ui = None):
        super(RegionViewer, self).__init__()
        self.region = region
        self.ui = ui

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


class ElectionViewer(QtWidgets.QWidget):
    def __init__(self, ui, election):
        self.ui = ui
        self.width = 800
        self.height = 400
        self.election_table = ElectionTable(ui, election)
        self.election_table.table.move(200,0)


class ElectionTable:
    def __init__(self, election, ui = None):
        self.ui = ui
        self.votingsystem = election.votingsystem
        self.election = election
        self.ui = ui
        self.width = 600
        self.height = 400

        self.tables = {
            'av': self.AV_Table,
            'stv': self.STV_Table,
            'fptp': self.FPTP_Table,
            'dhont': self.Divisor_Table,
            'webster': self.Divisor_Table,
            'borda': self.Borda_Table,
            'dowdall': self.Borda_Table
        }


    def load(self):
        if self.votingsystem in self.tables.keys():
            tabletype = self.tables[self.votingsystem]
            self.table = tabletype(self.election, self)
            if self.ui is not None:
                self.table.setParent(self.ui)


    class AV_Table(QtWidgets.QTableWidget):
        def __init__(self, election, tableclass):
            super(ElectionTable.AV_Table, self).__init__()
            self.election = election
            self.rounds = election.rounds

            self.candidates = election.order

            self.tableClass = tableclass

            self.load()

        def load(self):
            self.resize(self.tableClass.width, self.tableClass.height)
            self.setColumnCount(len(self.rounds))
            self.setRowCount(len(self.candidates))

            self.setSortingEnabled(False)

            for i in range(len(self.rounds)):
                item = QtWidgets.QTableWidgetItem()
                item.setText(('Round ' + str(i + 1)))
                self.setHorizontalHeaderItem(i, item)

            for c in range(len(self.candidates)):
                item = QtWidgets.QTableWidgetItem()
                item.setText(f'{self.candidates[c].name}\n({self.candidates[c].party.name})')
                self.setVerticalHeaderItem(c, item)

            for r in range(len(self.rounds)):
                round = self.rounds[r]
                for c in range(len(self.candidates)):
                    cand = self.candidates[c]
                    if cand in round.candidates():
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(round.votes[cand]))
                        self.setItem(c, r, item)
                        if round.loser == cand:
                            item.setBackground(QtGui.QColor(255, 180, 180))
                        elif r == len(self.rounds) - 1 :
                            item.setBackground(QtGui.QColor(180, 255, 180))
                    else:
                        item = QtWidgets.QTableWidgetItem()
                        item.setText('-')
                        self.setItem(c, r, item)


            self.resizeRowsToContents()
            self.resizeColumnsToContents()
            self.show()


    class STV_Table(QtWidgets.QTableWidget):
        def __init__(self, election, tableclass):
            super(ElectionTable.STV_Table, self).__init__()
            self.election = election
            self.rounds = election.rounds

            self.candidates = election.order
            print(self.candidates)

            self.tableClass = tableclass

            self.load()

        def load(self):
            self.resize(self.tableClass.width, self.tableClass.height)
            self.setColumnCount(len(self.rounds))
            self.setRowCount(len(self.candidates))

            self.setSortingEnabled(False)

            for i in range(len(self.rounds)):
                item = QtWidgets.QTableWidgetItem()
                item.setText(('Round ' + str(i + 1)))
                self.setHorizontalHeaderItem(i, item)

            for c in range(len(self.candidates)):
                item = QtWidgets.QTableWidgetItem()
                item.setText(f'{self.candidates[c].name}\n({self.candidates[c].party.name})')
                self.setVerticalHeaderItem(c, item)



            for r in range(len(self.rounds)):
                this_round = self.rounds[r]
                for c in range(len(self.candidates)):
                    cand = self.candidates[c]
                    if cand in this_round.candidates():
                        item = QtWidgets.QTableWidgetItem()
                        item.setText(str(round(this_round.votes[cand], 3)))
                        self.setItem(c, r, item)
                        if cand in this_round.losers:
                            item.setBackground(QtGui.QColor(255, 180, 180))
                        elif cand in this_round.winners:
                            item.setBackground(QtGui.QColor(180, 255, 180))
                    else:
                        item = QtWidgets.QTableWidgetItem()
                        item.setText('-')
                        self.setItem(c, r, item)


            self.resizeRowsToContents()
            self.resizeColumnsToContents()
            self.show()

    class FPTP_Table(QtWidgets.QTableWidget):
        def __init__(self, election, tableclass):
            super(ElectionTable.FPTP_Table, self).__init__()
            self.election = election
            self.round = election.rounds[0]

            self.candidates = list(self.round.candidates())

            self.tableClass = tableclass

            self.load()

        def load(self):
            self.resize(self.tableClass.width, self.tableClass.height)
            self.setColumnCount(2)
            self.setRowCount(len(self.candidates))

            item = QtWidgets.QTableWidgetItem()
            item.setText('Votes')
            self.setHorizontalHeaderItem(0, item)

            item = QtWidgets.QTableWidgetItem()
            item.setText('%')
            self.setHorizontalHeaderItem(1, item)

            for c in range(len(self.candidates)):
                item = QtWidgets.QTableWidgetItem()
                item.candidate = self.candidates[c]
                item.setText(self.candidates[c].name + '\n(' + self.candidates[c].party.name + ')')
                self.setVerticalHeaderItem(c, item)

            for c in range(len(self.candidates)):
                cand = self.candidates[c]
                if cand in self.round.votes:
                    votecount = QtWidgets.QTableWidgetItem()
                    votecount.setText(str(self.round.votes[cand]))
                    self.setItem(c, 0, votecount)
                    voteperc = QtWidgets.QTableWidgetItem()
                    voteperc.setText(str(self.round.percentages[cand]))
                    self.setItem(c, 1, voteperc)
                    if self.round.winner == cand:
                        votecount.setBackground(QtGui.QColor(180, 255, 180))
                        voteperc.setBackground(QtGui.QColor(180, 255, 180))

            self.resizeRowsToContents()
            self.resizeColumnsToContents()
            self.show()


    class Divisor_Table(QtWidgets.QTableWidget):
        def __init__(self, election, tableclass):
            super(ElectionTable.Divisor_Table, self).__init__()

            self.election = election
            self.rounds = election.rounds

            self.parties = list(self.rounds[0].votes.keys())

            self.tableClass = tableclass

            self.load()

        def load(self):
            self.resize(self.tableClass.width, self.tableClass.height)
            self.setColumnCount(len(self.rounds) + 1)
            self.setRowCount(len(self.parties))

            for i in range(len(self.rounds)):
                item = QtWidgets.QTableWidgetItem()
                item.setText(('Round ' + str(i + 1)))
                self.setHorizontalHeaderItem(i, item)
            item = QtWidgets.QTableWidgetItem()
            item.setText('Total')
            self.setHorizontalHeaderItem(len(self.rounds), item)

            for p in range(len(self.parties)):
                item = QtWidgets.QTableWidgetItem()
                item.party = self.parties[p]
                item.setText(self.parties[p].name)
                self.setVerticalHeaderItem(p, item)

            for r in range(len(self.rounds)):
                round = self.rounds[r]
                for p in range(len(self.parties)):
                    party = self.parties[p]
                    item = QtWidgets.QTableWidgetItem()
                    item.setText(str(round.votes[party]))
                    self.setItem(p, r, item)
                    if round.winner.party == party:
                        item.setBackground(QtGui.QColor(180, 255, 180))

            for p in range(len(self.parties)):
                total = self.election.party_seatcount[self.parties[p]]
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(total))
                item.setBackground(QtGui.QColor(200, 200, 200))
                self.setItem(p, len(self.rounds), item)

            self.resizeRowsToContents()
            self.resizeColumnsToContents()
            self.show()


    class Borda_Table(QtWidgets.QTableWidget):
        def __init__(self, election, tableclass):
            super(ElectionTable.Borda_Table, self).__init__()
            self.election = election
            self.round = election.rounds[0]

            self.candidates = list(self.round.candidates())

            self.tableClass = tableclass

            self.load()

        def load(self):
            self.resize(self.tableClass.width, self.tableClass.height)
            self.setColumnCount(1)
            self.setRowCount(len(self.candidates))

            item = QtWidgets.QTableWidgetItem()
            item.setText('Points')
            self.setHorizontalHeaderItem(0, item)

            for c in range(len(self.candidates)):
                item = QtWidgets.QTableWidgetItem()
                item.candidate = self.candidates[c]
                item.setText(self.candidates[c].name + '\n(' + self.candidates[c].party.name + ')')
                self.setVerticalHeaderItem(c, item)

            for c in range(len(self.candidates)):
                cand = self.candidates[c]
                if cand in self.round.candidates():
                    points = QtWidgets.QTableWidgetItem()
                    point_count = str(round(self.round.votes[cand], 3))
                    points.setText(point_count)
                    self.setItem(c, 0, points)
                    if cand in self.round.winners:
                        points.setBackground(QtGui.QColor(180, 255, 180))


            self.resizeRowsToContents()
            self.resizeColumnsToContents()
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

        xleanings = [voter.leaning[0] for voter in self.region]
        yleanings = [voter.leaning[1] for voter in self.region]

        pop = len(xleanings)
        alpha = 1/(pop/self.Alphascale) if pop > self.Alphascale else 1
        size = 1/(pop/self.Sizescale) if pop > self.Sizescale else 1

        self.figure = Figure(dpi=100)
        ax = self.figure.add_subplot(111)
        ax.plot(xleanings, yleanings, 'ro', alpha=alpha, color='#DD0000', linewidth=size)

        self.draw()
        self.show()

    def show_favourite(self, cands):
        candvotes = {cand:[[],[]] for cand in cands}
        # {candidate:[[Voters x leanings],[Voters' y leanings]]}

        for voter in self.region:
            candvotes[voter.rank(cands)[0]][0].append(voter.leaning[0])
            candvotes[voter.rank(cands)[0]][1].append(voter.leaning[1])

        pop = len(self.region)
        alpha = 1/(pop/self.Alphascale) if pop > self.Alphascale else 1
        size = 1/(pop/self.Sizescale) if pop > self.Sizescale else 1

        self.figure = Figure(dpi=100)
        ax = self.figure.add_subplot(111)
        for cand in candvotes:
            x = candvotes[cand][0]
            y = candvotes[cand][1]
            ax.plot(x, y, 'rx', alpha=alpha, color=cand.color, linewidth=size)

            candx = cand.leaning[0]
            candy = cand.leaning[1]
            ax.plot(candx,candy, 'ro', alpha=1, color=cand.color, linewidth=size*4, markeredgecolor='black')

        self.draw()
        self.show()

    def show_election(self, election):
        if election.votingsystem == 'av':
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
        self.r.addVoters(1000)
        self.r.reps_to_send = 3

        elec = e.RegionElection(self.r)
        elec.stv([e.Candidate() for i in range(10)])

        self.et = ElectionTable(elec)
        self.et.load()



def main():
    app = QtWidgets.QApplication(argv)
    t = Runn()
    app.exec_()


if __name__ == '__main__':
    main()
