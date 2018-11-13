import time

def calc_factorial(number):
    if number == 0:
        return 1
    else:
        factorial = number * calc_factorial(number - 1)
    return factorial

def for_factorial(number):
    fact = 1
    for i in range(number):
        fact = fact * (i+1)
    return fact

fstart = time.time()
for_factorial(90)
fend = time.time()
print (fend - fstart)


rstart = time.time()
calc_factorial(90)
rend = time.time()
print(rend - rstart)




