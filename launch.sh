#!/usr/bin/env bash


for filename in launchForCluster-*; do
    sbatch $filename
done