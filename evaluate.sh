#!/usr/bin/env bash

#python3 evaluate.py animacy data/lexicons/animacy/nomsSequoia.txt data/test_corpus/animacy/tree_tagged
python3 evaluate.py countability data/lexicons/countability-small/ANNOTATED_NOUNS.txt data/test_corpus/countability/class_annot/
#python3 evaluate.py countability-mask40 data/lexicons/countability-2/ANNOTATED_NOUNS.txt data/test_corpus/countability/class_annot/
#python3 evaluate.py countability-3 data/lexicons/countability-3/ANNOTATED_NOUNS.txt data/test_corpus/countability/class_annot/
#python3 evaluate.py countability-4 data/lexicons/countability-4/ANNOTATED_NOUNS.txt data/test_corpus/countability/class_annot/
#python3 evaluate.py countability-5 data/lexicons/countability-5/ANNOTATED_NOUNS.txt data/test_corpus/countability/class_annot/