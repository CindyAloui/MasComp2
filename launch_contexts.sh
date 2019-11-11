#!/usr/bin/env bash


for filename in contexts_launchers/launchForCluster-*; do
    echo $filename
    sbatch $filename
done