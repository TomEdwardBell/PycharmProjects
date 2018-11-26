class Queue():
    def __init__(self, qlength):
        self.head = -1
        self.tail = -1
        self.max_size = qlength
        self.queue = []
        for item in range(self.max_size):
            self.queue.append(None)
            self.queue[item] = None

    def enqueue(self, item):
        if self.isFull():
            return False
        else:
            self.queue[self.tail + 1] = item
            self.tail += 1

    def deque(self):
        if self.isEmpty():
            return False
        else:
            self.head = self.head + 1
            temp = self.queue[self.head]
            return temp

    def isEmpty(self):
        if self.head == 0:
            return True
        else:
            return False

    def isFull(self):
        print("h:", self.head, "t:", self.max_size)
        if self.head - self.tail == 1:
            return True
        else:
            return False

p = Queue(4)
while True:
    print("Queue: " + str(p.queue))
    enorde = input("Enqueue or Dequeue: ")
    if enorde in ["en", "enqueue"]:
        p.enqueue(input("What would you like to add to the queue: "))
    elif enorde in ["de", "dequeue"]:
        print(p.deque())
