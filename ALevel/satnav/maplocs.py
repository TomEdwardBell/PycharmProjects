import pygame
import time
import random
import json


class Options():
    pass


class Map():
    def __init__(self):
        self.points = []
        self.roads = []

    def adj_list(self):
        # Converts the Map into an adjecency list
        # Used for dijkstras
        adj = {point: {} for point in self.points}
        for point in self.points:
            for road in point.roads:
                other = None
                if road.a != point:
                    other = road.a
                elif road.b != point:
                    other = road.b
                adj[point][other] = road.time()
        return adj

    def point_at(self, pos):
        # Checks if theres a point at a certain (x, y) position
        for point in self.points:
            if pos == point.pos():
                return True
        return False

    def merge_points(self, p1, p2):
        # If two separate points have the same position, it merges them into one
        pass

    def create_point(self, name, pos):
        p = Point()
        p.name = name
        p.x, p.y = pos
        self.points.append(p)

        return p

    def connect(self, a, b):
        # Long function that allows you to connect to roads together
        # Most of the code here deals with allowing lines to intersect
        class Intersection(Point):
            def __init__(self, x, y, roads):
                super(Intersection, self).__init__(x, y)
                self.roads = roads

        def x_intersect(a, b, p, q, pos):
            # Connects a-b and p-q with the intersection at pos
            inter = self.create_point("", pos)
            self.connect(a, inter)
            self.connect(inter, b)
            self.connect(p, inter)
            self.connect(inter, q)

        def y_intersect(a, b, c, center):
            # conects a,b and c to the a particular center point
            self.connect(a, center)
            self.connect(center, b)
            self.connect(center, c)

        def orientation(p, q, r):
            # Returns orientation of two points
            val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
            if val < 0:
                val = -1  # -1 = Anti-clockwise
            elif val > 0:
                val = 1  # 1 = clockwise
            # 0 = colinear
            return val

        def check_intersection(line1, line2):
            # If they intersect, it returns True
            # If not, it returns False
            if ((orientation(line1.a, line1.b, line2.a) != orientation(line1.a, line1.b, line2.b)) and
                    (orientation(line2.a, line2.b, line1.a) != orientation(line2.a, line1.a, line1.b))):
                return True
            else:
                return False

        def find_poi(l1, l2):
            # Taken from
            # www.topcoder.com/community/competitive-programming
            # /tutorials/geometry-concepts-line-intersection-and-its-applications/

            A1, B1, C1 = l1.eq_form()
            A2, B2, C2 = l2.eq_form()c

            det = A1 * B2 - A2 * B1
            if det == 0:
                return False
            else:
                x = (B2 * C1 - B1 * C2) / det
                y = (A1 * C2 - A2 * C1) / det
                x, y = round(x), round(y)

            return x, y

        def in_range(line1, line2):
            # If two lines are very far apart it doesnt bother checking them for intersection
            if min(line1.a.x, line1.b.x) > max(line2.a.x, line2.b.x): return False
            if min(line2.a.x, line2.b.x) > max(line1.a.x, line1.b.x): return False
            if min(line1.a.y, line1.b.y) > max(line2.a.y, line2.b.y): return False
            if min(line2.a.y, line2.b.y) > max(line1.a.y, line1.b.y): return False
            return True

        def elements_shared(list1, list2):
            result = 0
            for element in list1:
                if element in list2:
                    result += 1
            return result

        def common_elements(list1, list2):
            result = []
            for element in list1:
                if element in list2:
                    result.append(element)
            return result

        # Finds the first intersection between a point and a road
        new_road = Road(a, b)
        intersection_found = False
        for road in self.roads:
            if in_range(road, new_road):
                if check_intersection(road, new_road):
                    intersection_found = True
                    ix, iy = find_poi(road, new_road)
                    poi = ix, iy
                    r1, r2 = road, new_road
                    if poi in [r1.a.pos(), r1.b.pos()] and poi in [r2.a.pos(), r2.b.pos()]:
                        intersection_found = False
                    elif poi in [r1.a.pos(), r1.b.pos()]:
                        # Y or T shaped intersection
                        print("T1")
                        inter = list(filter(lambda p: p.pos() == poi, [r1.a, r1.b]))[0]
                        r1_point = list(filter(lambda p: p.pos() != poi, [r1.a, r1.b]))[0]
                        self.delete_road(road)
                        y_intersect(r2.a, r2.b, r1_point, inter)
                        break

                    elif poi in [r2.a.pos(), r2.b.pos()]:
                        # Y or T shaped intersection
                        print("T2")
                        inter = list(filter(lambda p: p.pos() == poi, [r2.a, r2.b]))[0]
                        r2_point = list(filter(lambda p: p.pos() != poi, [r2.a, r2.b]))[0]
                        self.delete_road(road)
                        y_intersect(r1.a, r1.b, r2_point, inter)
                        break
                    else:
                        print("X")
                        self.delete_road(road)
                        x_intersect(r1.a, r1.b, r2.a, r2.b, poi)
                        break


        if not intersection_found:
            self.roads.append(Road(a,b))


    def delete_point(self, p):
        if p in self.points:
            for r in p.roads:
                self.delete_road(r)

    def delete_road(self, r):
        r.a.roads.remove(r)
        r.b.roads.remove(r)
        if r in self.roads:
            self.roads.remove(r)
        # del r

    def view(self):
        self.view = Mapview(self)
        self.view.show()

    def save(self):

    # Exports the map into a JSON file

    def open(self, file):


class Road():
    def __init__(self, a, b):
        self.a = a
        self.b = b
        a.roads.append(self)
        b.roads.append(self)

        self.speed = 10

        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def distance(self):
        ax, ay = self.a.pos()
        bx, by = self.b.pos()
        return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5

    def time(self):
        return self.distance() / self.speed

    def eq_form(self):
        # In the form Ax + By = C
        A = self.b.y - self.a.y
        B = self.a.x - self.b.x
        C = A * self.a.x + B * self.a.y
        return A, B, C


class Point():
    def __init__(self, x=None, y=None):
        self.roads = []
        self.name = ""
        self.x = x
        self.y = y

        if x is not None and y is not None:
            self.x, self.y = round(self.x), round(self.y)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def pos(self):
        return self.x, self.y

    def set_pos(self, coord):
        self.x, self.y = coord


class Mapview():
    def __init__(self, map):
        self.borders = {'left': 40, 'right': 40, 'top': 40, 'bottom': 40}

        self.zoom = 1
        # zoom>1, zooms in
        # zoom<1, zooms out

        self.bg_color = (16, 16, 16)

        self.point_color = (255, 255, 0)
        self.point_radius = 10

        self.road_color = (0, 0, 255)
        self.road_width = 3

        self.font = 'freesansbold.ttf'
        self.font_size = 15
        self.font_color = (255, 0, 0)

        self.map = map

        self.done = False

    def show(self):
        map = self.map

        pygame.init()
        max_x = max([p.x for p in map.points])
        max_y = max([p.y for p in map.points])
        w = max_x * self.zoom + self.borders['left'] + self.borders['right']
        h = max_y * self.zoom + self.borders['top'] + self.borders['bottom']

        screen = pygame.display.set_mode((w, h))

        points = []
        old_pos = ""
        while not self.done:
            screen.fill((0, 0, 0))
            if pygame.mouse.get_pressed() != (0, 0, 0):
                pos = pygame.mouse.get_pos()
                if pos != old_pos:
                    old_pos = pos
                    points.append(map.create_point("".format(pos), self.revert(pos)))
                    if len(points) == 2:
                        map.connect(points[0], points[1])
                        points = []
                    print(len(map.points) -1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True

            for road in map.roads:
                color = self.road_color
                color = road.color
                apos = self.convert(road.a.pos())
                bpos = self.convert(road.b.pos())
                width = self.road_width
                pygame.draw.line(screen, color, apos, bpos, width+random.randint(0, 5))

            for point in map.points:
                color = self.point_color
                pos = self.convert(point.pos())
                rad = self.point_radius
                pygame.draw.circle(screen, color, pos, rad)

                text = pygame.font.Font(self.font, self.font_size).render(point.name, True, self.font_color)
                text_rect = text.get_rect()
                x, y = self.convert(point.pos())
                text_rect.center = (x, y)
                screen.blit(text, text_rect)

            pygame.display.flip()
        pygame.quit()

    def convert(self, p):
        x, y = p
        x = round(x * self.zoom + self.borders['left'])
        y = round(y * self.zoom + self.borders['top'])
        return x, y

    def revert(self, p):
        x, y = p
        x = round((x - self.borders['left']) / self.zoom)
        y = round((y - self.borders['top']) / self.zoom)
        return x, y


m = Map()

a2 = m.create_point("a1", (400, 400))

m.view()
