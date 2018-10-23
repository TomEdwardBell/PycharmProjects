seed = 1212121212

sseed = str(seed)
sseed = sseed[::-1] # Reverses Seed
# Changing each individual digit of the seed
# By adding the first digit of the seed to each digit but only taking the last digit of the sum of them
key = int(sseed[0])
newseed = ""
for c in range(len(sseed)):
    newc = int(sseed[c])
    newc += key*c
    newc = str(newc)[-1]
    newseed = newseed + newc


print (seed,"-->",newseed)
