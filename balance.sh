#!/usr/bin/env bash

DIR_SEED="data/seeds/seeds-super-supersenses"
INPUT_DIR="data/frWaC/mcf/"
OUTPUT_DIR_BASE="data/frWaC/mcf_"

for filename in $DIR_SEED/seeds*; do
    if [[ $filename != *".txt" ]]; then
        f="$(basename -- $filename)"
        SEED1=$DIR_SEED"/"$f
        SEED2=$DIR_SEED"/not_"$f
        OUTPUT_DIR=$OUTPUT_DIR_BASE$f

        echo $f
        rm -r $OUTPUT_DIR
        mkdir -p $OUTPUT_DIR
        python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR
    fi
done

#SEED1="data/seeds/supersenses/noun.act"
#SEED2="data/seeds/supersenses/not_noun.act"
#INPUT_DIR="data/frWaC/mcf/"
#OUTPUT_DIR="data/frWaC/mcf_noun.act"
#
#echo "noun.act"
#
#rm -r $OUTPUT_DIR
#mkdir -p $OUTPUT_DIR
#python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR


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

#SEED1="data/seeds/supersenses/noun.act"
#SEED2="data/seeds/supersenses/not_noun.act"
#INPUT_DIR="data/frWaC/mcf/"
#OUTPUT_DIR="data/frWaC/mcf_act/"
#
#echo "Act"
#
#rm -r $OUTPUT_DIR
#mkdir -p $OUTPUT_DIR
#python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR
#
#SEED1="data/seeds/supersenses/noun.event"
#SEED2="data/seeds/supersenses/not_noun.event"
#INPUT_DIR="data/frWaC/mcf/"
#OUTPUT_DIR="data/frWaC/mcf_event/"
#
#echo "Event"
#
#rm -r $OUTPUT_DIR
#mkdir -p $OUTPUT_DIR
#python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR
