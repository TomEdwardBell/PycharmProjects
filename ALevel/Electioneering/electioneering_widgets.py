from PySide2 import QtCore, QtGui, QtWidgets
from sys import argv
import random
import time
from collections import Counter


import electioneering as e


class WidgetList(QtWidgets.QScrollArea):
    def __init__(self, **kwargs):
        super(WidgetList, self).__init__()
        if 'parent' in kwargs:
            self.setParent(kwargs['parent'])
        # Putting a WidgetList into another UI

        # Outer Widget        = The window , 'self' , contains just the inner scroll widget
        #                       Fixed size, even when more items are added
        # Inner scroll widget = The area that you scroll through
        #                       Widgets in the inner scroll widget are arranged vertically
        #                       Gets longer as more items are added
        # v_layout            = The vertical layout which the items in the inner scroll widget adhere to
        # items               = The individual widgets which are added to the widget list

        # Default size of the WidgetList outer widget
        self.window_size = (400, 800)

        # If width or height are specified in kwargs
        if 'width' in kwargs:
            self.window_size = kwargs['width'], self.window_size[1]
        if 'height' in kwargs:
            self.window_size = self.window_size[0], kwargs['height']

        # The inner widget has a variable height that you can scroll through
        self.inner_height = 0

        # The width of the scroll bar (constant)
        self.scroll_bar_width = 20

        # Resizing the outer widget to the window_size
        super(WidgetList, self).resize(self.window_size[0], self.window_size[1])

        # Vertical scroll bar on the outer widget list
        # Not horizontal scroll bar
        # So you can scroll through the many items on the inner layout
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.horizontalScrollBar().setEnabled(False)

        # But you can resize the outer widget
        self.setWidgetResizable(True)

        # The vertical layout which the inner_scroll_widget follows
        self.v_layout = QtWidgets.QVBoxLayout()
        self.v_layout.setMargin(0)
        self.v_layout.setSpacing(0)

        # The widget that all the sub-items are located
        self.inner_scroll_widget = QtWidgets.QWidget()
        # Setting its layout
        self.inner_scroll_widget.setLayout(self.v_layout)
        self.inner_scroll_widget.resize(self.width() - self.scroll_bar_width, self.inner_height)

        # Setting the widget which you scroll through
        self.setWidget(self.inner_scroll_widget)


        self.show()

    def add_widget(self, widget):
        widget.setParent(self.inner_scroll_widget)
        # Add the sub widget to the scroll widget
        widget.show()
        # Show the widget (incase it's hidden)

        self.inner_height += widget.height()
        # Add the widget's height to the inner height

        self.inner_scroll_widget.setFixedSize(self.width() - self.scroll_bar_width, self.inner_height)

        self.v_layout.addWidget(widget)
        # Add the widget to the vertical layout

        widget.setFixedSize(widget.width(), widget.height())
        # Make sure the widget has a fixed size

    def add_widgets(self, widgets):
        for widget in widgets:
            self.add_widget(widget)

    def clear(self):
        widgets = self.widgets()
        for w in range(len(widgets)):
            widget = widgets[w]

            # Remove the widget from the layout
            self.v_layout.removeWidget(widget)

            # Remove the widget from the WidgetList
            widget.setParent(None)

            # Hide the widget
            widget.hide()

            # Destroy the widget
            widget.destroy()

        # Set the inner height to 0
        self.inner_height = 0

        # Resize the inner scroll area
        self.inner_scroll_widget.setFixedSize(self.width() - self.scroll_bar_width, 0)

    def widgets(self):
        return self.inner_scroll_widget.children()[1:]
        # [:1] used because the first 'child' of the outer window is the inner scroll area
        # The rest are the items are the widgets in the list

    def resize(self, w, h):
        # Resizes the outer window
        # Height of the inner scrolls area stays the same
        super(WidgetList, self).resize(w, h)
        self.inner_scroll_widget.setFixedSize(w - self.scroll_bar_width, self.inner_height)

    def remove_widget(self, widget):
        if widget in self.widgets():

            # Remove widget from layout
            self.v_layout.removeWidget(widget)

            self.inner_height -= widget.height()
            # Take away the widget's height from the inner height

            self.inner_scroll_widget.setFixedSize(self.width() - self.scroll_bar_width, self.inner_height)

            # Kill widget
            widget.hide()
            widget.setParent(None)
            widget.destroy()


class PartiesList(WidgetList):
    # List of parties
    def __init__(self, mode, local_parties, national_parties, RegionOrNation=None):
        super(PartiesList, self).__init__(width=700, height=600)
        self.mode = mode
        self.move(500, 500)
        self.region_type = None

        if type(RegionOrNation) == e.Nation:
            # If it's a list of national parties
            self.region_type = 'nation'
            self.nation = RegionOrNation
            self.region = RegionOrNation
        elif type(RegionOrNation) == e.Region:
            # If it's a list of regional parties
            self.region_type = 'region'
            self.region = RegionOrNation

        if mode == 'select':
            # If you're using the list to select a party
            # selected_party is the party the user selects
            self.selected_party = False

        if national_parties != [] or self.region_type == 'nation':
            # For national parties
            national_parties_label = QtWidgets.QLabel("National Parties: ")
            national_parties_label.setFont(QtGui.QFont('Arial', 20))
            national_parties_label.resize(700, 100)
            self.add_widget(national_parties_label)

            if mode == 'edit' and self.region_type == 'nation':
                # If you're editing parties in a nation

                # Adding parties
                self.add_national_button = QtWidgets.QPushButton(self)
                self.add_national_button.setText('Add National Party')
                self.add_national_button.setFont(QtGui.QFont('Arial', 15))
                self.add_national_button.resize(600, 70)
                self.add_widget(self.add_national_button)
                self.add_national_button.clicked.connect(self.add_national_party)


                # Removing parties
                self.clear_national_button = QtWidgets.QPushButton(self)
                self.clear_national_button.setText('Clear National Parties')
                self.clear_national_button.setFont(QtGui.QFont('Arial', 15))
                self.clear_national_button.resize(600, 70)
                self.add_widget(self.clear_national_button)
                self.clear_national_button.clicked.connect(self.clear_national_parties)


            for party in national_parties:
                # Adding the party in each of the national parties
                self.add_widget(PartiesList.PartyButton(party, self))

        if local_parties != [] or self.region_type == 'region':
            # For regional parties
            local_parties_label = QtWidgets.QLabel("Regional Parties: ")
            local_parties_label.resize(700, 100)
            local_parties_label.setFont(QtGui.QFont('Arial', 20))
            self.add_widget(local_parties_label)

            # If you're editing regional parties
            if mode == 'edit' and self.region_type == 'region':
                self.add_regional_button = QtWidgets.QPushButton(self)
                self.add_regional_button.setText('Add Regional Party')
                self.add_regional_button.setFont(QtGui.QFont('Arial', 15))
                self.add_regional_button.resize(600, 70)
                self.add_widget(self.add_regional_button)
                self.add_regional_button.clicked.connect(self.add_regional_party)

                self.clear_regional_button = QtWidgets.QPushButton(self)
                self.clear_regional_button.setText('Clear Regional Parties')
                self.clear_regional_button.setFont(QtGui.QFont('Arial', 15))
                self.clear_regional_button.resize(600, 70)
                self.add_widget(self.clear_regional_button)
                self.clear_regional_button.clicked.connect(self.clear_regional_parties)

            for party in local_parties:
                # Adding regional parties
                self.add_widget(PartiesList.PartyButton(party, self))

    def add_national_party(self):
        if self.region_type == 'nation':
            party = e.Party(region=self.region)
            self.region.add_party(party)

            self.add_widget(PartiesList.PartyButton(party, self))

    def add_regional_party(self):
        if self.region_type == 'region':
            party = e.Party()
            self.region.add_party(party)

            self.add_widget(PartiesList.PartyButton(party, self))

    def clear_national_parties(self):
        if self.region_type == 'nation':
            self.nation.clear_parties()
            self.refresh()

            number_of_national_parties = len(self.region.parties)
            widgets = self.widgets()
            for widget in widgets[1:number_of_national_parties + 1]:
                self.remove_widget(widget)

    def clear_regional_parties(self):
        if self.region_type == 'region':

            widgets = self.widgets()
            number_of_regional_parties = len(self.region.get_local_parties())
            for widget in widgets[-number_of_regional_parties:]:
                # Regional buttons start from the bottom
                # Removes the last x widgets where x = number of regional parties
                print(widget)
                self.remove_widget(widget)
            self.region.clear_parties()

    def refresh(self):
        # Removes all widgets
        w = self.widgets()
        for widget in w:
            if type(widget) == self.PartyButton:
                self.remove_widget(widget)


    class PartyButton(QtWidgets.QPushButton):
        # Button for a PartyList
        def __init__(self, party ,ui):
            super(PartiesList.PartyButton, self).__init__(ui)
            self.party = party
            self.setText(party.name)

            self.setIcon(ColorIcon(party.color))
            self.ui = ui

            self.resize(600, 60)

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
    def __init__(self, ui = None):
        super(RepsList, self).__init__()
        if ui is not None:
            self.setParent(ui)

    def set_reps(self, representatives):
        self.clear()
        self.setStyleSheet('background-color: #777777')
        self.representatives = representatives
        self.views = [RepView(self, representative) for representative in representatives]
        for v in self.views:
            v.show()
        self.add_widgets(self.views)


class ColorIcon(QtGui.QIcon):
    def __init__(self, color):
        pixmap = QtGui.QPixmap(50, 50)
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
        self.show()

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
        self.candidate.name = self.nameedit.text()
        self.candidate.leaning = float(self.leaningedit0.text()), float(self.leaningedit1.text())
        self.candidate.relevance = float(self.relevanceedit.text())
        self.destroy()

    def select_party(self):
        if self.candidate.region.nation is not None:
            locals = self.candidate.region.get_local_parties()
            nationals = self.candidate.region.nation.parties
            partylist = PartiesList('select', locals, nationals)
        else:
            locals = self.candidate.region.get_local_parties()
            partylist = PartiesList('select', locals, [])
        while not partylist.selected_party:
            time.sleep(0.05)
            QtWidgets.QApplication.processEvents()
        partylist.destroy()
        self.candidate.party = partylist.selected_party
        self.partybutton.setText(self.candidate.party.name)
        self.partybutton.setIcon(ColorIcon(self.candidate.party.color))


class RepView(QtWidgets.QWidget):
    def __init__(self, window = None, representative = None):
        if window is None:
            super(RepView, self).__init__()
        else:
            super(RepView, self).__init__(window)

        self.font = QtGui.QFont()
        self.font.setPointSize(12)
        self.font.setFamily('Bahnschrift Light')
        self.bg_colors = ['#FFFFFF', '#EEEEEE']
        self.block_size = (800, 200)

        if representative is not None:
            self.representative = representative

        # self.resize(self.block_size[0], self.block_size[1])

        self.PartyColor = QtWidgets.QPushButton(self)
        self.PartyColor.clicked.connect(self.edit)
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

        self.setName(self.representative.name)
        self.setPartyName(self.representative.party.name)
        self.setPartyColor(self.representative.party.color)
        if self.representative.has_region():
            self.setRegionName(self.representative.region.get_name())
        else:
            self.setRegionName('No Region')


    def setPartyColor(self, color):
        self.PartyColor.setStyleSheet('background-color:' + color)

    def setName(self, name):
        self.NameLabel.setText(name)

    def setPartyName(self, name):
        self.PartyLabel.setText(name)

    def setRegionName(self, name):
        self.RegionLabel.setText(name)

    def edit(self):
        self.editor = CandEdit(self.representative)
        self.editor.donebutton.clicked.connect(self.refresh)

    def resize(self, x, y):
        super(RepView, self).resize(x, y)
        self.block_size = x, y
        

    def refresh(self):
        self.setName(self.representative.name)
        self.setPartyName(self.representative.party.name)
        self.setPartyColor(self.representative.party.color)
        try:
            self.setRegionName(self.representative.region.name)
        except:
            pass


class OptionSelector(WidgetList):
    def __init__(self, strings):
        super(OptionSelector, self).__init__()
        self.resize(400, 600)
        self.done = False
        self.choice = None
        for string in strings:
            self.add_widget(self.OptionButton(string, self))

    def option_selected(self, text):
        self.choice = text
        self.done = True
        #self.destroy()

    class OptionButton(QtWidgets.QPushButton):
        font = QtGui.QFont('Arial Bold', 14)
        def __init__(self, text, parent_ui):
            super(OptionSelector.OptionButton, self).__init__()
            self.resize(350, 100)
            self.setText(text)
            self.setFont(self.font)
            self.clicked.connect(lambda: parent_ui.option_selected(text))


class NationElectionRunner():
    def __init__(self, **kwargs):
        self.election = e.NationElection(nation=kwargs.get('nation', e.Nation()))

        self.vs_chooser = OptionSelector(self.election.voting_systems)

        while not self.vs_chooser.done:
            QtWidgets.QApplication.processEvents()
            time.sleep(0.02)

        if self.vs_chooser.choice == 'mmp':
            self.election.run(self.vs_chooser.choice)
        else:
            self.election.run(self.vs_chooser.choice)
        self.vs_chooser.destroy()

    class MMPOptions():
        def __init__(self):
            pass


class RegionElectionRunner():
    def __init__(self, **kwargs):
        if 'region' in kwargs:
            self.election = e.RegionElection(region=kwargs['region'])
        else:
            self.election = e.RegionElection()

        voting_systems= list(self.election.candidatesystems.keys()) + list(self.election.partylistsystems.keys())
        self.vs_chooser = OptionSelector(voting_systems)
        while not self.vs_chooser.done:
            QtWidgets.QApplication.processEvents()
            time.sleep(0.02)

        self.election.voting_system = self.vs_chooser.choice
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
            self.region = self.election.region
            self.done = False

            self.voting_systemlabel = QtWidgets.QLabel("Voting System: ")
            self.layout.setWidget(0, self.layout.LabelRole, self.voting_systemlabel)
            self.voting_systemfield = QtWidgets.QLabel(self.election.voting_system)
            self.layout.setWidget(0, self.layout.FieldRole, self.voting_systemfield)

            self.repsnumlabel = QtWidgets.QLabel("Number of Seats")
            self.layout.setWidget(1, self.layout.LabelRole, self.repsnumlabel)
            self.repsnumspinbox = QtWidgets.QSpinBox(self)
            self.repsnumspinbox.setMinimum(1)
            #self.repsnumspinbox.setMaximum(20)
            self.repsnumspinbox.setValue(self.election.region.seat_count)
            self.layout.setWidget(1, self.layout.FieldRole, self.repsnumspinbox)

            if election.voting_system in ['runoff', 'stv', 'borda', 'dowdall', 'fptp']:
                self.candslabel = QtWidgets.QLabel("Candidates")
                self.layout.setWidget(2, self.layout.LabelRole, self.candslabel)
                self.candsbutton = QtWidgets.QPushButton("Click to view candidates")
                self.candsbutton.clicked.connect(self.loadcandslist)
                self.layout.setWidget(2, self.layout.FieldRole, self.candsbutton)

            elif election.voting_system in ['dhondt', 'webster']:
                self.partieslabel = QtWidgets.QLabel("Parties")
                self.layout.setWidget(2, self.layout.LabelRole, self.partieslabel)
                self.partiesbutton = QtWidgets.QPushButton("Click to edit Parties")
                self.partiesbutton.clicked.connect(self.loadpartieslist)
                self.layout.setWidget(2, self.layout.FieldRole, self.partiesbutton)

            self.runbutton = QtWidgets.QPushButton('Run')
            self.runbutton.clicked.connect(self.runelection)
            self.layout.setWidget(3, self.layout.SpanningRole, self.runbutton)

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
                self.candslist.add_widget(self.CandButton(candidate))

        def loadpartieslist(self):
            if self.region.nation is not None:
                locals = self.region.get_local_parties()
                nationals = self.region.nation.parties
                self.partieslist = PartiesList('edit', locals, nationals, self.region)
            else:
                self.partieslist = PartiesList('edit', locals, [], self.region)

        class CandButton(QtWidgets.QPushButton):
            def __init__(self, candidate):
                super(RegionElectionRunner.ElectionOptions.CandButton, self).__init__()
                self.candidate = candidate
                self.edit = None
                self.resize(600, 100)

                text = self.candidate.name + '\n(' + self.candidate.party.name + ')'
                icon = ColorIcon(self.candidate.party.color)
                self.setText(text)
                self.setIcon(icon)

                self.clicked.connect(self.editcand)

            def editcand(self):
                if self.edit is not None:
                    self.edit.destroy()
                    self.edit = None
                self.edit = CandEdit(self.candidate)
                self.edit.donebutton.clicked.connect(self.refresh_button)


            def refresh_button(self):
                self.edit.save()
                text = self.candidate.name + '\n(' + self.candidate.party.name + ')'
                icon = ColorIcon(self.candidate.party.color)
                self.setText(text)
                self.setIcon(icon)

        class CandsList(WidgetList):
            def __init__(self, election):
                super(RegionElectionRunner.ElectionOptions.CandsList, self).__init__()
                self.election = election

                self.resize(660, 800)

                self.add_cands_layout = QtWidgets.QHBoxLayout(self)
                self.add_cands_button = QtWidgets.QPushButton('Add Candidates')
                self.add_cands_button.clicked.connect(self.add_candidates)
                self.add_cands_layout.addWidget(self.add_cands_button)
                self.add_cands_spinner = QtWidgets.QSpinBox()
                self.add_cands_spinner.setMinimum(1)
                #self.add_cands_spinner.setMaximum(40)
                self.add_cands_layout.addWidget(self.add_cands_spinner)
                self.add_cands_widget = QtWidgets.QWidget()
                self.add_cands_widget.setLayout(self.add_cands_layout)
                self.add_cands_widget.resize(620, 120)
                self.add_widget(self.add_cands_widget)

                self.add_party_cands_layout = QtWidgets.QHBoxLayout(self)
                self.add_party_cands_button = QtWidgets.QPushButton('Add Candidates \n From each party')
                self.add_party_cands_button.clicked.connect(self.add_party_candidates)
                self.add_party_cands_layout.addWidget(self.add_party_cands_button)
                self.add_party_cands_spinner = QtWidgets.QSpinBox()
                self.add_party_cands_spinner.setMinimum(1)
                #self.add_party_cands_spinner.setMaximum(10)
                self.add_party_cands_layout.addWidget(self.add_party_cands_spinner)
                self.add_party_cands_widget = QtWidgets.QWidget()
                self.add_party_cands_widget.setLayout(self.add_party_cands_layout)
                self.add_party_cands_widget.resize(620, 120)
                self.add_widget(self.add_party_cands_widget)


            def add_candidates(self):
                for i in range(self.add_cands_spinner.value()):
                    candidate = e.Candidate(region=self.election.region)
                    self.election.candidates.append(candidate)
                    candbutton = RegionElectionRunner.ElectionOptions.CandButton(candidate)
                    self.add_widget(candbutton)


            def add_party_candidates(self):
                for party in self.election.region.parties():
                    for i in range(self.add_party_cands_spinner.value()):
                        candidate = e.Candidate(region=self.election.region, party=party)
                        self.election.candidates.append(candidate)
                        candbutton = RegionElectionRunner.ElectionOptions.CandButton(candidate)
                        self.add_widget(candbutton)


class NationViewer(QtWidgets.QMainWindow):
    map_width = 2000
    map_height = 2000
    side_bar_width = 850

    class SideBar(WidgetList):
        font = QtGui.QFont()
        font.setFamily('Arial')
        font.setPointSize(15)
        class PartySeatsGraph(QtWidgets.QPushButton):
            def __init__(self, nation):
                super(NationViewer.SideBar.PartySeatsGraph, self).__init__()
                self.resize(NationViewer.side_bar_width - 50, 200)
                self.nation = nation

            def paintEvent(self, e):
                perc_by_party = self.nation.percentages_by_party()
                width_by_party = {party: perc_by_party[party] * self.width()/100 for party in perc_by_party}

                qp = QtGui.QPainter()
                qp.begin(self)
                x = 0
                if len(width_by_party.keys()) != 0:
                    for party in width_by_party:
                        color = QtGui.QColor(party.color)
                        qp.setPen(color)

                        qp.setBrush(color)
                        qp.setPen(color)

                        qp.setBrush(QtGui.QColor(color))
                        width = width_by_party[party]
                        qp.drawRect(round(x), 0, round(width), self.height())
                        x += width


                black_pen = QtGui.QPen()
                black_pen.setColor(QtGui.QColor('#000000'))
                black_pen.setWidth(int(self.width()/30))
                qp.setPen(black_pen)
                qp.setBrush(QtGui.QColor(0, 0, 0, 0))
                qp.drawRect(0, 0, self.width(), self.height())
                qp.end()

        class NationElectionButton(QtWidgets.QPushButton):
            def __init__(self, nation, side_bar):
                super(NationViewer.SideBar.NationElectionButton, self).__init__()
                self.resize(NationViewer.side_bar_width - 50, 200)
                self.nation = nation
                self.side_bar = side_bar
                self.setText('Run Election')
                self.clicked.connect(self.run_election)
                self.setFont(NationViewer.SideBar.font)
                self.show()

            def run_election(self):
                self.election = NationElectionRunner(nation=self.nation)
                self.side_bar.reps_list.set_reps(self.nation.representatives())

        def __init__(self, parent):
            super(NationViewer.SideBar, self).__init__(parent=parent, width=NationViewer.side_bar_width, height=NationViewer.map_height)

            self.parent_ui = parent
            self.add_regions_layout = QtWidgets.QHBoxLayout()
            self.add_regions_button = QtWidgets.QPushButton('Add Regions')
            self.add_regions_button.resize(400, 200)
            self.add_regions_button.setFont(NationViewer.SideBar.font)
            self.add_regions_button.clicked.connect(self.add_regions)
            self.add_regions_layout.addWidget(self.add_regions_button)
            self.add_regions_spinner = QtWidgets.QSpinBox()
            self.add_regions_spinner.setFont(NationViewer.SideBar.font)
            self.add_regions_spinner.resize(200, 200)
            self.add_regions_layout.addWidget(self.add_regions_spinner)
            self.add_regions_spinner.setMinimum(1)
            self.add_regions_spinner.setMaximum(99999)
            self.add_regions_widget = QtWidgets.QWidget(self)
            self.add_regions_widget.setLayout(self.add_regions_layout)
            self.add_regions_widget.resize(800, 100)
            self.add_widget(self.add_regions_widget)

            self.seat_count_layout = QtWidgets.QHBoxLayout()
            self.seat_count_button = QtWidgets.QPushButton('Set number of seats')
            self.seat_count_button.resize(400, 200)
            self.seat_count_button.clicked.connect(self.set_seat_count)
            self.seat_count_button.setFont(NationViewer.SideBar.font)
            self.seat_count_layout.addWidget(self.seat_count_button)
            self.seat_count_spinner = QtWidgets.QSpinBox()
            self.seat_count_spinner.setValue(self.parent_ui.nation.total_seat_count())
            self.seat_count_spinner.setMinimum(1)
            self.seat_count_spinner.setMaximum(999)
            self.seat_count_spinner.resize(200, 200)
            self.seat_count_spinner.setFont(NationViewer.SideBar.font)
            self.seat_count_layout.addWidget(self.seat_count_spinner)
            self.seat_count_widget = QtWidgets.QWidget()
            self.seat_count_widget.setLayout(self.seat_count_layout)
            self.seat_count_widget.resize(800, 100)
            self.add_widget(self.seat_count_widget)


            self.resize_layout = QtWidgets.QHBoxLayout()
            self.resize_button = QtWidgets.QPushButton('Resize Map')
            self.resize_button.resize(400, 200)
            self.resize_button.setFont(NationViewer.SideBar.font)
            self.resize_button.clicked.connect(self.resize_map)
            self.resize_layout.addWidget(self.resize_button)
            self.resize_spinner_0 = QtWidgets.QSpinBox()
            self.resize_spinner_1 = QtWidgets.QSpinBox()
            self.resize_spinner_0.resize(200, 200)
            self.resize_spinner_1.resize(200, 200)
            self.resize_spinner_0.setFont(NationViewer.SideBar.font)
            self.resize_spinner_1.setFont(NationViewer.SideBar.font)
            self.resize_spinner_0.setMinimum(1)
            self.resize_spinner_1.setMinimum(1)
            self.resize_spinner_0.setMaximum(20)
            self.resize_spinner_1.setMaximum(20)
            self.resize_layout.addWidget(self.resize_spinner_0)
            self.resize_layout.addWidget(self.resize_spinner_1)
            self.resize_widget = QtWidgets.QWidget(self)
            self.resize_widget.setLayout(self.resize_layout)
            self.resize_widget.resize(800, 100)
            self.add_widget(self.resize_widget)

            self.clear_button = QtWidgets.QPushButton('Clear Map')
            self.clear_button.setFont(NationViewer.SideBar.font)
            self.clear_button.clicked.connect(self.clear_map)
            self.clear_button.resize(400, 100)
            self.add_widget(self.clear_button)

            self.parties_list = PartiesList('edit', [], self.parent_ui.nation.parties, self.parent_ui.nation)
            self.parties_list.setParent(self)
            self.parties_list.resize(self.parent_ui.side_bar_width - 20, 500)
            self.add_widget(self.parties_list)

            self.add_widget(self.PartySeatsGraph(self.parent_ui.nation))

            self.nation_election_button = NationViewer.SideBar.NationElectionButton(self.parent_ui.nation, self)
            self.add_widget(self.nation_election_button)

            self.reps_list = RepsList(self)
            self.reps_list.resize(self.parent_ui.side_bar_width - 20, 500)
            self.reps_list.set_reps(self.parent_ui.nation.representatives())
            self.add_widget(self.reps_list)

            self.show()

        def add_regions(self):
            self.parent_ui.nation.create_regions(self.add_regions_spinner.value())
            self.parent_ui.map.refresh()

        def resize_map(self):
            x = self.resize_spinner_0.value()
            y = self.resize_spinner_1.value()
            self.parent_ui.nation.resize_map(x, y)
            self.parent_ui.map.refresh()

        def clear_map(self):
            self.parent_ui.nation.clear_map()
            self.parent_ui.map.refresh()
            self.reps_list.set_reps([])

        def set_seat_count(self):
            n = self.seat_count_spinner.value()
            self.parent_ui.nation.set_seat_count(n)

    def __init__(self, nation=None):
        super(NationViewer, self).__init__()
        if nation is None:
            nation = e.Nation()

        self.nation = nation
        self.map = NationMap(nation)
        self.map.setParent(self)
        self.map.move(0, 0)
        self.map.setFixedSize(self.map_width, self.map_height)

        self.resize(self.map_width + self.side_bar_width, self.map_height)

        self.side_bar = self.SideBar(self)
        self.side_bar.setGeometry(self.map_width, 0, self.side_bar_width, self.map_height)

        self.setWindowTitle('Electioneering')
        self.setWindowIcon(ColorIcon('#FFFFFF'))

        self.show()

    def add_region(self):
        self.nation.create_regions(1)
        self.map.refresh()

    def refresh(self):
        self.map.refresh()
        self.side_bar.reps_list.set_reps(self.nation.representatives())


class NationMap(QtWidgets.QScrollArea):
    width = 500
    height = 500

    def __init__(self, nation):
        super(NationMap, self).__init__()
        self.layout = QtWidgets.QGridLayout()
        self.layout.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.layout.setSpacing(5)
        self.region_map = nation.region_map
        self.nation = nation
        self.buttons = []
        self.blank_spaces = []

        self.setLayout(self.layout)

        self.refresh()
        self.show()

    def refresh(self):
        for button in self.buttons:
            button.hide()
            self.layout.removeWidget(button)
            button.destroy()
            del button

        for x in range(self.nation.map_width):
            for y in range(self.nation.map_height):
                    button = self.RegionButton(x, y, self)
                    self.layout.addWidget(button, y, x)
                    self.buttons.append(button)

    class RegionButton(QtWidgets.QPushButton):
        def __init__(self, x, y, nationmap):
            super(NationMap.RegionButton, self).__init__()
            self.view = None
            self.region = nationmap.nation.region_map[x][y]
            self.nation = nationmap.nation
            self.x, self.y = x, y

            policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.setSizePolicy(policy)

            #self.setMinimumSize(20, 20)

            self.clicked.connect(self.view_region)

        def view_region(self):
            if self.region is not None:
                self.regionviewer = RegionViewer(self.region)
            else:
                self.nation.add_region(None, self.x, self.y)
                self.region = self.nation.region_map[self.x][self.y]
                self.regionviewer = RegionViewer(self.region)

        def paintEvent(self, e):
            if self.region == None:
                qp = QtGui.QPainter()
                qp.begin(self)

                cx = self.width() // 2
                cy = self.height() // 2
                col = QtGui.QColor('#CCCCCC')
                qp.setBrush(col)
                qp.setPen(col)
                qp.drawEllipse(QtCore.QPoint(cx, cy), 10, 10)
            else:
                colors = [representative.party.color for representative in self.region.get_representatives()]
                total_rects = len(colors)
                color_count = dict(Counter(colors))

                qp = QtGui.QPainter()
                qp.begin(self)
                c = 0
                if total_rects != 0:
                    w = self.width() / total_rects
                    for color in color_count.keys():
                        col = QtGui.QColor(color)
                        qp.setPen(col)

                        qp.setBrush(col)
                        qp.setPen(col)

                        qp.setBrush(QtGui.QColor(col))
                        qp.drawRect(int(round(c * w)), 0, int(round(w * color_count[color])), self.height())
                        c += color_count[color]

                if self.width() > 95:
                    text_pen = QtGui.QPen()
                    if total_rects == 0:
                        text_pen.setColor(QtGui.QColor('#000000'))
                    else:
                        text_pen.setColor(QtGui.QColor('#FFFFFF'))
                    text_font = QtGui.QFont('Arial Black', int(min(self.width(), self.height())/20))
                    qp.setFont(text_font)
                    qp.setPen(text_pen)
                    name = self.region.get_name()
                    name = name.replace(' ', '\n')
                    self.setText(name)
                    qp.drawText(e.rect(), QtGui.Qt.AlignCenter, name)

                black_pen = QtGui.QPen()
                black_pen.setColor(QtGui.QColor('#000000'))
                black_pen.setWidth(int(self.width()/30) + 1)
                qp.setPen(black_pen)
                qp.setBrush(QtGui.QColor(0, 0, 0, 0))
                qp.drawRect(0, 0, self.width(), self.height())
                qp.end()

        def kill(self):
            self.paintEvent = self.nothing
            self.destroy()
            self.region = None
            del self

        def nothing(self):
            pass


class RegionViewer(QtWidgets.QWidget):
    c1_width = 700
    # Width of column one (Contains basic info and list of elections)
    c2_width = 700

    basic_info_height = 480
    electionlist_height = 600
    replist_height = basic_info_height + electionlist_height

    font = QtGui.QFont()
    font.setPointSize(12)
    font.setFamily('Bahnschrift Light')

    class BasicInfo(QtWidgets.QFormLayout):
        def __init__(self, region, ui):
            super(RegionViewer.BasicInfo, self).__init__(ui)
            self.region = region

            name = region.get_name()
            pop = region.population()
            bias = region.get_bias()
            seat_count = region.get_seat_count()

            self.name_label = QtWidgets.QLabel()
            self.name_label.setText("Name")
            self.name_label.setFont(RegionViewer.font)
            self.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.name_label)
            self.name_edit = QtWidgets.QLineEdit()
            self.name_edit.setText(name)
            self.name_edit.setFont(RegionViewer.font)
            self.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.name_edit)

            self.pop_label = QtWidgets.QLabel()
            self.pop_label.setText("Population")
            self.pop_label.setFont(RegionViewer.font)
            self.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.pop_label)
            self.pop_edit = QtWidgets.QSpinBox()
            self.pop_edit.setMaximum(999999)
            self.pop_edit.setMinimum(1)
            self.pop_edit.setValue(pop)
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
            self.biasedit0.setValue(bias[0])
            self.biasedit0.setFont(RegionViewer.font)
            self.biaslayout.addWidget(self.biasedit0)
            self.biasedit1 = QtWidgets.QDoubleSpinBox()
            self.biasedit1.setMinimum(-5)
            self.biasedit1.setMaximum(5)
            self.biasedit1.setDecimals(3)
            self.biasedit1.setValue(bias[1])
            self.biasedit1.setFont(RegionViewer.font)
            self.biaslayout.addWidget(self.biasedit1)
            self.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.biaslayout)

            self.seat_number_label = QtWidgets.QLabel('Seat Number')
            self.seat_number_label.setFont(RegionViewer.font)
            self.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.seat_number_label)
            self.seat_number_edit = QtWidgets.QSpinBox()
            self.seat_number_edit.setMinimum(1)
            self.seat_number_edit.setValue(seat_count)
            self.seat_number_edit.setFont(RegionViewer.font)
            self.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.seat_number_edit)

            self.parties_label = QtWidgets.QLabel()
            self.parties_label.setText("Parties")
            self.parties_label.setFont(RegionViewer.font)
            self.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.parties_label)
            self.parties_field = QtWidgets.QPushButton()
            self.parties_field.setText('View')
            self.parties_field.setFont(RegionViewer.font)
            self.parties_field.clicked.connect(self.editparties)
            self.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.parties_field)

            self.done_button = QtWidgets.QPushButton()
            self.done_button.setText("Save")
            self.done_button.setFont(RegionViewer.font)
            self.done_button.clicked.connect(self.save_info)
            self.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.done_button)

        def editparties(self):
            if self.region.nation is None:
                locals = self.candidate.region.get_local_parties()
                self.partieslist = PartiesList('edit', locals, [], self.region)
            else:
                locals = self.region.get_local_parties()
                nationals = self.region.nation.parties
                self.partieslist = PartiesList('edit', locals, nationals, self.region)

        def save_info(self):
            self.region.set_name(self.name_edit.text())
            self.region.set_bias((self.biasedit0.value(), self.biasedit1.value()))
            self.region.set_population(self.pop_edit.value())
            self.region.set_seat_count(self.seat_number_edit.value())


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

            self.resize(RegionViewer.c1_width, RegionViewer.electionlist_height)

            regional_election_button = QtWidgets.QPushButton(self)
            regional_election_button.setText('Run a Regional Election')
            regional_election_button.resize(600, 100)
            regional_election_button.setFont(RegionViewer.font)
            self.add_widget(regional_election_button)
            self.widgets()[-1].clicked.connect(self.add_election)

            elections = self.region.get_regional_elections()
            for e in range(len(elections)):
                self.add_widget(RegionViewer.ElectionButton(elections[e], e, self))

            self.setParent(self.ui)
            self.move(0, self.ui.basic_info_height)
            self.resize(RegionViewer.c1_width, RegionViewer.electionlist_height)

        def add_election(self):
            runner = RegionElectionRunner(region=self.region)
            election = runner.election
            self.add_widget(RegionViewer.ElectionButton(election, 0, self))
            self.ui.reload_repslist()

    def __init__(self, region, ui=None):
        super(RegionViewer, self).__init__()
        self.region = region
        self.ui = ui

        self.resize(self.c1_width + self.c2_width, self.replist_height)

        self.basicinfowidget = QtWidgets.QWidget(self)
        self.basicinfowidget.resize(self.c1_width, self.basic_info_height)
        self.basicinfowidget.setLayout(self.BasicInfo(self.region, self))

        self.electionlist = RegionViewer.ElectionList(self.region, self)
        self.electionlist.resize(self.c1_width, self.electionlist_height)

        self.repslist = RepsList(self)
        self.repslist.set_reps(self.region.get_representatives())
        self.repslist.move(self.c1_width, 0)
        self.repslist.resize(self.c2_width, self.replist_height)


        if self.ui is not None:
            self.setParent(self.ui)
        self.show()

    def reload_repslist(self):
        self.repslist.set_reps(self.region.get_representatives())


class ElectionTable(QtWidgets.QTableWidget):
    def __init__(self, election):
        super(ElectionTable, self).__init__()

        self.winner_color = '#80DA80'
        self.loser_color =  '#E39494'

        # Set the column headers
        if election.voting_system in ['runoff', 'stv', 'dhondt', 'webster']:
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
        if election.voting_system in ['dhondt', 'webster']:
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
        self.resize(600, 600)
        self.show()


class Runn():
    def __init__(self):
        self.n = e.Nation()
        self.n.resize_map(4, 4)
        self.nv = NationViewer(self.n)

def main():
    app = QtWidgets.QApplication(argv)
    t = Runn()
    app.exec_()


if __name__ == '__main__':
    main()