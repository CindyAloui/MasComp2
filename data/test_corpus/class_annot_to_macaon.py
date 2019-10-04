import io
import os

# for fname in os.listdir("countability/class_annot"):
#     file = io.open(os.path.join("countability/class_annot", fname), "r", encoding="utf8")
#     result_file = io.open(os.path.join("countability/to_treat.txt", fname), "w", encoding="utf8")
#     for line in file:
#         line = line.split()
#         buffer = ""
#         del line[0]
#         for word in line:
#             if "[[" not in word and "]]" not in word:
#                 result_file.write(word + "\n")

file = io.open("animacy/annotations.txt", "r", encoding="utf8")
result_file = io.open("animacy/to_treat.txt", "w", encoding="utf8")
for line in file:
    line = line.split()
    buffer = ""
    del line[0]
    for word in line:
        if "[[" not in word and "]]" not in word:
            result_file.write(word + "\n")
