

def word_count(filename):
    text = get_file(filename)
    text = remove_unwanted(text)
    words = text.split(" ")
    words = remove_spaces(words)

    count = {}
    count = count_up(words)

    count = sortdict(count)

    printout(count)


def get_file(filename):
    file = open(filename, "r")
    text = file.read()
    return(text)


def remove_unwanted(text):
    newtext = ""
    good_chars = list("abcdefghijklmnopqrstuvwxyz-' ")
    text = text.lower()
    for char in text:
        if char in good_chars:
            newtext = newtext + char
        else:
            newtext = newtext + " "
    return(newtext)


def remove_spaces(words):
    new_words = []
    for word in words:
        if word != " " and word != "":
            new_words.append(word)
    return (new_words)


def count_up(words):
    counter = {}
    for word in words:
        if word in counter:
            counter[word] +=  1
        else:
            counter[word] = 1
    return counter


def printout(dic):
    for word in dic:
        print(word+": "+str(dic[word]))


def sortdict(dic):

    highest = 0
    for item in dic:
        if dic[item] > highest:
            highest = dic[item]

    newdic = {}

    for count in range(highest, 0, -1):
        for word in dic:
            if dic[word] == count:
                newdic[word] = count


    return newdic

word_count("text.txt")