import io
import os
import csv

col = ["Noun", "Living_Animate_Entity", "Manufactured_Object", "Natural_Object", "Informational_Object",
              "Stative_situation", "Dynamic_situation"]

csv_file = io.open("Annotation-eval-grille-MERGE.csv", "r", encoding='utf8')
csv_reader = csv.reader(csv_file, delimiter='\t')
gold = []
result_file = io.open("test_file.txt", "w", encoding='utf8')
for c in col:
    result_file.write(c + "\t")

result_file.write("\n")
for row in csv_reader:
    if row[15] == '1':
        for i in range(7):
            if row[i] == '':
                row[i] = '0'
            result_file.write(row[i] + "\t")
        result_file.write("\n")
