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

def get_iDCG(gold, pred):
    iDCG = 0.0
    rank = sorted(gold.items(), key=operator.itemgetter(1))
    for i in range(len(rank)):
        iDCG += gold[rank[i][1]]/log(i + 2, 2)
    return iDCG

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage_and_exit()
    gold = {}
    pred = {}

    gold_file = io.open(sys.argv[1], 'r', encoding='utf8').readlines()
    pred_file = io.open(sys.argv[2], 'r', encoding='utf8').readlines()

    gold_col = gold_file[0].split("\t")
    pred_col = pred_file[0].split("\t")

    for i in range(1, len(gold_file)):
        line = gold_file[i].split("\t")[:-1]
        if len(line) != 7:
            print(line)
            continue
        gold[line[0]] = {}
        for j in range(1, 7):
            if line[j] != '0':
                line[j] = '1'
            gold[line[0]][gold_col[j]] = int(line[j])

    for i in range(1, len(pred_file)):
        line = pred_file[i].split("\t")[:-1]
        if len(line) != 7 or line[0] not in gold:
            continue

        pred[line[0]] = {}
        pred_tmp = {}
        for j in range(1, 7):
            pred_tmp[gold_col[j]] = line[j]
        sorted_pred = sorted(pred_tmp.items(), key=operator.itemgetter(1))
        rank = 1
        for t in sorted_pred:
            pred[line[0]][t[0]] = rank
            rank += 1

    nDCG = {}
    for noun in gold:
        DCG = get_DCG(gold[noun], pred[noun])
        iDCG = get_iDCG(gold[noun])
        nDCG[noun] = DCG/iDCG
