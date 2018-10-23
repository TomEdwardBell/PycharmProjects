class Player():
    def __init__(self):
        self.health = 0
        self.max_health = 100
        self.name = None

    def get_hit(self):
        print("[" + self.name + ": " + "\" Ouch! I got hit\"")
        print("{ Health: "+str(self.health)+" / "+str(self.max_health)+"}")


class Mob():
    def __init__(self):
        self.name = None
        self.type = None

    def say(self, line):
        print("[" + self.name + ": " + "\"" + line + "\"]")


class Animal(Mob):
    def __init__(self):
        super(Animal, self).__init__()
        self.alive = True
        self.type = "Animal"
        self.health = None

    def get_hit(self):
        self.say("OWWW")


    def die(self):
        self.alive = False


class Fight():
    def __init__(self, player, opponent):
        print("{ You have entered a fight with " + opponent + "}")
bob = Animal()
bob.name = "Johnny"
bob.say("LMAOOOO")