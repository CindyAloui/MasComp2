from keras import Model
from keras.layers.embeddings import Embedding
from keras.layers import Input, LSTM, Dense, Flatten, Concatenate
from keras.models import load_model
import numpy as np
import io
import os
from random import choice

embed_word_dim = 128
embed_lemma_dim = 128
embed_morpho_dim = 32
embed_position_dim = 32
nb_epochs = 1
batch_size = 128


def get_set_from_file(filename):
    file = io.open(filename, "r", encoding="utf8")
    list = set()
    for line in file:
        list.add(line[:-1])
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
    input_positions_left = Input(shape=(None,), dtype='int32')
    emb_word_left = Embedding(len(vocab_words), embed_word_dim)(input_words_left)
    emb_lemma_left = Embedding(len(vocab_lemmas), embed_lemma_dim)(input_lemmas_left)
    emb_morpho_left = Embedding(len(vocab_morphos), embed_morpho_dim)(input_morphos_left)
    emb_position_left = Embedding(position_size, embed_position_dim)(input_positions_left)
    concat_left = Concatenate()([emb_word_left, emb_lemma_left, emb_morpho_left, emb_position_left])
    lstm_left = LSTM(300)(concat_left)
    input_words_right = Input(shape=(None,))
    input_lemmas_right = Input(shape=(None,))
    input_morphos_right = Input(shape=(None,))
    input_positions_right = Input(shape=(None,), dtype='int32')
    emb_word_right = Embedding(len(vocab_words), embed_word_dim)(input_words_right)
    emb_lemma_right = Embedding(len(vocab_lemmas), embed_lemma_dim)(input_lemmas_right)
    emb_morpho_right = Embedding(len(vocab_morphos), embed_morpho_dim)(input_morphos_right)
    emb_position_right = Embedding(position_size, embed_position_dim)(input_positions_right)
    concat_right = Concatenate()([emb_word_right, emb_lemma_right, emb_morpho_right, emb_position_right])
    lstm_right = LSTM(300)(concat_right)

    morpho = Input(shape=(None,))
    emb_morpho = Embedding(len(vocab_morphos), embed_morpho_dim, input_length=1)(morpho)
    flat = Flatten()(emb_morpho)
    concat = Concatenate()([lstm_left, flat, lstm_right])

    dense = Dense(300)(concat)
    output = Dense(2, activation="softmax")(dense)
    model = Model(inputs=[input_words_left, input_lemmas_left, input_morphos_left, input_positions_left,
                          input_words_right, input_lemmas_right, input_morphos_right, input_positions_right, morpho],
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


class Classifier:
    def __init__(self, class1_file, class2_file, model=None):
        self.class1_name = os.path.basename(class1_file)
        self.class2_name = os.path.basename(class2_file)
        self.class1 = get_set_from_file(class1_file)
        self.class2 = get_set_from_file(class2_file)
        if model == None:
            self.model = new_lstm_model()
        else:
            self.model = load_model(model)

    def train(self, dir, model_filename):
        words_left = []
        lemmas_left = []
        morphos_left = []
        positions_left = []
        words_right = []
        lemmas_right = []
        morphos_right = []
        positions_right = []
        current_words = []
        current_lemmas = []
        current_morphos = []
        current_positions = []
        morpho = []
        Y = []
        current_y = []
        word_positions = []
        p = -1
        filenames = []
        for filename in os.listdir(dir):
            filenames.append(filename)
        dev_filename = choice(filenames)
        filenames.remove(dev_filename)
        filenames.append(dev_filename)
        best_loss = None
        for epoch in range(nb_epochs):
            total_loss = 0
            print("Epochs " + str(epoch))
            for filename in filenames:
                print(filename)
                file = io.open(os.path.join(dir, filename), "r", encoding="utf8")
                for line in file:
                    line = line.split("\t")
                    if len(line) != 7:
                        continue
                    p += 1
                    current_words.append(get_index(line[0], vocab_words))
                    current_lemmas.append(get_index(line[3], vocab_lemmas))
                    current_morphos.append(get_index(line[2], vocab_morphos))
                    current_positions.append(p)
                    if line[1] == "NOUN" and line[3] in self.class1:
                        word_positions.append(p)
                        current_y.append([0, 1])
                    if line[1] == "NOUN" and line[3] in self.class2:
                        word_positions.append(p)
                        current_y.append([1, 0])
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
                            positions_left.append(new_positions_left)

                            words_right.append(list(reversed(current_words[word_positions[i] + 1:])))
                            lemmas_right.append(list(reversed(current_lemmas[word_positions[i] + 1:])))
                            morphos_right.append(list(reversed(current_morphos[word_positions[i] + 1:])))
                            positions_right.append(list(reversed(new_positions_right)))
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
                            add_padding(positions_right)
                            add_padding(positions_left)
                            add_padding(morpho)
                            X = [np.array(words_left), np.array(lemmas_left), np.array(morphos_left),
                                 np.array(positions_left), np.array(words_right), np.array(lemmas_right), np.array(morphos_right),
                                 np.array(positions_right), np.array(morpho)]
                            # print(self.model.train_on_batch(X, np.array(Y)))
                            if filename != dev_filename:
                                self.model.train_on_batch(X, np.array(Y))
                            else:
                                r = self.model.evaluate(X, np.array(Y))
                                print(r)
                                total_loss += r[0]
                            Y = []
                            words_left = []
                            lemmas_left = []
                            morphos_left = []
                            positions_left = []
                            words_right = []
                            lemmas_right = []
                            morphos_right = []
                            positions_right = []
                            morpho = []
                if words_left and filename != dev_filename:
                    add_padding(words_left)
                    add_padding(words_right)
                    add_padding(lemmas_right)
                    add_padding(lemmas_left)
                    add_padding(morphos_right)
                    add_padding(morphos_left)
                    add_padding(positions_right)
                    add_padding(positions_left)
                    add_padding(morpho)
                    X = [np.array(words_left), np.array(lemmas_left), np.array(morphos_left),
                         np.array(positions_left), np.array(words_right), np.array(lemmas_right), np.array(morphos_right),
                         np.array(positions_right), np.array(morpho)]
                    # print(self.model.train_on_batch(X, np.array(Y)))
                    self.model.train_on_batch(X, np.array(Y))
                # print(self.model.metrics_names)
            if best_loss is None or total_loss < best_loss:
                best_loss = total_loss
                self.save(model_filename)
            else:
                print("Best loss: " + str(best_loss))
                return

    def save(self, model_filename):
        print("Saving...")
        self.model.save("models/" + model_filename + ".h5")
