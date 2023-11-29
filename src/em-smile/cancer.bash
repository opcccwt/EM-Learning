#!/bin/bash

n=64
N=10
k=3
seed=1

data="/mnt/d/academic/Master/UCLA/CapstoneProject/Harmonization/POP909-Dataset-master/POP909_Hugin_Summary/HuginSummary.dat"
seed="/mnt/d/academic/Master/UCLA/CapstoneProject/Harmonization/sample.net"
/usr/bin/time build/learn $data $seed $n $N $k $seed