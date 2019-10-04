import io
import os
from random import shuffle


def write_nouns(f, nouns):
    for n in nouns:
        f.write(n + "\n")


train_size_percent = 80.0

# file_seed1 = io.open("animacy/200-ANIM.txt", "r", encoding="utf8")
# file_seed2 = io.open("animacy/200-INANIM.txt", "r", encoding="utf8")
#
# file_train_seed1 = io.open("animacy/200-ANIM-train.txt", "w", encoding="utf8")
# file_train_seed2 = io.open("animacy/200-INANIM-train.txt", "w", encoding="utf8")
#
# file_dev_seed1 = io.open("animacy/200-ANIM-dev.txt", "w", encoding="utf8")
# file_dev_seed2 = io.open("animacy/200-INANIM-dev.txt", "w", encoding="utf8")

for file in os.listdir("supersenses")

seed1 = []
seed2 = []

for line in file_seed1:
    seed1.append(line[:-1])
for line in file_seed2:
    seed2.append(line[:-1])

shuffle(seed1)
shuffle(seed2)

train_size_seed1 = int(len(seed1) * train_size_percent / 100)
train_size_seed2 = int(len(seed2) * train_size_percent / 100)

train_seed1 = seed1[:train_size_seed1]
train_seed2 = seed2[:train_size_seed2]

dev_seed1 = seed1[train_size_seed1:]
dev_seed2 = seed2[train_size_seed2:]

write_nouns(file_dev_seed1, dev_seed1)
write_nouns(file_dev_seed2, dev_seed2)
write_nouns(file_train_seed1, train_seed1)
write_nouns(file_train_seed2, train_seed2)

