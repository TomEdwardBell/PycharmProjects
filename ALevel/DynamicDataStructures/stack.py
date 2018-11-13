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
        print(self.head, self.max_size)
        if self.head == self.max_size:
            return True
        else:
            return False

p = Stack(3)
while True:
    print("Stack: " + str(p.stack))
    pushorpop = input("push or pop: ")
    if pushorpop == "push":
        p.push(input("What would you like to push: "))
    if pushorpop == "pop":
        print(p.pop())

