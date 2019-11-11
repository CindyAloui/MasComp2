#!/usr/bin/env bash


for filename in train_launchers/launchForCluster-*; do
    echo $filename
    sbatch $filename
done