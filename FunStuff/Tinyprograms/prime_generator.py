current_number = 1
primes = [2, 3]

if False:
    while True:
        current_number += 1
        isprime = True
        prime_test = 0
        sqr = int(current_number**0.5)
        while primes[prime_test] < sqr:
            prime_test += 1
            if current_number % primes[prime_test] == 0:
                isprime = False
        if isprime:
            primes.append(current_number)
            print(len(primes),":",current_number)#

current_number = 1
if True:
    #for current_number in range(3, 10000, 1)\
    while len(primes) < 20000:
        current_number += 2
        isprime = True
        prime_test = 0
        sqr = int(current_number**0.5)

        for prime in primes:
            if prime > sqr:
                break
            if not isprime:
                break
            if current_number % prime == 0:
                isprime = False
        if isprime:
            primes.append(current_number)

print (primes)
print(len(primes))