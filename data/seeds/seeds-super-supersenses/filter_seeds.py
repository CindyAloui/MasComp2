import io
import os
from operator import itemgetter

nouns = {}

for filename in os.listdir("."):
    # if "noun." not in filename or "not_nouns" in filename:
    if "not_seeds." not in filename :
        continue
    print(filename)
    nouns[filename] = {}
    file = io.open(filename, 'r', encoding='utf8')
    for line in file:
        nouns[filename][line[:-1]] = 0


i = 0
for corpus in os.listdir("../../frWaC/moses/"):
    i += 1
    print(i)
    for line in io.open(os.path.join("../../frWaC/moses/", corpus), 'r', encoding="utf8"):
        for word in line.split():
            word = word.split("|")
            for f in nouns:
                if len(word) > 2 and word[1] in nouns[f] and word[2] == "NOM":
                    nouns[f][word[1]] += 1

for filename in nouns:
    print(filename)
    file = io.open(filename, 'w', encoding='utf8')
    for key, value in sorted(nouns[filename].items(), key=itemgetter(1), reverse=True):
        if value < 1000:
            continue
        print(key)
        file.write(key + "\n")
