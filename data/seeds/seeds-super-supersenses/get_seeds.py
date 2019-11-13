from nltk.corpus import wordnet as wn
import io
from random import choices
import os
from operator import itemgetter

# file = io.open("all_nouns_with_supersenses.txt", "w", encoding='utf8')

gigasenses = {"Living_Animate_Entity": ["animal", "person"],
              "Natural_Object": ["body", "plant", "object", "food", "location", "substance"],
              "Manufactured_Object": ["artifact", "food", "location", "substance"],
              "Informational_Object": ["cognition", "communication", "possession"],
              "Dynamic_situation": ["act", "event", "process"],
              "Stative_situation": ["attribute", "state", "feeling", "relation"],
              }

supersenses = {}
for synset in list(wn.all_synsets('n')):
    current = set()
    s = synset.lexname().replace("noun.", "")
    for g in gigasenses:
        if s in gigasenses[g]:
            current.add(g)
    # for lemma in synset.lemma_names('fra'):
    french = synset.lemma_names('fra')
    for lemma in french:
        lemma = lemma.lower()
        if lemma not in supersenses:
            supersenses[lemma] = set()
        supersenses[lemma] = supersenses[lemma].union(current)

# for corpus in os.listdir("../../frWaC/moses/"):
#     print(corpus)
#     for line in io.open(os.path.join("../../frWaC/moses/", corpus), 'r', encoding="utf8"):
#         for word in line.split():
#             word = word.split("|")
#             if len(word) > 2 and word[1] in nouns and word[2] == "NOM":
#                 nouns[word[1]] += 1


# for key, value in sorted(nouns.items(), key=itemgetter(1), reverse=True):
#     if value < 1000:
#         continue
#     file.write(key)
#     # print(value)
#     for s in supersenses[key]:
#         file.write("\t" + s)
#     file.write("\n")

nouns = {}
for lemma in supersenses:
    if not lemma.isalpha():
        continue
    if len(supersenses[lemma]) == 1:
        for s in supersenses[lemma]:
            if s not in nouns:
                nouns[s] = set()
            nouns[s].add(lemma)

for s in nouns:
    # file = io.open("noun." + s, "w", encoding='utf8')
    # for n in nouns[s]:
    #     file.write(n.lower() + '\n')
    others = []
    for s2 in nouns:
        if s2 == s:
            continue
        for n in nouns[s2]:
            others.append(n)

    file = io.open("not_seeds." + s, "w", encoding='utf8')
    for n in others:
        file.write(n.lower() + '\n')
