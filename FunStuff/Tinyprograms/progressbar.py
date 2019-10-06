import time
import random

length = 40
total = 10
fill_char = "█"
empty_char = "-"


def returnbar(length, full):
    global fill_char
    global empty_char
    filled =  int(length * full)
    empty = length - filled
    percentage = str(full*100)[2:4] + "%"
    return("|{}{}|{}".format(fill_char*filled, empty_char*empty, percentage))


def loadbar():
    pass

while True:
    print(returnbar(40, random.random()))