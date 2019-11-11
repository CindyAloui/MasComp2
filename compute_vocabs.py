import io
import os

def add(dic, w):
    if w not in dic:
        dic[w] = 0
    dic[w] += 1

def write_vocab(vocab, file):
    for w in vocab:
        if vocab[w] > 1000:
            file.write(w + "\n")


if __name__ == '__main__':
    dir = "data/frWaC/mcf/"
    words = {}
    lemmas = {}
    morpho = {}
    i = 0
    for filename in os.listdir(dir):
        print(i)
        i += 1
        file = io.open(os.path.join(dir, filename), "r", encoding='utf8')
        for line in file :
            line = line.split("\t")
            if len(line) != 7:
                continue
            add(words, line[0])
            add(lemmas, line[3])
            add(morpho, line[2])

    words_file =io.open("data/vocabs/words", "w", encoding='utf8')
    lemmas_file =io.open("data/vocabs/lemmas", "w", encoding='utf8')
    morphos_file =io.open("data/vocabs/morphos", "w", encoding='utf8')

    write_vocab(words, words_file)
    write_vocab(lemmas, lemmas_file)
    write_vocab(morpho, morphos_file)