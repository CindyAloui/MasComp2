import io
import os
import sys
from src.classifier import Classifier
from keras.models import load_model
from src.classifier import get_index, get_dir_from_file, add_padding
import numpy as np

class_1 = "C"
class_2 = "M"
vocab_words = get_dir_from_file("data/vocabs/words")
vocab_lemmas = get_dir_from_file("data/vocabs/lemmas")
vocab_morphos = get_dir_from_file("data/vocabs/morphos")
position_size = 300



def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <modelName> <lexicalScores> <testDir>")
    sys.exit(0)


def get_lexical_scores_from_file(filename):
    file = io.open(filename, "r", encoding='utf8')
    scores = {}
    for line in file:
        line = line.split("\t")
        scores[line[0]] = float(line[1][:-1])
    return scores


def get_X_Y(file):
    words_left = []
    lemmas_left = []
    morphos_left = []
    words_right = []
    lemmas_right = []
    morphos_right = []
    current_words = []
    current_lemmas = []
    current_morphos = []
    current_positions = []
    morpho = []
    current_y = []
    Y = []
    word_positions = []
    p = -1
    noun = os.path.basename(file.name)[:-4]
    annot = None
    while True:
        line = file.readline()
        if not line:
            break
        if line[0] == "#" and (line[1] == class_1 or line[1] == class_2):
            print("ok")
            annot = line[1]
        line = line.split("\t")
        if len(line) != 7:
            continue
        p += 1
        w = line[0]
        l = line[3]
        if line[1] == "NOUN" and line[3] == noun and annot != None:
            word_positions.append(p)
            current_y.append(annot)
        current_words.append(get_index(w, vocab_words))
        current_lemmas.append(get_index(l, vocab_lemmas))
        current_morphos.append(get_index(line[2], vocab_morphos))
        current_positions.append(p)
        if line[6] == "1\n":
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
                words_left.append(current_words[:word_positions[i]])
                lemmas_left.append(current_lemmas[:word_positions[i]])
                morphos_left.append(current_morphos[:word_positions[i]])
                words_right.append(list(reversed(current_words[word_positions[i] + 1:])))
                lemmas_right.append(list(reversed(current_lemmas[word_positions[i] + 1:])))
                morphos_right.append(list(reversed(current_morphos[word_positions[i] + 1:])))
                morpho.append([current_morphos[word_positions[i]]])
                Y.append(np.array(current_y[i]))
            word_positions = []
            current_y = []
            current_words = []
            current_lemmas = []
            current_morphos = []
            current_positions = []
            p = -1

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
    return X, Y


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage_and_exit()
    dir = sys.argv[3]
    model = load_model("models/" + sys.argv[1] + ".h5")
    lexical_scores = get_lexical_scores_from_file(sys.argv[2])
    total = 0.0
    total_good = 0.0

    #Test contexte

    for filename in os.listdir(dir):
        file = io.open(os.path.join(dir, filename), "r", encoding='utf8')
        X, Y = get_X_Y(file)
        predictions = model.predict(X)
        for i in range(len(predictions)):
            total += 1
            prediction = predictions[i][0]
            if prediction < 0.5 and Y[i] == class_1:
                total_good += 1
            elif prediction >= 0.5 and Y[i] == class_2:
                total_good += 1
    print(total_good/total)


    #Test animacy
    
    # for filename in os.listdir(dir):
    #     file = io.open(os.path.join(dir, filename), "r", encoding='utf8')
    #     for line in file:
    #         flag = False
    #         line = line.split()
    #         annot = line[0].split("|")[0]
    #         for word in line:
    #             word = word.split("|")
    #             if word[0] == "[[":
    #                 flag = True
    #             elif word[0] == "]]":
    #                 flag = False
    #             elif flag == True:
    #
    #                 lemma = word[1]
    #                 if lemma in lexical_scores:
    #                     if lexical_scores[lemma] < 0.5:
    #                         pred = "A"
    #                     else:
    #                         pred = "I"
    #                 else:
    #                     pred = "I"
    #                 if annot == "A" or annot == "I":
    #                     total += 1
    #                     if annot == pred:
    #                         total_good += 1
    # print(total_good/total)


    #Test countable
    # for filename in os.listdir(dir):
    #     file = io.open(os.path.join(dir, filename), "r", encoding='utf8')
    #     name = filename[:-4]
    #     if name not in lexical_scores:
    #         print(name)
    #         # exit(0)
    #         lexical_scores[name] = 0
    #     if lexical_scores[name] > 0.5:
    #         c = "M"
    #     else:
    #         c = "C"
    #     for line in file:
    #         if line[0] == "C" or line[0] == "M":
    #             total += 1.0
    #         if line[0] == c:
    #             total_good += 1.0
    # print(total_good/total)
