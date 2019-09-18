import os
import sys
from src.classifier import Classifier
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <fileClass1> <fileClass2> <corpusDir> <modelFileName>")
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print_usage_and_exit()
    classifier = Classifier(class1_file=sys.argv[1], class2_file=sys.argv[2])
    classifier.train(sys.argv[3], sys.argv[4])
