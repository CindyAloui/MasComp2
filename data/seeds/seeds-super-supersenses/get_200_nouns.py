import io
import os
from random import shuffle

supersenses = {}
for filename in os.listdir("."):
    if ".py" not in filename:
        file = io.open(filename, "r", encoding="utf8")
        supersenses[filename] = []
        for line in file:
            if line.strip() == '':
                continue
            supersenses[filename].append(line.strip())

for g1 in supersenses:
    file = io.open("not_" + g1, "w", encoding="utf8")
    l = []
    for g2 in supersenses:
        if g1 == g2:
            continue
        l.extend(supersenses[g2])
    shuffle(l)
    for i in range(200):
        file.write(l[i] + "\n")

# for filename in os.listdir("."):
#     if "not_" in filename:
#         l = []
#         file = io.open(filename, "r", encoding="utf8")
#         for line in file:
#             l.append(line)
#         shuffle(l)
#         print(filename)
#         file = io.open(filename, "w", encoding="utf8")
#         for i in range(200):
#             file.write(l[i])

# file = io.open("all_nouns_with_supersenses.txt", "r", encoding="utf8")
# words = {}
# for line in file:
#     line = line.split()
#     if len(line[0]) < 3:
#         continue
#     words[line[0]] = line[1:]
# for supersense in os.listdir("."):
#     if "noun." in supersense and "not_noun" not in supersense:
#         result = io.open("not_" + supersense, "w", encoding="utf8")
#         l = []
#         for word in words:
#             if supersense not in words[word]:
#                 l.append(word)
#         shuffle(l)
#         for i in range(200):
#             result.write(l[i] + "\n")
