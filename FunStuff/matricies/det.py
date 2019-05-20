import random
import time

class Matrix(list):
    def __init__(self, h, w, fill = []):
        super(Matrix, self).__init__()

        self.h = h
        self.w = w
        self.square = self.h == self.w
        self.vector = self.w == 1 and self.h != 0

        for y in range(h):
            self.append([])
            for x in range(w):
                self[y].append(0)

        if fill != []:
            self.set(fill)

    def set_value(self,h, w, value):
        if 0 <= h <= self.h and 0 <= w <= self.w:
            self[h][w] = value

    def set(self, l):
        if type(l[0]) == list:
            self.set_2d(l)
        elif type(l[0]) == int:
            self.set_1d(l)

    def set_2d(self, l):
        if len(l) == self.h and len(l[0]) == self.w:
            for row in range(self.h):
                for col in range(self.w):
                    self[row][col] = l[row][col]
        else: return  False

    def set_1d(self, li):
        if len(li) == self.h * self.w:
            for i in range(len(li)):
                y = int(i / self.w)
                x = i % self.w
                self[y][x] = li[i]
        else: return False

    def fill(self, num):
        for r in range(self.h):
            for c in range(self.w):
                self[r][c] = num
                
    def det(self):
        if not self.square:
            return None
        if self.w == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]
        else:
            sign = 1
            d = 0
            for i in range(self.w):
                mini = self.sub_matrix(i , 0)
                d += self[0][i] * sign * mini.det()
                sign *= -1
            return d

    def list_vals(self):
        l = []
        for r in self:
            for i in r:
                l.append((i))
        return l

    def is_flat(self):
        return self.det() == 0

    def area_change(self):
        return abs(self.det())

    def sub_matrix(self, targeth, targetw):
        nh, nw = -1, -1
        mini = Matrix(self.h -1, self.w -1)
        for h in range(self.h):
            if h != targeth:
                nh += 1
                nw = -1
                for w in range(self.w):
                    if not (h == targeth or w == targetw):
                        nw += 1
                        mini[nh][nw] = self[h][w]
        return mini

    def adjunct(self):
        adj = Matrix(self.w, self.h)
        for h in range(self.h):
            for w in range(self.w):
                adj[w][h] = self[h][w]
        return adj

    def inverse(self):
        if not self.square:
            return False
        det = self.det()
        if self.h == 2:
            if det == 0:
                return False
            abcd = self.list_vals()
            a, b, c, d = abcd[0], abcd[1], abcd[2], abcd[3]
            return MMult(Matrix(2,2, [d, -1*b, -1*c, a]), 1 / det)

        else:
            inv = Matrix(self.h, self.w)
            for h in range(self.h):
                for w in range(self.w):
                    plus_or_minus = ((h + w)%2)*-2 +1
                    inv[h][w] = self.sub_matrix(h,w).det() * plus_or_minus

            inv = MMult(inv.adjunct(), 1 / det)
            return  inv

    def randomize(self):
        for h in range(self.h):
            for w in range(self.w):
                self[h][w] = random.randint(0, 155)

    def transform(self, coord_list):
        new_list = []
        for coord in coord_list:
            new_list.append(MMult(self, coord))
        return new_list

    def __str__(self):
        strings = []
        max_width = 0
        for x in self:
            for y in x:
                if len(str(y)) > max_width:
                    max_width = len(str(y))

        max_width = str(max_width)
        for h in range(self.h):
            strings.append("")
            strings[h] += "│ "
            for j in range(self.w):
                strings[h] += '{:^'+max_width+'}'
                strings[h] = strings[h].format(self[h][j])
                strings[h] += ' '
            strings[h] = strings[h]
            strings[h] += '│'
        top = "╭╴" + " "*(len(strings[0]) - 4) + "╶╮"
        bottom = "╰╴" + " "*(len(strings[0]) - 4) + "╶╯"
        strings.insert(0, top)
        strings.append(bottom)

        string = "\n"
        for row in strings:
            string += row
            string += '\n'
        return string

    def __add__(self, other):
        return MAdd(self, other)

    def __sub__(self, other):
        return MSub(self, other)

    def __mul__(self, other):
        return MMult(self, other)

    def __truediv__(self, other):
        return MDiv(self, other)

def MAdd(m1, m2):
    if (m1.h, m1.w) == (m2.h, m2.w):
        new = Matrix(m1.h, m2.w)
        for h in range(m1.h):
            for w in range(m2.w):
                v = m1[h][w] + m2[h][w]
                new.set_value(h,w,v)
    else:
        return False


def MSub(m1, m2):
    if (m1.h, m1.w) == (m2.h, m2.w):
        new = Matrix(m1.h, m2.w)
        for h in range(m1.h):
            for w in range(m2.w):
                v = m1[h][w] - m2[h][w]
                new.set_value(h,w,v)
    else:
        return False


def MMult(m1, m2):
    nums = [int, float]
    if type(m1) in nums and type(m2) in nums:
        return m1 * m2
    elif type(m1) in nums and type(m2) == Matrix:
        m3 = Matrix(m2.h, m2.w)
        for h in range(m2.h):
            for w in range(m2.w):
                m3.set_value(h, w, m1 * m2[h][w])
        return m3
    elif type(m1) == Matrix and type(m2) in nums:
        return MMult(m2, m1)
    else:
        if m1.w == m2.h:
            mult = Matrix(m1.h, m2.w)
            for h in range(m1.h):
                for w in range(m2.w):
                    current = 0
                    for i in range(m1.w):
                        current += m1[h][i] * m2[i][w]
                    mult[h][w] = current
            return mult
        else:
            return False

def MDiv(m1, m2):
    return MMult(m1, m2.inverse())
M = Matrix