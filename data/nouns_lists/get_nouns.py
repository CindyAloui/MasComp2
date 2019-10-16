import io
import os
import csv
from operator import itemgetter


# def is_ok(str):
#     for c in str:
#         if not c.isalpha() and c != "'" and c != "-":
#             return False
#     return True

lexique3 = io.open("Lexique3.tsv", "r", encoding='utf8')

reader = csv.reader(lexique3, delimiter='\t')
occ = {}

for row in reader:
    if row[3] == "NOM" and len(row[2]) > 1:
        occ[row[2]] = 0


total = 0.0
i = 0

for corpus in os.listdir("../frWaC/mcf/"):
    i += 1
    print(i)
    for line in io.open(os.path.join("../frWaC/mcf/", corpus), 'r', encoding="utf8"):
        line = line.split()
        if len(line) != 7:
            continue
        if line[1] == "NOUN":
            total += 1
            s = line[3].lower()
            if s not in occ:
                continue
            occ[s] += 1

result = io.open("10000-nouns.txt", "w", encoding='utf8')

sorted_occ = sorted(occ.items(), key=itemgetter(1), reverse=True)
for i in range(1, 11):
    sum = 0.0
    lowest_number_of_occ = 0
    r = i*1000
    print("\nStats pour les " + str(r) + " premiers noms")
    for j in range(r):
        if r == 10000:
            result.write(sorted_occ[j][0] + "\t" + str(sorted_occ[j][1]) + "\n")
        sum += sorted_occ[j][1]
        lowest_number_of_occ = sorted_occ[j][1]
    print("Couverture : " + str((sum/total) * 100) + "%")
    print("Nombre d'occ min : " + str(lowest_number_of_occ))