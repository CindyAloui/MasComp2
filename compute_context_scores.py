import io
import os
import sys
from keras.models import load_model
from src.classifier import get_index, get_set_from_file, get_dir_from_file
import numpy as np
from math import pow

exponent = 16
occ = {}
num = {}
denum = {}
gigasenses = {"Living_Animate_Entity", "Natural_Object", "Manufactured_Object", "Informational_Object",
              "Dynamic_situation", "Stative_situation"}

for g in gigasenses:
    print(g)
print("\n")

for g in gigasenses:
    print(g)
exit(0)
vocab_words = get_dir_from_file("data/vocabs/words")
vocab_lemmas = get_dir_from_file("data/vocabs/lemmas")
vocab_morphos = get_dir_from_file("data/vocabs/morphos")
position_size = 300
nouns_finished = set()


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + "<nounsList> <corpusDir> ")
    sys.exit(0)

def add_padding(words):
    max_len = 0
    for word in words:
        if max_len < len(word):
            max_len = len(word)
    if max_len == 0:
        max_len = 1
    for i in range(len(words)):
        for j in range(len(words[i]), max_len):
            words[i].insert(0, 0)
    for word in words:
        if len(word) != max_len:
            print("BUG")


def update(buffer, nouns, result_file):
    current_words = []
    current_lemmas = []
    current_morphos = []
    current_positions = []
    word_positions = []
    words_left = []
    lemmas_left = []
    morphos_left = []
    words_right = []
    lemmas_right = []
    morphos_right = []
    morpho = []
    n = []
    current_nouns = []
    p = -1

    for line in buffer.split("\n"):
        line = line.split("\t")
        if len(line) != 7:
            continue
        p += 1
        current_words.append(get_index(line[0], vocab_words))
        current_lemmas.append(get_index(line[3], vocab_lemmas))
        current_morphos.append(get_index(line[2], vocab_morphos))
        current_positions.append(p)
        if line[1] == "NOUN" and line[3] in nouns:
            word_positions.append(p)
            current_nouns.append(line[3])
        if line[6] == "1":
            for i in range(len(word_positions)):
                new_positions_left = []
                new_positions_right = []
                for p in current_positions:
                    if p < word_positions[i]:
                        new_positions_left.append(abs(p - word_positions[i]))
                    if p > word_positions[i]:
                        new_positions_right.append(abs(p - word_positions[i]))

                if len(new_positions_left) >= position_size or len(new_positions_right) >= position_size:
                    continue
                n.append(current_nouns[i])
                words_left.append(current_words[:word_positions[i]])
                lemmas_left.append(current_lemmas[:word_positions[i]])
                morphos_left.append(current_morphos[:word_positions[i]])

                words_right.append(list(reversed(current_words[word_positions[i] + 1:])))
                lemmas_right.append(list(reversed(current_lemmas[word_positions[i] + 1:])))
                morphos_right.append(list(reversed(current_morphos[word_positions[i] + 1:])))
                morpho.append([current_morphos[word_positions[i]]])
            word_positions = []
            current_words = []
            current_lemmas = []
            current_morphos = []
            current_positions = []
            p = -1
    if words_left:
        add_padding(words_left)
        add_padding(words_right)
        add_padding(lemmas_right)
        add_padding(lemmas_left)
        add_padding(morphos_right)
        add_padding(morphos_left)
        add_padding(morpho)
        X = [np.array(words_left), np.array(lemmas_left), np.array(morphos_left),
             np.array(words_right), np.array(lemmas_right), np.array(morphos_right),
             np.array(morpho)]

        predictions = {}
        for g in gigasenses:
            predictions[g] = models[g].predict(X)
        for i in range(len(n)):
            result_file.write(n[i] + "\t")
            for g in gigasenses:
                prediction = predictions[g][i][0]
                result_file.write(str(prediction) + "\t")
            result_file.write("\n")
                # if prediction > 0.5:
                #     num[w][g] += 1
                # num[w][g] += prediction * pow(2.0 * (0.5 - prediction), exponent)
                # denum[w][g] += pow(2.0 * (0.5 - prediction), exponent)
                # occ[w] += 1
            # if prediction > 0.95:
            #     occ[w] += 1
            #     num[w] += 1
            #     denum[w] += 1
            # elif prediction < 0.05:
            #     denum[w] += 1
            #     occ[w] += 1


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage_and_exit()
    models = {}
    for g in gigasenses:
        models[g] = load_model("models/seeds." + g + ".h5")
    nouns = get_set_from_file(sys.argv[1])
    for n in nouns:
        occ[n] = 0
        num[n] = {}
        denum[n] = {}
        for g in gigasenses:
            num[n][g] = 0
            denum[n][g] = 0
    directory = "data/contexts/version2"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # name_of_list = os.path.basename(sys.argv[2])
    mcf_filename = sys.argv[2]
    result_file = io.open(directory + "/" + os.path.basename(mcf_filename[:-4]), 'w', encoding='utf8')
    # i = 0
    # for filename in os.listdir(sys.argv[1]):
    #     i += 1
    #     print("File " + str(i))
    file = io.open(os.path.join("data/frWaC/10000-nouns-mcf", mcf_filename), "r", encoding='utf8')
    buffer = ""
    for line in file:
        tmp = line.split("\t")
        if len(tmp) == 7:
            buffer += line
            if tmp[6] == "1\n":
                update(buffer, nouns, result_file)
                buffer = ''
            if len(nouns) - len(nouns_finished) == 0:
                break

    # for n in nouns:
    #     result_file.write(n)
    #     for g in gigasenses:
    #         if denum[n][g] == 0:
    #             print(n)
    #             continue
    #         r = num[n][g]/occ[n]
    #         result_file.write("\t" + str(r))
    #     result_file.write("\n")
