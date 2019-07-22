import io
import os


def write_vocab(vocab, file):
    for w in vocab:
        file.write(w + "\n")


if __name__ == '__main__':
    dir = "data/frWaC/mcf_test/"
    words = set()
    lemmas = set()
    morpho = set()
    for filename in os.listdir(dir):
        file = io.open(os.path.join(dir, filename), "r", encoding='utf8')
        for line in file :
            line = line.split("\t")
            if len(line) != 7:
                continue
            words.add(line[0])
            lemmas.add(line[3])
            morpho.add(line[2])

    words_file =io.open("data/vocabs/words", "w", encoding='utf8')
    lemmas_file =io.open("data/vocabs/lemmas", "w", encoding='utf8')
    morphos_file =io.open("data/vocabs/morphos", "w", encoding='utf8')

    write_vocab(words, words_file)
    write_vocab(lemmas, lemmas_file)
    write_vocab(morpho, morphos_file)