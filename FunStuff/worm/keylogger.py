import keyboard

string = ""

for char in ([chr(n) for n in range(97, 123)] + ["\b", "\n", " "]):
    keyboard.add_hotkey(char, lambda c = char: add(c))

def add(char):
    global string
    if char == "\b":
        string += "\\b"
    else:
        string += char
    print(string)
