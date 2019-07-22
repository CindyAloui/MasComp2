#!/usr/bin/env bash

SEED1="data/seeds/countability/COMPTABLES-200.txt"
SEED2="data/seeds/countability/MASSIFS-200.txt"
INPUT_DIR="data/frWaC/little_frWaC_countability/"
OUTPUT_DIR="data/frWaC/little_frWaC_countability/"

mkdir -p $OUTPUT_DIR
python3 src/balance.py $SEED1 $SEED2 $INPUT_DIR $OUTPUT_DIR