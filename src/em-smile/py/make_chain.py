#!/usr/bin/env python

import sys
import pybn.net as net

from collections import defaultdict

def bit_string(num,n):
    bits = []
    for pos in xrange(n):
        bit = num % 2
        num = num / 2
        bits.append(str(bit))
    return "".join(bits)

if len(sys.argv) != 3:
    print ("usage: %s [n] [log2 N]" % sys.argv[0])
    exit(1)

n = int(sys.argv[1])
logN = int(sys.argv[2])
N = 2**logN

print (n,N)

net_type = "BAYES"
var_sizes = [2]*n
pot_domains = [[0]] + [ [var-1,var] for var in xrange(1,n) ]
pot0 = [ '0.5', '0.5' ]
pot = [ '0.9', '0.1', '0.1', '0.9' ]
pots =  [ pot0 ] + [ pot ]*(n-1)

bn = net.Network(net_type,var_sizes,pot_domains,pots)

f = open('chain-%d.net' % n,'w')
f.write(bn.hugin_net())
f.close()

names = [ 'x%d' % var for var in xrange(n) ]
dataset = []
for i in xrange(N):
    st = bit_string(i,n)
    st = [ "s"+bit for bit in st ]
    #st = [ state if i % 2 == 0 else "*" for i,state in enumerate(st) ]
    dataset.append(tuple(st))

# write smile dataset
f = open('chain-%d-%d.smile.train' % (n,logN),'w')
f.write(','.join(names))
f.write('\n')
for instance in dataset:
    f.write(",".join(instance))
    f.write("\n")
f.close()

D = defaultdict(lambda: 0)
for instance in dataset:
    D[instance] += 1

# write hugin dataset
f = open('chain-%d-%d.hugin.train' % (n,logN),'w')
f.write('#\t')
f.write('\t'.join(names))
f.write('\n')
for instance in D:
    f.write("%d\t" % D[instance])
    f.write("\t".join(instance))
    f.write("\n")
f.close()
