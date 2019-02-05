import math

class CNum:
    def __init__(self, r=0, i=0):
        self.r = r
        self.i = i

    def re(self):
        return self.r

    def im(self):
        return self.i

    def modarg(self):
        s = ("["+str(self.mod())+","+str(self.arg())+"°]")
        return s

    def mod(self):
        return (self.r ** 2 + self.i ** 2) ** 0.5

    def arg(self):
        return math.degrees(math.atan(self.i / self.r))

    def format(self):
        if self.r == int(self.r):
            r = int(self.r)
        else:
            r = self.r

        if self.i == int(self.i):
            i = int(self.i)
        else:
            i = self.i

        s = ("(" + str(r) + " + " + str(i) + "i" + ")")
        return s

    def conj(self):
        re = self.r
        im = self.i
        return CNum(re, im * -1)

    def __str__(self):
        return self.format()


def CAdd(comp1, comp2):
    re = comp1.re() + comp2.re()
    im = comp1.im() + comp2.im()
    return CNum(re, im)


def CMult(comp1, comp2):
    re = comp1.re()*comp2.re() - comp1.im()*comp2.im()
    im = comp1.re()*comp2.im() + comp1.im()*comp2.re()
    return CNum(re, im)


def CSub(comp1, comp2):
    return CAdd(comp1, CMult(comp2, -1))


def CDiv(comp1, comp2):
    re1 = comp1.re()
    im1 = comp1.im()

    re2 = comp2.re()
    im2 = comp2.im()

    re = ((re1 * re2)+(im1 * im2)) / (re2**2 + im2**2)
    im = ((im1 * re2)-(re1 * im2)) / (re2**2 + im2**2)
    return CNum(re,im)


def CConj(comp):
    re = comp.re()
    im = comp.im() * -1
    return CNum(re, im)