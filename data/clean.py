import io
import os

def get_set_from_file(filename):
    file = io.open(filename, "r", encoding="utf8")
    list = set()
    for line in file:
        line = line.split("\t")
        list.add(line[0])
    return list


nouns = get_set_from_file("nouns_lists/10000-nouns.txt")
directory = "frWaC/10000-nouns-mcf"
if not os.path.exists(directory):
    os.makedirs(directory)

i = 0

for corpus in os.listdir("frWaC/mcf"):
    i += 1
    print(i)
    result_file = io.open(os.path.join(directory, corpus), "w", encoding='utf8')
    file = io.open(os.path.join("frWaC/mcf", corpus), "r", encoding="utf8")
    id_kept = set()
    nouns_sentence = {}
    current_id = None
    flag = False
    for line in file:
        if "#id_" in line:
            current_id = int(line[4:-1])
        line = line.split("\t")
        if len(line) != 7:
            continue
        if line[1] == "NOUN" and line[3] in nouns:
            flag = True
        if line[6] == "1\n":
            if flag is True:
                id_kept.add(current_id)
            flag = False

    file = io.open(os.path.join("frWaC/mcf", corpus), "r", encoding="utf8")

    for line in file:
        if "#id_" in line:
            if int(line[4:-1]) in id_kept:
                flag = True
            else:
                flag = False
        if flag is True:
            result_file.write(line)
