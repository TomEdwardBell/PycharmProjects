dec = int(input("Decimal Number: "))
binary = ""
quotient = dec
remainder = 0
while quotient != 0:
    remainder = quotient % 2
    binary += str(remainder)
    quotient = quotient // 2

print("Wrong order: " + binary)
print("Right order: " + binary[::-1])
