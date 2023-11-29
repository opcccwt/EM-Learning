This is an implementation of EM learning directly on an arthimetic circuit.
# Usage
If you already have the ac, lmap and pmap file, create an AC by
```
ac = AC(ac, lmap, log)
ac.loadPmap(pmap)
```
where `log` is a boolean that should be set to true if you have a large model and want to run EM learning in log mode to prevent underflow. 
Run EM learning by
```
log, logs = ac.EM(dat, constant, maxit, threshold, batch_size, conv, smooth)
```
`dat` is the location of the data file. `constant` is a list of the parameters that you do not want to update during training. Add x$0 to the list to indicate that P(x0) is fixed and add y$0$z$0$k$0 to indicate P(y0 | z0, k0) is fixed. `conv` is the class to load data
and you will need to provide a dictionary that maps the name of the states to the indices of the states to `conv`. The reason is that we use ACE to compile a Bayesian network into an arthimetic circuit and ACE will use the indices of the states as the names.
For instance, if there are three states in the BN state0, state1 and state2. Then create a converter by
```
d = dict()
d["state0"] = 0
d["state1"] = 1
d["state2"] = 2
conv = converter()
conv.setConvert(d)
```
This function will return the final log likelihood in `log` and the log likelihoods in each iteration in `logs`. After learning, you can save the new circuit by
```
ac.save(new_lmap)
```
where `new_lmap` is the location to store the new lmap file.

Suppose you have the Bayeisan network(.net file) but not the circuit, then do
```
netToAc(net, var)
```
where `net` is the location of the net file and var is the name of the variables that are subject to change. There will be two dummy files generated and you can delete them.

