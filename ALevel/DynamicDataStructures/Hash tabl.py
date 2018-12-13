import time
from tabulate import tabulate


class HashRecord:
    def __init__(self, key, dat, adr):
        self.key = key
        self.data = dat
        self.adr = adr
        self.pointer = -1

    def display(self):
        string = self.key + ": " + self.data
        return (string)

    def get_data(self):
        return(self.data)

    def get_key(self):
        return (self.key)

    def get_pointer(self):
        return (self.pointer)

    def get_record(self):
        return(self.key, self.data)


class HashTable(list):
    def __init__(self, maxlen):
        super(HashTable, self).__init__()
        self.maxlen = maxlen
        self.create_table()

    def create_table(self):
        for i in range(self.maxlen):
            self.append(HashRecord("-1", "-1", -1))

    def get_hash(self, key):
        sum = 0
        for k in key:
            sum += ord(k) ** 2
        hsh = sum % self.maxlen
        return hsh
    
    def add_item(self, key, data):
        hsh = self.get_hash(key)
        while self[hsh].get_record() != ("-1", "-1"):
            oldhsh = hsh
            pointer = self[hsh].get_pointer()
            if pointer == -1:
                hsh = (hsh + 1) % self.maxlen
            else:
                hsh = pointer
            self[oldhsh].pointer = hsh
        print(key, " going to ", hsh, )
        time.sleep(0.01)
        self[hsh] = HashRecord(key, data, hsh)

    def display(self):
        for item in self:
            print(item.display())
            
    def give(self, key):
        hsh = self.get_hash(key)
        if self[hsh].get_data() == key:
            return self[hsh].get_data()
        else:
            while self[hsh].get_key() != key:
                print("Current:", hsh, " Key:", self[hsh].get_key(), " Going to:", self[hsh].get_pointer(), " AKA:", self[self[hsh].get_pointer()].get_key(), sep="")
                hsh = self[hsh].get_pointer()
            return self[hsh].get_data()

states = '''
Alabama - AL
Alaska - AK
Arizona - AZ
Arkansas - AR
California - CA
Colorado - CO
Connecticut - CT
Delaware - DE
Florida - FL
Georgia - GA
Hawaii - HI
Idaho - ID
Illinois - IL
Indiana - IN
Iowa - IA
Kansas - KS
Kentucky - KY
Louisiana - LA
Maine - ME
Maryland - MD
Massachusetts - MA
Michigan - MI
Minnesota - MN
Mississippi - MS
Missouri - MO
Montana - MT
Nebraska - NE
Nevada - NV
New Hampshire - NH
New Jersey - NJ
New Mexico - NM
New York - NY
North Carolina - NC
North Dakota - ND
Ohio - OH
Oklahoma - OK
Oregon - OR
Pennsylvania - PA
Rhode Island - RI
South Carolina - SC
South Dakota - SD
Tennessee - TN
Texas - TX
Utah - UT
Vermont - VT
Virginia - VA
Washington - WA
West Virginia - WV
Wisconsin - WI
Wyoming - WY
'''

h = HashTable(51)
states = states.splitlines(False)
newstates = []
for state in states:
    if state != '':
        newstate = []
        newstate = state.split(" - ")
        h.add_item(newstate[1], newstate[0])
        newstates.append(newstate)
h.display()

while True:
    pp = input("Initials: ")
    print("State: " + h.give(pp))
