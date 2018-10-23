import random

def gen_seed(base, length):
    if base == 10:
        return gen_seed_10(length)  # For generating purely numerical seeds

    if base == 16:
        return gen_seed_16(length)  # For generating seeds where each character is 16 bits

    if base == 26:
        return gen_seed_26(length)  # For generating purely alphabetical seeds

    if base == 32:
        return gen_seed_32(length)  # For generating seeds where each character is 32 bits

    if base == 64:
        return gen_seed_64(length)  # For generating seeds where each character is 64 bits

def gen_seed_10 (length):
    newseed = ""
    for u in range (length):
        digit = str(random.randint (0,9))
        newseed = newseed + digit
    return newseed

def gen_seed_16 (length):
    newseed = ""
    for u in range (length):
        digit = random.randint(0, 15)
        charachter = ""
        if digit < 10: #digit between 0 and 9 gets 0-->9
            charachter = str(digit)
        elif digit > 9: #digit between 26 and 51 gets 0-->6
            charachter = chr((digit -10 + 97))
        newseed = newseed + charachter
    return newseed


def gen_seed_26 (length):
    newseed = ""
    for u in range (length):
        digit = random.randint(0, 25)
        charachter = chr((digit + 65))
        newseed = newseed + charachter
    return newseed


def gen_seed_32 (length):
    newseed = ""
    for u in range (length):
        digit = random.randint(0, 31)
        charachter = ""
        if digit < 26:  # digit between 0 and 25 gets A-->Z
            charachter = chr((digit -  0 + 65))
        elif digit > 25:  # digit between 26 and 51 gets 0-->6
            charachter = chr((digit - 26 + 48))
        newseed = newseed + charachter
    return newseed

def gen_seed_64 (length):
    newseed = ""
    for u in range (length):
        digit = random.randint(0, 63)
        charachter = ""
        if digit < 26:  # digit between 0 and 25 gets A-->Z
            charachter = chr((digit -  0 + 65))
        elif digit > 25 and digit < 52:  # digit between 26 and 51 gets a-->z
            charachter = chr((digit - 26 + 97))
        elif digit > 51 and digit < 62:  # digits between 52 and 62 gets 0-->9
            charachter = chr((digit - 52 + 48))
        elif digit == 62:  # digit 63 is -
            charachter = "+"
        elif digit == 63:  # digit 64 is _
            charachter = "/"
        newseed = newseed + charachter
    return newseed
