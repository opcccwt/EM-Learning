#!/bin/bash

n=64
N=10
k=3
seed=1

#cd py/chain
#python3 make_chain.py $n $N $k $seed
#cd ../..

data="py/chain/chain-$n-$N.train"
seed="py/chain/chain-$n.seed.net"
/usr/bin/time build/learn $data $seed $n $N $k $seed
