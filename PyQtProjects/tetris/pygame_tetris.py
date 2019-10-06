import random
import pygame

class Options:
    board_width = 10
    board_height = 24
    window_size = (400, 960)
    time_gap = 0.2

    shapes = [
        #[(0, 0)], # Single block
        [(0, 0), (1, 0), (1, 1)] # Large Square
    ]

    colors = {
        'dead': '#555555',
        'active': '#FF0000',
        'empty': '#FFFFFF'
    }

class Board(dict):
    def __init__(self):
        super(Board, self).__init__()
        self.running = True
        self.dead = []
        self.active = []
        self.center = (0, 0)
        self.fill()
        self.ui_commands = []

    def fill(self):
        for y in range(Options.board_height):
            for x in range(Options.board_width):
                self[x, y] = Empty()

    def new_piece(self):
        self.active = []
        shape = random.choice(Options.shapes)
        self.center = (int(Options.board_width/2), 0)
        for shape_coord in shape:
            coord = coord_add(shape_coord, self.center)
            if type(self[coord]) != Empty:
                self.game_over()
                return None
            else:
                self[coord] = Piece()
                self.active.append(coord)

    def tick(self):
        if self.check((0, 1)):
            self.move((0, 1))
        else:
            self.kill_piece()
            for row in self.check_rows():
                self.clear_row(row)
            self.new_piece()

    def check(self, direction):
        for c in self.active:
            new = coord_add(c, direction)
            if not(-1 < new[0] < Options.board_width and -1 < new[1] < Options.board_height):
                return False
            if new not in self.active and not type(self[new]) == Empty :
                return False
        return True

    def kill_piece(self):
        for c in self.active:
            self.dead.append(self[c])
            self[c].die()
        self.active = []

    def input(self, key):
        if key == "w":
            self.rotate()
        elif key == "s":
            self.down()
        elif key == "a":
            self.move((-1, 0))
        elif key == "d":
            self.move((1, 0))

    def move(self, direction):
        new_active = []
        # Find out new positions
        for c in self.active:
            new = coord_add(c, direction)
            new_active.append(new)

        # Add new pieces
        for n in new_active:
            if n not in self.active:
                self.make_active(n)

        # Remove old pieces
        for c in self.active:
            if c not in new_active:
                self.make_empty(c)

        # Update self.active
        self.active = new_active
        self.center = coord_add(self.center, direction)

    def down(self):  # Moves piece downwards until it hits the bottom
        clear = self.check((0, 1))
        while clear:
            self.move((0, 1))
            self.display()
            clear = self.check((0, 1))

    def check_move(self, direction):
        if self.check(direction):
            self.move(direction)
            self.display()

    def display(self):
        print('--------------------')
        for y in range(Options.board_height):
            line = ''
            for x in range(Options.board_width):
                item = self[x, y]
                line += str(item)
            print(line)

    def check_rows(self):
        rows = []
        for y in range(Options.board_height):
            full = True
            for x in range(Options.board_width):
                if type(self[x, y]) == Empty:
                    full = False
                elif not self[x, y].dead:
                    full = False
            if full:
                rows.append(y)
        return rows

    def clear_row(self, row):
        for y in range(row, 0, -1):
            for x in range(Options.board_width):
                if (x, y) not in self.active:
                    self[x, y] = self[x, y - 1]
                    if (x, y - 1) in self.dead:
                        self.dead.remove((x, y - 1))
                        self.dead.append((x, y))
        for x in range(Options.board_width):
            self[x, 0] = Empty()

    def rotate(self):
        clear = True
        cx, cy = self.center
        for (x, y) in self.active:
            newx, newy = -(y-cy)+cx, (x-cx)+cy
            if not(0 <= newx < Options.board_width and 0 <= newy < Options.board_height):
                clear = False
            elif type(self[newx, newy]) != Empty and (newx, newy) not in self.active:
                clear = False
        if clear:
            # Find out new positions
            new_active = []
            for (x, y) in self.active:
                newx, newy = -(y-cy)+cx,  (x-cx)+cy
                new_active.append((newx, newy))

            # Add new pieces
            for n in new_active:
                if n not in self.active:
                    self.make_active(n)

            # Remove old pieces
            for c in self.active:
                if c not in new_active:
                    self.make_empty(c)

            self.active = new_active
            self.make_active(new_active)

    def make_empty(self, c):
        x, y = c
        self[c] = Empty()
        self.state = "empty"
        self.ui_commands.append((x, y, 'empty'))

    def make_active(self, c):
        x, y = c
        self[c] = Piece()
        self.state = "active"
        self.ui_commands.append((x, y, 'active'))

    def game_over(self):
        self.ui_commands.append("QUIT")


class Empty():
    def __init__(self):
        self.state = "empty"

    def __str__(self):
        return '▢'

    def die(self):
        pass


class Piece():
    def __init__(self):
        super(Piece, self).__init__()
        self.dead = False
        self.state = "active"

    def __str__(self):
        if self.dead:
            return '▩'
        else:
            return '▣'

    def die(self):
        self.dead = True
        self.state = "dead"


def coord_add(t1, t2):
    return t1[0] + t2[0], t1[1] + t2[1]


class TetrisScreen():
    def __init__(self, window_size, grid_size, game):
        super(TetrisScreen, self).__init__()
        self.window_size = window_size
        self.grid_size = grid_size
        self.square_size = self.grid_size[0] / self.window_size[0], self.grid_size[1] / self.window_size[1]

        self.game = game

        self.state_colors = {
            'dead': '#555555',
            'active': '#FF0000',
            'empty': '#FFFFFF'
        }

    def create_pygame(self):
        pygame.init()

        self.screen = pygame.display.set_mode(self.window_size)
        self.game_finished = False

        xsize, ysize = self.square_size

    def set_color(self, coords, color):
        x, y = coords
        xsize, ysize = self.square_size
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, xsize, ysize))


    def display(self):
        for

    def run_game(self):
        clock = pygame.time.Clock()

        while not self:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]: self.game.input("w")
            if pressed[pygame.K_a]: self.game.input("a")
            if pressed[pygame.K_s]: self.game.input("s")
            if pressed[pygame.K_d]: self.game.input("d")

            self.game.tick()

            self.display(self.game)

            self.game.ui_commands = []

            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

b = Board()

t = TetrisScreen((500, 1000), (5, 10), Board())
t.create_pygame()
t.run_game()