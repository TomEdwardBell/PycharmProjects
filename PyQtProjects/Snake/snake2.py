from PySide2 import QtWidgets, QtCore, QtGui
import random
from sys import argv

class Snake:
    def __init__(self, **kwargs):
        self.board_width  = kwargs.get('w', 40)
        self.board_height = kwargs.get('h', 40)

        self.edges_kill = False
        self.restart()

    def restart(self):
        self.alive = True
        self.snake_coords = [(self.board_width//2, self.board_height//2)]
        self.direction = (0, 1)
        self.walls = []
        self.food_coord = self.food_loc()
        for i in range(6):
            self.walls += self.create_wall()

    def create_wall(self):
        x, y = (random.randint(0, self.board_width), random.randint(0, self.board_height))
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        walls = []
        while 0 <= x < self.board_width and 0 <= y < self.board_height:
            walls.append((x, y))
            x, y = add((x, y), direction)

        return walls

    def tick(self):
        new_head = add(self.snake_coords[-1], self.direction)

        if new_head == self.food_coord:
            self.food_coord = self.food_loc()
        else:
            self.snake_coords = self.snake_coords[1:]

        if new_head in self.snake_coords or new_head in self.walls:
            self.kill()
        if self.edges_kill:
            if not(0 <= new_head[0] < self.board_width and 0 <= new_head[1] < self.board_height):
                self.kill()
        elif not(0 <= new_head[0] < self.board_width and 0 <= new_head[1] < self.board_height):
            new_head = new_head[0] % self.board_width, new_head[1] % self.board_height

        if self.alive:
            self.snake_coords.append(new_head)

    def set_direction(self, direction):
        dx,dy = direction
        ox, oy = self.direction
        if (dx + ox) != 0 and (dy + oy) != 0:
            self.direction = direction

    def food_loc(self):
        (fx, fy) = random.randint(0, self.board_width - 1), random.randint(0, self.board_height - 1)
        while (fx, fy) in self.snake_coords or (fx, fy) in self.walls:
            (fx, fy) = random.randint(0, self.board_width - 1), random.randint(0, self.board_height - 1)
        return (fx, fy)

    def kill(self):
        self.alive = False

class ContainerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ContainerWindow, self).__init__()
        self.show()


class SnakeBoard(QtWidgets.QWidget):
    def __init__(self):
        super(SnakeBoard, self).__init__()
        self.resize(2000, 2000)
        self.game = Snake()
        self.snake_color = QtGui.QColor(0, 255, 0)
        self.food_color =  QtGui.QColor('#FF0000')
        self.wall_color =  QtGui.QColor('#FFFF00')

        self.timer = None

        self.setStyleSheet('background-color: #333333;')

        self.show()

        self.restart()

    def tps(self):
        return 5*len(self.game.snake_coords)**0.3 + 1

    def do_timer(self):
        if self.game.alive:
            self.game.tick()
            self.repaint()
            self.timer.setInterval(int(1000/self.tps()))
        else:
            self.timer.stop()
            self.repaint()
            restart_timer = QtCore.QTimer(self)
            restart_timer.start(5000)
            restart_timer.timeout.connect(self.restart())

    def restart(self):
        self.timer = QtCore.QTimer(self)
        self.timer.start(int(1000/self.tps()))
        self.timer.timeout.connect(self.do_timer)
        self.game.restart()

    def new_snake_color(self):
        print('new color')
        self.snake_color = QtGui.QColor.fromHsv(random.randint(0, 255), 255, 255)
        if random.random() < 0.5:
            self.game.snake_coords = self.game.snake_coords[1:]

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_E:
            self.new_snake_color()

        key_directions = {
            QtCore.Qt.Key_W: (0, -1),
            QtCore.Qt.Key_A: (-1, 0),
            QtCore.Qt.Key_S: (0, 1),
            QtCore.Qt.Key_D: (1, 0),
                          }

        for key in key_directions:
            if e.key() == key:
                self.game.set_direction(key_directions[key])

    def paintEvent(self, e):
        piece_width = self.width() / self.game.board_width
        piece_height = self.height() / self.game.board_height
        coords = self.game.snake_coords
        snake_pen = QtGui.QPen(self.snake_color, 0)
        food_pen = QtGui.QPen(self.food_color, 0)
        fx, fy = self.game.food_coord


        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setPen(snake_pen)
        qp.setBrush(self.snake_color)

        if self.game.alive:
            sx, sy = coords[-1]
            qp.drawRect(int(sx * piece_width), int(sy * piece_height), int(piece_width), int(piece_height))
            for sx, sy in coords[:-1]:
                qp.drawRect(int(sx * piece_width), int(sy * piece_height), int(piece_width), int(piece_height))

            qp.setPen(food_pen)
            qp.setBrush(self.food_color)
            qp.drawRect(int(fx * piece_width), int(fy * piece_height), int(piece_width), int(piece_height))

            qp.setBrush(self.wall_color)
            for wx, wy in self.game.walls:
                qp.drawRect(int(wx * piece_width), int(wy * piece_height), int(piece_width), int(piece_height))

        if not self.game.alive:
            font = QtGui.QFont()
            font.setPointSize(100)
            font.setFamily('papyrus')
            font.setBold(True)
            qp.setFont(font)
            qp.setBrush(self.food_color)
            qp.setPen(QtGui.QPen(self.food_color))
            qp.drawText(0, 0, self.width(), self.height()//1.2, 100, 'YOU \n FUCKING \n DIED')

        qp.end()


def add(c1, c2):
    return c1[0] + c2[0], c1[1] + c2[1]


def main():
    app = QtWidgets.QApplication(argv)
    s = SnakeBoard()
    app.exec_()


if __name__ == '__main__':
    main()