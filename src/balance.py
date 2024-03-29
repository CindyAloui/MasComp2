import io
import os
import sys
from random import shuffle

SEED1 = 0
SEED2 = 1
max_occ = 1000

def get_set_from_file(filename):
    file = io.open(filename, "r", encoding="utf8")
    list = set()
    for line in file:
        list.add(line[:-1])
    return list


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + "<seed1File> <seed2File> <inputDir> <outputDir>")
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print_usage_and_exit()
    in_dir = sys.argv[3]
    out_dir = sys.argv[4]
    seed1_train = get_set_from_file(sys.argv[1] + "-train.txt")
    seed1_dev = get_set_from_file(sys.argv[1] + "-dev.txt")
    seed2_train = get_set_from_file(sys.argv[2] + "-train.txt")
    seed2_dev = get_set_from_file(sys.argv[2] + "-dev.txt")

    j = 0
    for filename in os.listdir(in_dir):
        j += 1
        print(j)
        if filename == "dev.mcf":
            print("ok")
            seed1 = seed1_dev
            seed2 = seed2_dev
        else:
            seed1 = seed1_train
            seed2 = seed2_train

        occ = {}
        for n in seed1:
            occ[n] = 0
        for n in seed2:
            occ[n] = 0
        file = io.open(os.path.join(in_dir, filename), "r", encoding="utf8")
        result_file = io.open(os.path.join(out_dir, filename), "w", encoding="utf8")
        id = []
        id_kept = set()
        seed1_sentence = {}
        seed2_sentence = {}
        current_id = None
        current_s1 = 0
        current_s2 = 0
        current_occ = {}
        for n in seed1:
            current_occ[n] = 0
        for n in seed2:
            current_occ[n] = 0
        nb_s1 = 0
        nb_s2 = 0
        flag = True
        for line in file:
            if "#id_" in line:
                current_id = int(line[4:-1])
            line = line.split("\t")
            if len(line) != 7:
                continue
            if line[1] == "NOUN" and line[3] in seed1:
                if occ[line[3]] >= max_occ:
                    flag = False
                current_occ[line[3]] += 1
                current_s1 += 1
            if line[1] == "NOUN" and line[3] in seed2:
                if occ[line[3]] >= max_occ:
                    flag = False
                current_occ[line[3]] += 1
                current_s2 += 1
            if line[6] == "1\n":
                if (current_s1 != 0 or current_s2 != 0) and flag is True:
                    id.append(current_id)
                    new_sentence = {SEED1: current_s1, SEED2: current_s2}
                    if current_s1 > current_s2:
                        seed1_sentence[current_id] = new_sentence
                    else:
                        seed2_sentence[current_id] = new_sentence
                    for n in seed1:
                        occ[n] += current_occ[n]
                    for n in seed2:
                        occ[n] += current_occ[n]
                    nb_s1 += current_s1
                    nb_s2 += current_s2

                for n in seed1:
                    current_occ[n] = 0
                for n in seed2:
                    current_occ[n] = 0
                current_s1 = 0
                current_s2 = 0
                flag = True
        if not id:
            print("No id for file " + filename + " .")
            continue

        if nb_s1 > nb_s2:
            current_s1 = 0
            current_s2 = 0
            for sent in seed2_sentence:
                id_kept.add(sent)
                id.remove(sent)
                current_s1 += seed2_sentence[sent][SEED1]
                current_s2 += seed2_sentence[sent][SEED2]
            shuffle(id)
            for i in id:
                id_kept.add(i)
                current_s1 += seed1_sentence[i][SEED1]
                current_s2 += seed1_sentence[i][SEED2]
                if current_s2 <= current_s1:
                    break
        else:
            current_s1 = 0
            current_s2 = 0
            for sent in seed1_sentence:
                id_kept.add(sent)
                id.remove(sent)
                current_s1 += seed1_sentence[sent][SEED1]
                current_s2 += seed1_sentence[sent][SEED2]
            shuffle(id)
            for i in id:
                id_kept.add(i)
                current_s1 += seed2_sentence[i][SEED1]
                current_s2 += seed2_sentence[i][SEED2]
                if current_s1 <= current_s2:
                    break

        # print("\n")
        # print(current_s1)
        # print(current_s2)
        # print(nb_s1)
        # print(nb_s2)
        flag = False
        file = io.open(os.path.join(in_dir, filename), "r", encoding="utf8")
        for line in file:
            if "#id_" in line:
                if int(line[4:-1]) in id_kept:
                    flag = True
                    id_kept.remove(int(line[4:-1]))
                else:
                    flag = False
            if flag is True:
                result_file.write(line)
