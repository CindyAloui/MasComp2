import io
import os
from random import shuffle

seeds_nouns = set()

def update(file) :
    for line in file:
        seeds_nouns.add(line[:-1])


result = io.open("data/nouns_lists/nouns_to_annot.txt", "w", encoding="utf8")
for filename in os.listdir("data/seeds/seeds-super-supersenses/"):
    if "seeds." in filename and "not_" not in filename and ".py" not in filename:
        print(filename)
        file_seed1 = io.open("data/seeds/seeds-super-supersenses/" + filename, "r", encoding="utf8")
        file_seed2 = io.open("data/seeds/seeds-super-supersenses/" + "not_" + filename, "r", encoding="utf8")
        update(file_seed1)
        update(file_seed2)

nouns_file = io.open("data/nouns_lists/10000-nouns.txt", "r", encoding="utf8")
nouns = []
i = 0
for line in nouns_file:
    if i == 5000:
        break
    line = line.split("\t")
    if line[0] not in seeds_nouns:
        nouns.append(line[0])
    i += 1

shuffle(nouns)

for i in range(400):
    result.write(nouns[i] + "\n")

