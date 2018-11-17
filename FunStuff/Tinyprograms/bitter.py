import random

while True:
    r = random.randint(0,(127))
    print(r, r.to_bytes(2,"little").decode())