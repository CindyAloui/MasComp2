import io
import os
import sys
from src.classifier import Classifier
from keras.models import load_model

c = 0
m = 0
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


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage_and_exit()
    dir = sys.argv[3]
    model = load_model("models/" + sys.argv[1] + ".h5")
    lexical_scores = get_lexical_scores_from_file(sys.argv[2])
    total = 0.0
    total_good = 0.0

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


    for filename in os.listdir(dir):
        file = io.open(os.path.join(dir, filename), "r", encoding='utf8')
        name = filename[:-4]
        if name not in lexical_scores:
            print(name)
            # exit(0)
            lexical_scores[name] = 0
        if lexical_scores[name] > 0.5:
            c = "M"
        else:
            c = "C"
        for line in file:
            if line[0] == "C" or line[0] == "M":
                total += 1.0
            if line[0] == c:
                total_good += 1.0
    print(total_good/total)
