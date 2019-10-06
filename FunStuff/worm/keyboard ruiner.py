import keyboard
import random


def ceaser(key):
    for n in range(97, 123):
        new = (n-97 + key) % (123 - 97) + 97
        keyboard.add_hotkey(chr(n), lambda c=new: keyboard.write("\b" + chr(c)))

def replace(word):
    word = "\b" + word + " "
    for n in range(ord("a"), ord("z")):
        keyboard.add_hotkey(chr(n), lambda c=word: keyboard.write(c))

def uwu():
    def random_face():
        faces = "ᵕ꒳ᵕ ᵘʷᵘ ⒰⒲⒰ 🇺🇼🇺  🆄🆆🆄  🅄🅆🅄 પฝપ  ሁሠሁ  ⓤⓦⓤ  🅤🅦🅤  ｕｗｕ  ＵｗＵ  𝖴𝗐𝖴 𝗨𝘄𝗨 ᵾwᵾ 𝕌𝕨𝕌 𝓤𝔀𝓤".split()
        keyboard.write("\b{} ".format(random.choice(faces)))

    keyboard.add_hotkey("r", lambda: keyboard.write("\bw"))
    keyboard.add_hotkey(".", lambda: random_face())

uwu()