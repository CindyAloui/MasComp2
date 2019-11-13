from keras import Model
from keras.layers.embeddings import Embedding
from keras.layers import Input, LSTM, Dense, Flatten, Concatenate
from keras.models import load_model
import numpy as np
import io
import os
from random import shuffle, random

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
embed_word_dim = 500
embed_lemma_dim = 500
embed_morpho_dim = 64
embed_position_dim = 64
epochs_size = 30000
batch_size = 128
max_epoch_without_upgrade = 10
mask = 0.3

def get_set_from_file(filename):
    file = io.open(filename, "r", encoding="utf8")
    list = set()
    for line in file:
        line = line.replace("\n", '').split()
        list.add(line[0])
    return list


def get_dir_from_file(filename):
    file = io.open(filename, "r", encoding="utf8")
    dir = {}
    dir["__NO_WORD__"] = 0
    i = 1
    for line in file:
        dir[line[:-1]] = i
        i += 1
    dir["__UNKNOWN__"] = i
    return dir


def get_index(w, vocab):
    if w in vocab:
        return vocab[w]
    return vocab["__UNKNOWN__"]


vocab_words = get_dir_from_file("data/vocabs/words")
vocab_lemmas = get_dir_from_file("data/vocabs/lemmas")
vocab_morphos = get_dir_from_file("data/vocabs/morphos")
position_size = 300


def new_lstm_model():
    input_words_left = Input(shape=(None,))
    input_lemmas_left = Input(shape=(None,))
    input_morphos_left = Input(shape=(None,))
    emb_word_left = Embedding(len(vocab_words), embed_word_dim)(input_words_left)
    emb_lemma_left = Embedding(len(vocab_lemmas), embed_lemma_dim)(input_lemmas_left)
    emb_morpho_left = Embedding(len(vocab_morphos), embed_morpho_dim)(input_morphos_left)
    concat_left = Concatenate()([emb_word_left, emb_lemma_left, emb_morpho_left])
    lstm_left = LSTM(300)(concat_left)
    input_words_right = Input(shape=(None,))
    input_lemmas_right = Input(shape=(None,))
    input_morphos_right = Input(shape=(None,))
    emb_word_right = Embedding(len(vocab_words), embed_word_dim)(input_words_right)
    emb_lemma_right = Embedding(len(vocab_lemmas), embed_lemma_dim)(input_lemmas_right)
    emb_morpho_right = Embedding(len(vocab_morphos), embed_morpho_dim)(input_morphos_right)
    concat_right = Concatenate()([emb_word_right, emb_lemma_right, emb_morpho_right])
    lstm_right = LSTM(300)(concat_right)

    morpho = Input(shape=(None,))
    emb_morpho = Embedding(len(vocab_morphos), embed_morpho_dim, input_length=1)(morpho)
    flat = Flatten()(emb_morpho)
    concat = Concatenate()([lstm_left, flat, lstm_right])

    dense = Dense(150)(concat)
    output = Dense(2, activation="softmax")(dense)
    model = Model(inputs=[input_words_left, input_lemmas_left, input_morphos_left,
                          input_words_right, input_lemmas_right, input_morphos_right, morpho],
                  outputs=output)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
    return model


def add_padding(words):
    max_len = 0
    for word in words:
        if max_len < len(word):
            max_len = len(word)
    for i in range(len(words)):
        for j in range(len(words[i]), max_len):
            words[i].insert(0, 0)
    for word in words:
        if len(word) != max_len:
            print("BUG")


def get_batch(file, class1, class2):
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
    Y = []
    current_y = []
    word_positions = []
    p = -1

    while True:
        line = file.readline()
        if not line:
            break
        line = line.split("\t")
        if len(line) != 7:
            continue
        p += 1
        w = line[0]
        l = line[3]
        if line[1] == "NOUN" and line[3] in class1:
            word_positions.append(p)
            current_y.append([0, 1])
        elif line[1] == "NOUN" and line[3] in class2:
            word_positions.append(p)
            current_y.append([1, 0])
        elif os.path.basename(file.name) != "dev.mcf" and random() < mask:
            l = "__UNKNOWN__"
            w = "__UNKNOWN__"
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
            if len(words_left) >= batch_size:
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
                return X, Y, True

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
    return X, Y, False


class Classifier:
    def __init__(self, class1_file=None, class2_file=None, model=None):
        if class1_file != None:
            self.class1_name = os.path.basename(class1_file)
            self.class2_name = os.path.basename(class2_file)
            self.class1_dev = get_set_from_file(class1_file + "-dev.txt")
            self.class2_dev = get_set_from_file(class2_file + "-dev.txt")
            self.class1_train = get_set_from_file(class1_file + "-train.txt")
            self.class2_train = get_set_from_file(class2_file + "-train.txt")
        if model == None:
            self.model = new_lstm_model()
        else:
            self.model = load_model(model)

    def evaluate_on_dev(self, dev_filename, class1, class2):
        file = io.open(dev_filename, "r", encoding="utf8")
        flag = True
        loss = 0
        accuracy = 0
        nb = 0
        while flag:
            X, Y, flag = get_batch(file, class1, class2)
            l, a = self.model.evaluate(X, np.array(Y), verbose=0)
            nb += len(X[0])
            loss += l * len(X[0])
            accuracy += a * len(X[0])
            # if nb >= epochs_size:
            #     flag = False
        print("Loss : " + str(loss/nb) + " , acc : " + str(accuracy/nb))
        return accuracy / nb

    def train(self, dir, model_filename):
        current_epoch_size = 0
        filenames = []
        nb_epoch = 1
        nb_epoch_without_upgrade = 0
        print("Iter " + str(nb_epoch))
        best_accuracy = None
        for filename in os.listdir(dir):
            filenames.append(filename)
        filenames.remove("dev.mcf")
        dev_filename = os.path.join(dir, "dev.mcf")

        while True:
            shuffle(filenames)
            for filename in filenames:
                print("File : " + filename)
                class1 = self.class1_train
                class2 = self.class2_train
                file = io.open(os.path.join(dir, filename), "r", encoding="utf8")
                flag = True
                while flag:
                    X, Y, flag = get_batch(file, class1, class2)
                    print(X)
                    print(Y)
                    print("\n\n")
                    self.model.train_on_batch(X, np.array(Y))
                    current_epoch_size += len(X[0])
                    if current_epoch_size >= epochs_size:
                        accuracy = self.evaluate_on_dev(dev_filename, self.class1_dev, self.class2_dev)
                        current_epoch_size = 0
                        nb_epoch += 1
                        if best_accuracy is None or accuracy > best_accuracy:
                            nb_epoch_without_upgrade = 0
                            best_accuracy = accuracy
                            self.save(model_filename)
                        else:
                            nb_epoch_without_upgrade += 1
                        if nb_epoch_without_upgrade >= max_epoch_without_upgrade:
                            print("Best accuracy: " + str(best_accuracy))
                            return
                        print("Iter " + str(nb_epoch))


    def save(self, model_filename):
        print("Saving...")
        self.model.save("models/" + model_filename + ".h5")
