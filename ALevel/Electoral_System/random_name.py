import random

firsts_f = open('first_names.txt', 'r')
firsts = firsts_f.readlines()
firsts_f.close()

lasts_f = open('last_names.txt', 'r')
lasts = lasts_f.readlines()
lasts_f.close()

def full():
    return first() + ' ' + last()

def first():
    global firsts
    name = random.choice(firsts)[:-1]
    return name


def last():
    global lasts
    name = random.choice(lasts)[:-1]
    return name


def party():
    name = ''
    for i in range(random.randint(2, 4)):
        name += chr(random.randint(65, 85))
    if prob(0.5): name += 'P'
    return name


def region():
    name = ''
    locations = [' North ', ' South', ' East', ' West', ' NE', ' NW', ' SE', ' SW', ' Central', ' Upper', ' Lower',
                 ' Park', ' Valley', ' Green']

    starts = ['Alder', 'Ash', 'Ban', 'Barn', 'Bath', 'Berken', 'Birris', 'Brent', 'Brom',  # As Bs
              'Charish', 'Cam', 'Car', 'Cal', 'Chel', 'Cope', 'Craw', 'Croy', 'Dews', 'Dud', 'Dor',  # Cs Ds
              'Eal', 'Eas', 'Edd', 'Ere', 'Exe', 'Fel', 'Fal', 'Fil', 'Folke',  # Es Fs
              'Gains', 'Gar', 'Grim', 'Guil', 'Green', 'Harr', 'Hack', 'Halt', 'Horn', 'Hen', 'Hex',  # Gs Hs
              'Ip', 'Ken', 'Kings', 'Lei', 'Lew', 'Lewes', 'Ley', 'Lin', 'Lut', 'Lan',  # Is Js Ks Ls
              'Mal', 'Mel', 'Man', 'Mid', 'Mil', 'New', 'Nun', 'Ox', 'Orp',  # Ms Ns Os
              'Pen', 'Ply', 'Port', 'Ports', 'Pres', 'Put', 'Punt', 'Pud', 'Read', 'Redd', 'Roch', 'Rug',  # Ps Qs Rs
              'Sail', 'Scar', 'Sur', 'Strat', 'Tam', 'Tat', 'Tel', 'Thor', 'Tun', 'Ux', 'Ul',  # Ss Ts Us
              'Vaux', 'Vex', 'Wal', 'Wans', 'War', 'Wasp', 'Wat', 'Well', 'Win'  # Vs Ws Xs Ys Zs
              ]

    suffixes = ['bridge', 'bury', 'by', 'cester', 'chester', 'cliffe', 'don', 'dif','erton', 'field', 'ford', 'ferry',
                'ham','ick', 'ing', 'ington', 'itch', 'mouth', 'ney', 'pool', 'sea', 
                'shire', 'sley', 'ter', 'ton', 'wood', 'worth']

    if prob(0.7): # One long location name

        name = random.choice(starts) + random.choice(suffixes)
        if prob(0.5):
            name += random.choice(locations)

    else: # Two short location names
        name = random.choice(starts) + random.choice(suffixes) + ' and ' + random.choice(starts) + random.choice(suffixes)

    return name

def nation():
    prefixes = ['The Republic of ', 'Republic of ', 'The Kingdom of ', 'The Empire of ', 'The ']

    middles = [
        'Northern ', 'North ', 'Eastern ', 'East ', 'Southern ', 'South ', 'Western ', 'West ', 'Central ',
               ]

    ends = ['astan', 'land', 'asia', 'ania', 'lands', 'akia', 'avia', 'oslavia']

    name = ''

    return name

def syllable():
    begins = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'y', 'z',
             'bl', 'br',
             'cl', 'cr', 'ch', 'chr',
             'fl', 'fr',
             'gl', 'gr',
             'jh',
             'kl', 'kr',
             'ps', 'pr', 'pl', 'ph',
             'sc', 'sk', 'sch', 'sg', 'sn',
             'th', 'tr',
             ]

    vowels = ['a', 'e', 'i', 'o', 'u']

    dipthongs = ['ai', 'au',
                'ei', 'eu',
                'ia', 'io', 'iu',
                'oi', 'ou',
                'ua',
                 'oo', 'ee']

    ends = ['b', 'c', 'd', 'f', 'g', 'j', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'y', 'z',
            'bs',
            'ch', 'ck', 'cks',
            'ds',
            'ls', 'ld' 'll',
            'ms', 'mn', 'mp',
            'ns', 'nt',
            'ps', 'ph',
            'rs', 'rt',
            'st', 'sd', 'sk', 'sp'
            'ts', 'th']

    s = ''
    s+=random.choice(begins)
    if prob(1/3): s+=random.choice(vowels)
    else: s+=random.choice(dipthongs)
    s+= random.choice(ends)

    return s

def prob(p):
    return random.random() < p