#!/usr/bin/env bash

mkdir tmp
python3 src/identify.py $1 tmp/
mv tmp/* $1
rm -r tmp