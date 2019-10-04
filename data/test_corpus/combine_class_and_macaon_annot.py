import io
import os
import sys

dir_class = "countability/class_annot"
dir_macaon = "countability/treated"
new_dir = "countability/test"
class_1 = "C"
class_2 = "M"

for filename in os.listdir(dir_class):
    file_class = io.open(os.path.join(dir_class, filename), 'r', encoding='utf8')
    file_macaon = io.open(os.path.join(dir_macaon, filename) + ".mcf", 'r', encoding='utf8')
    new_file = io.open(os.path.join(new_dir, filename), 'w', encoding='utf8')
    while True:
        line_class = file_class.readline()
        if line_class == '':
            break
        if not line_class.strip():
            continue
        sentence = line_class.split()
        annot = sentence[0]
        if annot != class_1 and annot != class_2:
            continue
        sentence.remove(sentence[0])
        sentence.remove("[[")
        sentence.remove("]]")


        new_file.write("#" + annot + "\n")
        buffer_sentence = []
        buffer = []
        while(True):
            line_macaon = file_macaon.readline()
            if line_macaon == '':
                break
            if not line_macaon.strip():
                continue
            buffer.append(line_macaon)
            line_macaon = line_macaon.split("\t")
            buffer_sentence.append(line_macaon[0])
            if buffer_sentence[-len(sentence):] == sentence:
                new_buffer = buffer[-len(sentence):]
                for line in new_buffer:
                    new_file.write(line)
                break