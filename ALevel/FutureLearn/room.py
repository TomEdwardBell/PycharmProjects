class Room():


    def __init__(self, room_name):
        self.name = room_name
        self.desc = None
        self.linked_rooms = {}

        self.opposite_directions = {
            "north": "south",
            "south": "north",
            "east": "west",
            "west": "east",
            "above": "below",
            "below": "above"
    }



    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_desc(self, desc):
        self.desc = desc

    def get_desc(self):
        return self.desc

    def describe(self):
        print (self.desc)

    def link_room(self, room_to_link, direction, reverse):
        self.linked_rooms[direction] = room_to_link
        if reverse:
            opp_direction = self.opposite_directions[direction]
            room_to_link.link_room(self, opp_direction, False)

    def get_details(self):
        print("▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁")
        print(self.name)
        print("---------------")
        print(self.desc)
        for direction in self.linked_rooms:
            print("The " + self.linked_rooms[direction].get_name() + " is " + direction)
        print("▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔")