import io
import os
import sys
from src.classifier import Classifier
from keras.models import load_model


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <modelName> <lexicalScores> <testDir>")
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print_usage_and_exit()
    dir = sys.argv[3]
    model = load_model("models/" + sys.argv[1] + ".h5")
    for filename in os.listdir(dir):
        file = io.open(os.path.join(dir, filename), "r", encoding='utf8')
