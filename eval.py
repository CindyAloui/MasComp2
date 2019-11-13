import io
import os
import sys
import operator
from math import log

def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <goldFile> <predFile>")
    sys.exit(0)

def get_DCG(gold, pred):
    DCG = 0.0
    for s in gold:
        DCG += gold[s]/log(pred[s] + 1, 2)
    return DCG

def get_iDCG(gold):
    iDCG = 0.0
    rank = sorted(gold.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(len(rank)):
        iDCG += gold[rank[i][0]]/log(i + 2, 2)
    return iDCG

def all_zero(l):
    for n in l:
        if l[n] != 0:
            return False
    return True

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage_and_exit()
    gold = {}
    pred = {}

    gold_file = io.open(sys.argv[1], 'r', encoding='utf8').readlines()
    pred_file = io.open(sys.argv[2], 'r', encoding='utf8').readlines()

    gold_col = gold_file[0].replace("\n", '').split("\t")
    pred_col = pred_file[0].replace("\n", "").split("\t")

    for i in range(1, len(gold_file)):
        line = gold_file[i].split("\t")[:-1]
        if len(line) != 7:
            print(line)
            continue
        gold[line[0]] = {}
        for j in range(1, 7):
            # if gold_col[j] == "Natural_Object":
            #     continue
            if line[j] != '0':
                line[j] = '1'
            else:
                line[j] = '0'
            gold[line[0]][gold_col[j]] = int(line[j])

    for i in range(1, len(pred_file)):
        line = pred_file[i].replace("\n", "").split("\t")
        if len(line) != 7 or line[0] not in gold:
            continue
        pred[line[0]] = {}
        pred_tmp = {}
        for j in range(1, 7):
    #         if float(line[j]) > 0.5:
    #             pred[line[0]][pred_col[j]] = 0
    #         else:
    #             pred[line[0]][pred_col[j]] = 1
    #
    # good = 0.0
    # total = 0.0
    #
    # for noun in gold:
    #     for g in gold[noun]:
    #         total += 1
    #         if gold[noun][g] == pred[noun][g]:
    #             good += 1
    #
    # print(good/total)

            # if pred_col[j] == "Natural_Object":
            #     continue
            pred_tmp[pred_col[j]] = line[j]

        sorted_pred = sorted(pred_tmp.items(), key=operator.itemgetter(1))
        rank = 1
        for t in sorted_pred:
            pred[line[0]][t[0]] = rank
            rank += 1


    nDCG = {}
    mAP = {}
    for noun in gold:
        # mAP[noun] = get_mAP(gold[noun], pred[noun])
        if all_zero(gold[noun]):
            continue
        DCG = get_DCG(gold[noun], pred[noun])
        iDCG = get_iDCG(gold[noun])
        if iDCG == 0:
            print(gold[noun])
        nDCG[noun] = DCG/iDCG

    mean = 0
    for noun in nDCG:
        mean += nDCG[noun]
        print(noun + ' ' + str(nDCG[noun]))

    print("\n\n")
    print("Moyenne sur tout les noms : " + str(mean/len(nDCG)) + "\n\n")


#     if len(sys.argv) != 3:
#         print_usage_and_exit()
    gold = {}
    pred = {}

    gold_file = io.open(sys.argv[1], 'r', encoding='utf8').readlines()
    pred_file = io.open(sys.argv[2], 'r', encoding='utf8').readlines()

    gold_col = gold_file[0].replace("\n", '').split("\t")
    pred_col = pred_file[0].replace("\n", '').split("\t")

    for c in gold_col:
        if c != 'NOUN':
            gold[c] = {}
            pred[c] = {}

    for i in range(1, len(gold_file)):
        line = gold_file[i].replace("\n", '').split("\t")[:-1]
        if len(line) != 7:
            print(line)
            continue
        # gold[line[0]] = {}
        for j in range(1, 7):
            if line[j] != '0':
                line[j] = '1'
            gold[gold_col[j]][line[0]] = int(line[j])

    for i in range(1, len(pred_file)):
        line = pred_file[i].replace("\n", '').split("\t")
        if len(line) != 7:
            continue
        # pred[line[0]] = {}
        for j in range(1, 7):
            pred[pred_col[j]][line[0]] = line[j]

    for col in pred :
        sorted_pred = sorted(pred[col].items(), key=operator.itemgetter(1))
        rank = 1
        for t in sorted_pred:
            pred[col][t[0]] = rank
            rank += 1

    nDCG = {}
    for noun in gold:
        DCG = get_DCG(gold[noun], pred[noun])
        iDCG = get_iDCG(gold[noun])
        nDCG[noun] = DCG/iDCG

    mean = 0
    for noun in nDCG:
        print(noun.strip() + " : " + str(nDCG[noun]))