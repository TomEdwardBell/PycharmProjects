import random

firsts_f = open("first_names.txt", "r")
firsts = firsts_f.readlines()
firsts_f.close()

lasts_f = open("last_names.txt", "r")
lasts = lasts_f.readlines()
lasts_f.close()

def full():
    return first() + " " + last()

def first():
    global firsts
    name = random.choice(firsts)[:-1]
    return name


def last():
    global lasts
    name = random.choice(lasts)[:-1]
    return name


def party():
    name = ""
    for i in range(random.randint(2, 4)):
        name += chr(random.randint(65, 85))
    if random.randint(0, 1): name += "P"
    return name


def region():
    name = ""
    locations = [" North ", " South", " East", " West", " NE", " NW", " SE", " SW", " Central", " Upper", " Lower",
                 " Park", " Valley", " Green"]

    starts = ["Alder", "Ash", "Ban", "Barn", "Bath", "Berken", "Birris", "Brent", "Brom",  # As Bs
              "Charish", "Cam", "Cal", "Chel", "Cope", "Craw", "Croy", "Dews", "Dud", "Dor",  # Cs Ds
              "Eal", "Eas", "Edd", "Ere", "Exe", "Fel", "Fal", "Fil", "Folke",  # Es Fs
              "Gains", "Gar", "Grim", "Guil", "Green", "Harr", "Hack", "Halt", "Horn", "Hen", "Hex",  # Gs Hs
              "Ip", "Ken", "Kings", "Lei", "Lew", "Lewes", "Ley", "Lin", "Lut", "Lan",  # Is Js Ks Ls
              "Mal", "Mel", "Man", "Mid", "Mil", "New", "Nun", "Ox", "Orp",  # Ms Ns Os
              "Pen", "Ply", "Port", "Ports", "Pres", "Put", "Punt", "Pud", "Read", "Redd", "Roch", "Rug",  # Ps Qs Rs
              "Sail", "Scar", "Sur", "Strat", "Tam", "Tat", "Tel", "Thor", "Tun", "Ux", "Ul",  # Ss Ts Us
              "Vaux", "Vex", "Wal", "Wans", "War", "Wat", "Well", "Win"  # Vs Ws Xs Ys Zs
              ]

    suffixes = ['bridge', 'bury', 'by', 'cester', 'chester', 'cliffe', 'don', 'erton', 'field', 'ford', 'ham',
                'ick', 'ing', 'ington', 'itch', 'mouth', 'ney', 'pool', 'sea', 'shire', 'sley', 'ter', 'ton',
                'wood', 'worth']

    name = random.choice(starts) + random.choice(suffixes)
    if random.randint(0, 1) == 0:
        name += random.choice(locations)

    return name

def nation():
    prefixes = ["The Republic of ", "Republic of ", "The Kingdom of ", "The Empire of ", "The "]

    middles = [
        "Northern ", "North ", "Eastern ", "East ", "Southern ", "South ", "Western ", "West ", "Central ",
               ]

    ends = ["astan", "land", "asia", "ania", "lands", "akia", "avia", "oslavia"]

    name = ""
    if random.randint(0, 1): name += random.choice(prefixes)
    if random.randint(0, 2): name += random.choice(middles)
    for i in range(random.randint(1, 2)):
        name += syllable()
    if random.randint(0, 1): name += random.choice(ends)

    return name

def syllable():
    begins = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "y", "z",
             "bl", "br",
             "cl", "cr", "ch", "chr",
             "fl", "fr",
             "gl", "gr",
             "jh",
             "kl", "kr",
             "ps", "pr", "pl", "ph",
             "sc", "sk", "sch", "sg", "sn",
             "th", "tr",
             ]

    vowels = ["a", "e", "i", "o", "u"]

    dipthongs = ["ai", "au",
                "ei", "eu",
                "ia", "io", "iu",
                "oi", "ou",
                "ua",
                 "oo", "ee"]

    ends = ["b", "c", "d", "f", "g", "j", "k", "l", "m", "n", "p", "r", "s", "t", "v", "w", "y", "z",
            "bs",
            "ch", "ck", "cks",
            "ds",
            "ls", "ld" "ll",
            "ms", "mn", "mp",
            "ns", "nt",
            "ps", "ph",
            "rs", "rt",
            "st", "sd", "sk", "sp"
            "ts", "th"]

    s = ""
    s+=random.choice(begins)
    if random.randint(0, 3) != 0: s+=random.choice(vowels)
    else: s+=random.choice(dipthongs)
    s+= random.choice(ends)

    return s
