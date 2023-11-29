#!/bin/bash

n=100
#N=10
k=10
seed=1

for N in $(seq 12 12); do
    echo "%%% $N"
    cd py/chain
    python3 make_chain.py $n $N $k $seed
    cd ../..

    data="py/chain/chain-$n-$N.train"
    net="py/chain/chain-$n.seed.net"
    /usr/bin/time build/learn $data $net $n $N $k $seed
done
