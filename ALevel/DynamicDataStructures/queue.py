class Queue():
    def __init__(self, qlength):
        self.head = 0
        self.tail = 0
        self.max_size = qlength
        self.queue = []
        for item in range(self.max_size):
            self.queue.append(None)
            self.queue[item] = None

    def enque(self, item):
        if self.isFull():
            return False
        else:
            self.queue[self.head] = item
            self.head += 1

    def deque(self):
        if self.isEmpty():
            return False
        else:
            self.head = self.head - 1
            temp = self.queue[self.head]
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

p = Queue(3)
while True:
    print("Queue: " + str(p.queue))
    pushorpop = input("Enqueue or Dequeue: ")
    if pushorpop in ["en", "enqueue"]:
        p.enque(input("What would you like to add to the queue: "))
    elif pushorpop in ["de", "dequeue"]:
        print(p.deque())
