#!/bin/bash

n=4
N=10
k=3
seed=0

cd py
python make_wedge.py $n $N $k $seed
cd ..

data="py/wedge-$n-$N.smile.train"
data_a="py/wedge-$n-$N.simple-a.smile.train"
data_b="py/wedge-$n-$N.simple-b.smile.train"
data_c="py/wedge-$n-$N.simple-c.smile.train"
net="py/wedge-$n.net"
net_a="py/wedge-$n.simple-a.net"
net_b="py/wedge-$n.simple-b.net"
build/learn $data $data_a $data_b $data_c $net $net_a $net_b $n $N
