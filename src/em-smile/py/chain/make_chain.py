 #!/usr/bin/env python

import sys
import random
import pybn.net as net

from collections import defaultdict

def save_khaled_data(filename,dataset):
    f = open(filename,'w')
    for instance in dataset:
        instance = [ '-1' if val == '*' else val[1:] for val in instance ]
        f.write(",".join(instance))
        f.write("\n")
    f.close()

def save_smile_data(filename,names,dataset):
    f = open(filename,'w')
    f.write(','.join(names))
    f.write('\n')
    for instance in dataset:
        f.write(",".join(instance))
        f.write("\n")
    f.close()

def save_samiam_data(filename,names,dataset):
    f = open(filename,'w')
    f.write(','.join(names))
    f.write('\n')
    for instance in dataset:
        instance = [ "N/A" if x == "*" else x for x in instance ]
        f.write(",".join(instance))
        f.write("\n")
    f.close()

def save_hugin_data(filename,names,dataset):
    f = open(filename,'w')

    D = defaultdict(lambda: 0)
    for instance in dataset:
        D[instance] += 1

    instances = D.keys()
    instances.sort()

    f.write('#\t')
    f.write('\t'.join(names))
    f.write('\n')
    for instance in instances:
        f.write("%d\t" % D[instance])
        f.write("\t".join(instance))
        f.write("\n")
    f.close()

def random_pr(k,psi=1.0):
    pr = [ random.gammavariate(psi,1) for i in range(k) ]
    #pr = [ -math.log(random.random()) for i in range(k) ]
    pr_sum = sum(pr)
    pr = [ p/pr_sum for p in pr ]
    return pr

def str_random_pr(k,psi=1.0):
    pr = random_pr(k,psi=psi)
    return [ "%f" % p for p in pr ]

def sample(pr):
    q = random.random()
    cur = 0
    for i,p in enumerate(pr):
        cur += p
        if q <= cur:
            return i
    return i

if len(sys.argv) != 5:
    print ("usage: %s [n] [log2 N] [k] [seed]" % sys.argv[0])
    print ("    n: number of nodes")
    print ("    N: dataset size (2^N)")
    print ("    k: # of states")
    print (" seed: random number seed")
    exit(1)

n = int(sys.argv[1])
logN = int(sys.argv[2])
N = 2**logN
k = int(sys.argv[3])
seed = int(sys.argv[4])
random.seed(seed)

print ("parameters:", n,N,k,seed)

net_type = "BAYES"
var_sizes = [k]*(n+1)
pot_domains = [[0]] + \
              [ [var-1,var] for var in range(1,n+1) ]

pot0 = str_random_pr(k)
all_pots = [pot0]
for j in range(n):
    pot = []
    for i in range(k): pot.extend(str_random_pr(k))
    all_pots.append(pot)

bn = net.Network(net_type,var_sizes,pot_domains,all_pots)

#f = open('chain-%d.net' % n,'w')
#f.write(bn.hugin_net())
#f.close()

#f = open('chain-%d.uai' % n,'w')
#f.write(str(bn))
#f.close()

names = [ 'x%d' % var for var in range(n+1) ]

dataset = []
for i in range(N):
    instance = bn.simulate()
    instance = [ "s%d" % x for x in instance ]
    instance = [ x if (j % 2 == 0) else '*' for j,x in enumerate(instance) ]
    dataset.append(instance)

# write smile dataset
filename = 'chain-%d-%d.train' % (n,logN)
save_smile_data(filename,names,dataset)

# write samiam dataset
filename = 'chain-%d-%d.samiam.train' % (n,logN)
save_samiam_data(filename,names,dataset)

# write hugin dataset
#filename = 'chain-%d-%d.hugin.train' % (n,logN)
#save_hugin_data(filename,names,dataset)

# write khaled dataset
filename = 'chain-%d-%d.khaled.train' % (n,logN)
save_khaled_data(filename,dataset)

# NETWORK SEED
net_type = "BAYES"
var_sizes = [k]*(n+1)
pot_domains = [[0]] + \
              [ [var-1,var] for var in range(1,n+1) ]

pot0 = str_random_pr(k)
all_pots = [pot0]
for j in range(n):
    pot = []
    for i in range(k): pot.extend(str_random_pr(k))
    all_pots.append(pot)

bn = net.Network(net_type,var_sizes,pot_domains,all_pots)

f = open('chain-%d.seed.net' % n,'w')
f.write(bn.hugin_net())
f.close()

f = open('chain-%d.seed.uai' % n,'w')
f.write(str(bn))
f.close()
