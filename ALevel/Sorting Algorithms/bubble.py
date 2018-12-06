import random

def bubble_sort(l):
    # l is the list
    for run in range(len(l) -2):
        for j in range(len(l) - run - 1):
            if l[j] > l[j + 1]:
                l[j], l[j + 1] = l[j + 1], l[j]
    return(l)


while True:
    li = []
    for i in range(random.randint(2,20)):
        li.append(random.randint(0, 10))
    print(li)
    print(bubble_sort(li), "\n")