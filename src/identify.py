import io
import os
import sys


def print_usage_and_exit():
    print("Usage: " + sys.argv[0] + " <inputDir> <outputDir>")
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage_and_exit()
    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    id = 0
    for filename in os.listdir(input_dir):
        print(filename)
        old_file = io.open(os.path.join(input_dir, filename), 'r', encoding="utf8")
        new_file = io.open(os.path.join(output_dir, filename), "w", encoding="utf8")
        buffer = ""
        for line in old_file:
            if line[0] == "#" and len(line.split("\t")) != 7:
                continue
            buffer += line
            line = line.split("\t")
            if len(line) == 7 and line[6] == '1\n':
                new_file.write("#id_" + str(id) + "\n" + buffer)
                id += 1
                buffer = ""