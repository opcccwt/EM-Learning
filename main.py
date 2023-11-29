from AC_v1.AC import AC
from AC_v1.utility import converter
from AC_v1.utility import netToAc

net = "Example/10.net"

# Compile a BN to an AC.
netToAc(net, [f"node{str(i)}" for i in range(5)])

# Load AC
log = True
ac = AC("Example/10.net.ac", "Example/10.net.lmap", log)
ac.loadPmap("Example/10.net.pmap")

# Create converter
c = converter()
d = dict()
d["state0"] = 0
d["state1"] = 1
c.setConvert(d)

# Run EM learning
dat = "Example/10.dat"
constant = []
maxit = 10
threshold = 1e-3
batch_size = 1024

ac.EM(dat, constant, maxit, threshold, batch_size, c = c)

# Save the new lmap
ac.save("Example/new10.net.lmap")
