from PySide2 import QtWidgets, QtCore, QtGui
import random

class Snake:
    def __init__(self, **kwargs):
        self.board_width  = kwargs.get('w', 20)
        self.board_height = kwargs.get('h', 20)

        self.walls_kill = False
        self.alive = True

        self.snake_coords = []
        # snake_coords[-1] = head
        # snake_coords[0] = tail
        self.food_coord = (4, 4)
        self.snake_coords.append((self.board_width//2, self.board_height//2))
        self.direction = (0, 1)

    def tick(self):
        new_head = add(self.snake_coords[-1], self.direction)
        if new_head == self.food_coord:
            self.food_coord = self.food_loc()
        else:
            self.snake_coords = self.snake_coords[1:]

        if new_head in self.snake_coords or (self.walls_kill and not(0 <= new_head[0] < self.board_width and 0 <= new_head[0] < self.board_height)):
            self.kill()
        else:
            self.snake_coords.append(new_head)

    def food_loc(self):
        (fx, fy) = random.randint(0, self.board_width), random.randint(0, self.board_height)
        while (fx, fy) not in self.snake_coords:
            (fx, fy) = random.randint(0, self.board_width), random.randint(0, self.board_height)
        return (fx, fy)

    def kill(self):
        self.alive = False

class SnakeBoard(QtWidgets.QWidget):
    def __init__(self):
        super(SnakeBoard, self).__init__()
        self.resize(1000, 1000)
        self.game = Snake()
        self.snake_color = QtGui.QColor('#00FF00')

    def paintEvent(self, e):
        for sx, sy in Q


def add(c1, c2):
    return c1[0] + c2[0], c1[1] + c2[1]