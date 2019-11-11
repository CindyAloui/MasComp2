import io
import sys
import os
import numpy as np
from src.classifier import get_index, get_set_from_file, get_dir_from_file
from keras.models import load_model
from random import shuffle

gigasenses = {"Living_Animate_Entity", "Natural_Object", "Manufactured_Object", "Informational_Object",
              "Dynamic_situation", "Stative_situation"}
position_size = 300

threshold = 0.3

vocab_words = get_dir_from_file("data/vocabs/words")
vocab_lemmas = get_dir_from_file("data/vocabs/lemmas")
vocab_morphos = get_dir_from_file("data/vocabs/morphos")
occ = {}
positive = {}
negative = {}
neutre = {}
errors = {}
successes = {}
other = {}
nouns_positive = {}
nouns_negative = {}

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

def sentence(l, p):
    r = ''
    for i in range(len(l)):
        if i == p:
            r += '[[' + l[i] + "]" + ' '
        else:
            r += l[i] + ' '
    return r

def update(buffer, g):
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
    y = []
    s = []
    tmp = []
    for line in buffer.split("\n"):
        line = line.split("\t")
        if len(line) != 7:
            continue
        p += 1
        current_words.append(get_index(line[0], vocab_words))
        current_lemmas.append(get_index(line[3], vocab_lemmas))
        current_morphos.append(get_index(line[2], vocab_morphos))
        tmp.append(line[0])
        current_positions.append(p)
        if line[1] == "NOUN" and (line[3] in nouns_positive[g] or line[3] in nouns_negative[g]):
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

                if len(new_positions_left) >= position_size or len(new_positions_right) >= position_size :
                    continue
                n.append(current_nouns[i])
                words_left.append(current_words[:word_positions[i]])
                lemmas_left.append(current_lemmas[:word_positions[i]])
                morphos_left.append(current_morphos[:word_positions[i]])

                words_right.append(list(reversed(current_words[word_positions[i] + 1:])))
                lemmas_right.append(list(reversed(current_lemmas[word_positions[i] + 1:])))
                morphos_right.append(list(reversed(current_morphos[word_positions[i] + 1:])))
                morpho.append([current_morphos[word_positions[i]]])
                s.append(sentence(tmp, word_positions[i]))
            tmp = []
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
        predictions = models[g].predict(X)
        for i in range(len(predictions)):
            prediction = predictions[i][0]
            w = n[i]
            if prediction < 0.5 - threshold:
                positive[g][w] += 1
                if w in nouns_negative[g]:
                    errors[g]["neg"].append(s[i])
                else:
                    successes[g]["pos"].append(s[i])
            elif prediction > 0.5 + threshold:
                negative[g][w] += 1
                if w in nouns_negative[g]:
                    successes[g]["neg"].append(s[i])
                else:
                    errors[g]["pos"].append(s[i])
            else:
                neutre[g][w] += 1
                if w in nouns_negative[g]:
                    other[g]["neg"].append(s[i])
                else:
                    other[g]["pos"].append(s[i])

            occ[w] += 1


if __name__ == '__main__':
    models = {}
    for g in gigasenses:
        models[g] = load_model("models/seeds." + g + ".h5")
    for g in gigasenses:
        nouns_positive[g] = get_set_from_file("data/seeds/seeds-super-supersenses/seeds." + g + "-dev.txt")
        nouns_negative[g] = get_set_from_file("data/seeds/seeds-super-supersenses/not_seeds." + g + "-dev.txt")

    for g in gigasenses:
        positive[g] = {}
        negative[g] = {}
        neutre[g] = {}
        errors[g] = {"pos": [], "neg": []}
        successes[g] = {"pos": [], "neg": []}
        other[g] = {"pos": [], "neg": []}
        for n in nouns_positive[g]:
            positive[g][n] = 0
            negative[g][n] = 0
            neutre[g][n] = 0
            occ[n] = 0
        for n in nouns_negative[g]:
            positive[g][n] = 0
            negative[g][n] = 0
            neutre[g][n] = 0
            occ[n] = 0

    directory = "exemples"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for g in gigasenses:
        print(g)
        filename = "data/frWaC/mcf_supersenses/mcf_seeds." + g + "/dev.mcf"
        file = io.open(filename, "r", encoding='utf8')
        buffer = ""
        for line in file:
            tmp = line.split("\t")
            if len(tmp) == 7:
                buffer += line
                if tmp[6] == "1\n":
                    update(buffer, g)
                    buffer = ''
        shuffle(errors[g]["pos"])
        shuffle(errors[g]["neg"])
        shuffle(successes[g]["pos"])
        shuffle(successes[g]["neg"])
        shuffle(other[g]["pos"])
        shuffle(other[g]["neg"])

        result_file = io.open(directory + "/" + g, 'w', encoding='utf8')
        result_file.write("Erreurs : \n\n\n\tSur des contextes devant être prédits comme appartenant au super-supersense:\n\n ")
        for i in range(10):
            result_file.write(errors[g]["pos"][i] + "\n")
        result_file.write("\n\n\n\tSur des contextes devant être prédits comme n'appartenant pas au super-supersense:\n\n ")
        for i in range(10):
            if i >= len(errors[g]["neg"]):
                continue
            result_file.write(errors[g]["neg"][i] + "\n")

        result_file.write("\n\n-----------------------------------------------------------\n"
                          "\nReussites : \n\n\tSur des contextes devant être prédits comme appartenant au super-supersense:\n\n ")
        for i in range(10):
            result_file.write(successes[g]["pos"][i] + "\n")
        result_file.write("\n\n\n\tSur des contextes devant être prédits comme n'appartenant pas au super-supersense:\n\n ")
        for i in range(10):
            result_file.write(successes[g]["neg"][i] + "\n")

        result_file.write("\n\n-----------------------------------------------------------\n"
                          "\nContexte prédit comme non discriminant : \n\n\tSur des contextes devant être prédits comme appartenant au super-supersense:\n\n ")
        for i in range(10):
            result_file.write(other[g]["pos"][i] + "\n")
        result_file.write("\n\n\n\tSur des contextes devant être prédits comme n'appartenant pas au super-supersense:\n\n ")
        for i in range(10):
            result_file.write(other[g]["neg"][i] + "\n")

        # for n in nouns_positive[g]:
        #     result_file.write(n + " : \n")
        #     result_file.write("\t " + str(positive[g][n]) + " contextes prédits comme appartenant au supersense \n")
        #     result_file.write("\t " + str(neutre[g][n]) + " contextes prédits comme non discriminants \n")
        #     result_file.write("\t " + str(negative[g][n]) + " contextes prédits comme n'appartenant pas au supersense \n")
        #     result_file.write("\n\n")
        #
        # result_file.write("\n\n__________________________________________________________________________________\n\n ")
        # result_file.write("Noms n'appartenant pas au supersense : \n\n ")
        # for n in nouns_negative[g]:
        #     result_file.write(n + " : \n")
        #     result_file.write("\t " + str(positive[g][n]) + " contextes prédits comme appartenant au supersense \n")
        #     result_file.write("\t " + str(neutre[g][n]) + " contextes prédits comme non discriminants \n")
        #     result_file.write("\t " + str(negative[g][n]) + " contextes prédits comme n'appartenant pas au supersense \n")
        #     result_file.write("\n\n")
        #
