raw_first = open("first_names_raw.csv", "r")
firsts_file = open("first_names.txt","a")
for line in raw_first:
    firsts_file.write(line.split(',')[1][1:-1] + "\n")
    pass

raw_lasts = open("last_names_raw.txt", "r")
lasts_file = open("last_names.txt","a")
for line in raw_lasts:
    lasts_file.write(line.split('\t')[1] + "\n")
