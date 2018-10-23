seed = 1947374730


class Room:
    def __init__(self):
        self.name = None
        self.desc = None
        self.type = None
        self.enterable = False


class NoRoom(Room):
    def __init__(self):
        super(NoRoom, self).__init__()
        self.enterable = False
        self.type = " "
        self.name = "no room"
        self.desc = "Not a room"

class DungeonMap:
    def __init__(self):
        self.map = {}
        self.generate_map()

    def generate_map(self):
        self.gen_empty_map()
        self.place_rooms()

    def gen_empty_map(self):
        map_w = 5  # Make map_w and map_h ODD POSITIVE INTEGERS
        map_h = 5
        center_w = int(map_w / 2)
        center_h = int(map_h / 2)
        for wrange in range(map_w):
            for hrange in range(map_h):
                w = int(wrange - center_w)
                h = int(hrange - center_h)
                self.map[w, h] = NoRoom

    def place_rooms(self):
        self.map[0, 0].name = "spawn"
        self.map[0, 0].type = "s"

        pathcount = (int(str(seed)[0]) % 3) + 1
        for path in range(pathcount):
            carryforward = True
            current_coords = [0, 0]
            while carryforward:
                x_dir_or_y_dir = int(str(seed)[1]) % 2
                dir = [0,0]
                movement = int(str(seed)[2]) % 2 - 1
                dir[x_dir_or_y_dir] = movement
                print(dir)

    def show_map(self):
        pass



def main():
    dungeon = DungeonMap()

if __name__ == '__main__':
    main()
