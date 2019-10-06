class P:
    def __init__(self,x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def eq_form(self):
        # In the form Ax + By = C
        A = self.b.y - self.a.y
        B = self.a.x - self.b.x
        C = A*self.a.x + B*self.a.y
        return A, B, C




def intersect(l1, l2):
    # Taken from
    # www.topcoder.com/community/competitive-programming
    # /tutorials/geometry-concepts-line-intersection-and-its-applications/

    A1, B1, C1 = l1.eq_form()
    A2, B2, C2 = l2.eq_form()

    i = P(0, 0) # i = point of intersection

    det = A1*B2 - A2*B1
    if det == 0:
        return False
    else:
        i.x = (B2*C1 - B1*C2)/det
        i.y = (A1*C2 - A2*C1)/det

    return i.x, i.y


l1 = Line(P(0, 0), P(100, 200))
l2 = Line(P(100, 0), P(0, 100))

print(intersect(l1, l2))