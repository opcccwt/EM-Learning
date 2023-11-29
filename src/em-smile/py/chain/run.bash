#!/bin/bash

# number of nodes in chain
n=100
# size of dataset is 2^logN
logN=5
# number of states
k=10

# number of instances
#cases=5 # edit below

for seed in {1..5}; do
    dirname="nets/$(printf %03d $seed)"
    mkdir -p $dirname
    python3 make_chain.py $n $logN $k $seed
    mv chain*.net chain*.uai chain*.train $dirname
done
