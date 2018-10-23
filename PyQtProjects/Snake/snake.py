from PyQt5 import QtWidgets, QtGui, QtCore
from sys import argv
import random


class Options:  # Use this to change the options
    def __init__(self):
        self.tick_speed = 310
        # ^ Amount of time between each snake move (milliseconds)
        #   Anything less than 20 doesn't work very well
        #   Anything over 300 doesn't work very well

        self.speed_up_with_size = 0.982
        # ^ Allows you to speed up as you get longer
        #   Set as 1 to ignore this effect
        #   The lower the number the more it accelerates
        #   Keep this number between 0.8 and 1 (or otherwise it's very extreme)
        #   Anything over 1 will slow down as you get longer

        self.board_size = (10, 10)
        # ^ Size of the grid (width, height)

        self.window_size = (600, 600)
        # ^ Size of the window (width, height)

        self.controls_size = 100
        # ^ Size of the controls on the right
        #   But you can use WASD


class MainGame:
    def __init__(self):
        self.ui = Ui(self)
        self.options = Options()

        self.snakes = []
        self.food = ""
        self.direction = (0, 0)
        self.timer_available = True
        self.del_last_piece = True
        self.ui.init_ui()
        self.ui.show()

        self.add_snake_piece((1, 1))
        self.food = Food(self.ui, (0, 0))
        self.main_loop()
        self.dead = False
        self.turning = False

    def food_eaten(self):
        self.del_last_piece = False

    def change_direction(self, change):
        valid_turn = True
        if change[0] == self.direction[0] or change[1] == self.direction[1]:
            # ^Makes sure that you're only turning 90 degrees
            valid_turn = False

        if change == self.direction:
            valid_turn = False

        if self.direction == (0, 0):
            valid_turn = True

        if self.turning:
            valid_turn = False

        if valid_turn:
            self.turning = True
            self.direction = change

    def place_snake(self):
        pass

    def add_snake_piece(self, coords):
        x, y = coords
        snake_piece = SnakePiece(self.ui, coords, self.ui.scale)
        snake_piece.show()

        self.snakes = [snake_piece] + self.snakes

    def main_loop(self):
        self.dead = False
        tick_count = 0
        while not self.dead:
            tick_count += 1
            if self.timer_available:
                self.timer_available = False
                tick_speed = self.options.tick_speed * (self.options.speed_up_with_size ** (len(self.snakes) - 1))
                timer = QtCore.QTimer()
                timer.timeout.connect(self.main_loop_timer_done)
                timer.start(tick_speed)
            QtGui.QGuiApplication.processEvents()

    def main_loop_timer_done(self):
        self.tick()
        self.timer_available = True

    def tick(self):
        self.turning = False

        newx = self.snakes[0].x + self.direction[0]
        newy = self.snakes[0].y + self.direction[1]
        newx, newy = self.check_edges(newx, newy)
        self.add_snake_piece((newx, newy))
        self.remove_last_piece()
        self.color_head()
        self.check_food()
        self.check_dead()



    def check_edges(self, newx, newy):
        if self.snakes[0].x + self.direction[0] > (self.ui.grid_size[0] - 1):
            newx = 0
        if self.snakes[0].y + self.direction[1] > (self.ui.grid_size[1] - 1):
            newy = 0
        if self.snakes[0].x + self.direction[0] < 0:
            newx = self.ui.grid_size[0] - 1
        if self.snakes[0].y + self.direction[1] < 0:
            newy = self.ui.grid_size[1] - 1
        return(newx, newy)

    def remove_last_piece(self):
        if self.del_last_piece:
            self.snakes[-1].hide()
            del self.snakes[-1]
        else:
            self.del_last_piece = True

    def color_head(self):
        self.snakes[0].setStyleSheet("background-color: #55DD55")
        if len(self.snakes) > 1:
            self.snakes[1].setStyleSheet("background-color: #22FF22")

    def check_food(self):
        if (self.snakes[0].x, self.snakes[0].y) == (self.food.x, self.food.y):
            self.food.goto((random.randint(0, self.ui.grid_size[0] - 1), random.randint(0, self.ui.grid_size[1] -1)))
            self.del_last_piece = False

    def check_dead(self):
        piece_coords = []
        for snake in self.snakes:
            if (snake.x, snake.y) in piece_coords:
                self.game_over()
                self.dead = True
            piece_coords.append((snake.x, snake.y))


    def game_over(self):
        self.snakes[0].setStyleSheet("background-color: #DD2222")
        for snake in self.snakes[1:]:
            snake.setStyleSheet("background-color: #EE1111")


class Ui(QtWidgets.QMainWindow):
    def __init__(self, maingame):
        super(Ui, self).__init__()
        self.parent = maingame
        self.options = Options()
        self.board = {}

        self.window_size = self.options.window_size
        self.grid_size = self.options.board_size

        self.margin = (5, 5, 5, self.options.controls_size) #Top margin, Bottom margin, Left Margin, Right Margin
        self.borders = (0, 0)
        self.piece_size = 0
        self.scale = 0

        self.widgets = self.Widgets()

    class Widgets:
        pass

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_W:
            self.parent.change_direction((0, -1))
        elif e.key() == QtCore.Qt.Key_A:
            self.parent.change_direction((-1, 0))
        elif e.key() == QtCore.Qt.Key_S:
            self.parent.change_direction((0, 1))
        elif e.key() == QtCore.Qt.Key_D:
            self.parent.change_direction((1, 0))


    def init_ui(self):
        self.piece_size = min(self.window_size)
        boardx, boardy = self.window_size
        xcount, ycount = self.grid_size
        borderx, bordery = self.borders

        self.scale = (boardx / xcount, boardy / ycount)

        self.resize(boardx + self.margin[2] + self.margin[3], boardy + self.margin[0] + self.margin[1])

        self.widgets.arrow_up = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_up, "up")
        self.widgets.arrow_dn = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_dn, "dn")
        self.widgets.arrow_rt = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_rt, "rt")
        self.widgets.arrow_lt = QtWidgets.QPushButton(self)
        self.make_arrow_button(self.widgets.arrow_lt, "lt")

        #self.widgets.arrow_lt = QtWidgets.QPushButton(self)
        #self.make_arrow_button(self.widgets.arrow_lt, "no")
        # ^Optional pause button




    def make_arrow_button(self, arrow, direction):
        direction_chr = {"up": "W", "dn": "S", "rt": "D", "lt": "A", "no": "||"}
        direction_change = {"up": (0, -1), "dn": (0, 1), "rt": (1, 0), "lt": (-1, 0), "no": (0, 0)}

        symbol = direction_chr[direction]
        arrow.setText(symbol)

        change = direction_change[direction]

        smallest_size = min([self.margin[3], self.height()])

        width = smallest_size / 3
        height = smallest_size / 3

        arrow.resize(width, height)
        xpos = self.width() - width*(-1 * change[0] + 2)
        ypos = 0 + height*(1 * change[1] + 1)
        arrow.move(xpos, ypos)

        font_size = int(smallest_size / 5)

        arrow.setStyleSheet("font-size: "+str(font_size)+"px;")

        arrow.clicked.connect(lambda x: self.parent.change_direction(change))


class Food(QtWidgets.QPushButton):
    def __init__(self, ui, coords):
        super(Food, self).__init__(ui)
        self.x, self.y = coords
        self.scalex, self.scaley = ui.scale
        self.ui = ui
        self.goto(coords)
        self.setStyleSheet("background-color: #eebb88")
        self.resize(self.scalex, self.scaley)
        self.show()

    def goto(self, location):
        x, y = location
        self.move(x * self.scalex + self.ui.margin[2], y*self.scaley + self.ui.margin[0])
        self.x, self.y = location


class SnakePiece(QtWidgets.QPushButton):
    def __init__(self, ui, coords, scale):
        super(SnakePiece, self).__init__(ui)
        self.x, self.y = coords
        self.scalex, self.scaley = scale
        self.ui = ui
        self.goto(coords)
        self.setStyleSheet("background-color: #33EE33")
        self.show()

    def goto(self, location):
        x, y = location
        self.x, self.y = location
        self.move(x * self.scalex + self.ui.margin[2], y*self.scaley + self.ui.margin[0])
        self.resize(self.scalex, self.scaley)
        self.show()



def main():
    app = QtWidgets.QApplication(argv)
    game = MainGame()
    app.exec_()


if __name__ == '__main__':
    main()