class Stack():
    def __init__(self, qlength):
        self.head = 0
        self.max_size = qlength
        self.stack = []
        for item in range(self.max_size):
            self.stack.append(None)
            self.stack[item] = None

    def push(self, item):
        if self.isFull():
            return False
        else:
            self.stack[self.head] = item
            self.head += 1

    def pop(self):
        if self.isEmpty():
            return False
        else:
            self.head = self.head - 1
            temp = self.stack[self.head]
            return temp

    def isEmpty(self):
        if self.head == 0:
            return True
        else:
            return False

    def isFull(self):
        if self.head == self.max_size:
            return True
        else:
            return False

    def display(self):
        for item in range(self.max_size):
            print(str(item).zfill(2),": ",self.stack[item], sep="")

p = Stack(60)
while True:
    p.display()
    pushorpop = input("push or pop: ")
    if pushorpop == "push":
        p.push(input("What would you like to push: "))
    if pushorpop == "pop":
        print(p.pop())

