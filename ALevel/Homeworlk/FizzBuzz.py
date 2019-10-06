howfar = int(input("How far to count? "))
while howfar < 1:
    howfar = int(input("Not a valid number, please try again: "))
for loop in range(1, howfar + 1):
    if loop % 3 == 0 and loop % 5 == 0:
        print("Fizzbuzz")
    elif loop % 3 == 0:
        print("Fizz")
    elif loop % 5 == 0:
        print("Buzz")
    else:
        print(loop)
