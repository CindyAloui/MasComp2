#!/usr/bin/env bash

#SEED1="data/seeds/countability/COMPTABLES-200.txt"
#SEED2="data/seeds/countability/MASSIFS-200.txt"
#INPUT_DIR="data/frWaC/mcf/"
#OUTPUT_DIR="data/frWaC/mcf_countability/"
#
#echo "Countability"
#
#rm -r $OUTPUT_DIR
#mkdir -p $OUTPUT_DIR
#python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR
#
#
#SEED1="data/seeds/animacy/200-ANIM.txt"
#SEED2="data/seeds/animacy/200-INANIM.txt"
#INPUT_DIR="data/frWaC/mcf/"
#OUTPUT_DIR="data/frWaC/mcf_animacy/"
#
#echo "Animacy"
#
#rm -r $OUTPUT_DIR
#mkdir -p $OUTPUT_DIR
#python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR
#

SEED1="data/seeds/supersenses/noun.act"
SEED2="data/seeds/supersenses/not_noun.act"
INPUT_DIR="data/frWaC/mcf/"
OUTPUT_DIR="data/frWaC/mcf_act/"

echo "Act"

rm -r $OUTPUT_DIR
mkdir -p $OUTPUT_DIR
python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR

SEED1="data/seeds/supersenses/noun.event"
SEED2="data/seeds/supersenses/not_noun.event"
INPUT_DIR="data/frWaC/mcf/"
OUTPUT_DIR="data/frWaC/mcf_event/"

echo "Event"

rm -r $OUTPUT_DIR
mkdir -p $OUTPUT_DIR
python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR
