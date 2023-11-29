#!/bin/bash

# number of nodes in chains
n=10
# size of dataset is 2^logN
logN=5
# number of states
k=3

# number of instances
#cases=5 # edit below

for seed in {1..5}; do
    dirname="nets/$(printf %03d $seed)"
    mkdir -p $dirname
    python make_wedge.py $n $logN $k $seed
    mv wedge*.net wedge*.uai wedge*.train $dirname
done
