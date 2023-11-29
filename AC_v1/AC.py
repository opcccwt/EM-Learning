import sys
import os
sys.path.append(os.getcwd() + "/AC_v1")
import numpy as np
from Node import Parameter
from Node import Indicator
from Node import addGate
from Node import mulGate
from Node import TOLERANCE
from Node import NEGINF
from utility import converter

class AC:
    # Create a AC by its ac file and lmap file
    def __init__(self, ac, lmap, log = False):
        self.log = log
        self.levels = None
        self.ac = ac
        self.lmap = lmap
        # Store the line number of the variables for pmap
        self.lineToVariable = dict()
        # Store the value of the variables.
        numToVariable = dict()
        # Store the indicators. 
        self.indicator = dict()
        self.parameter = []
        f = open(lmap)
        for i, line in enumerate(f.readlines()):
            terms = line.strip().split("$")
            if (len(terms) > 1):
                v = None
                # Only extract parameters and indicators from lmap.
                if (terms[1].lower() == "c"):
                    v = Parameter(float(terms[3]), log)
                    self.parameter.append(v)
                elif (terms[1].lower() == "i"):
                    name = terms[-2]
                    index = int(terms[-1])
                    v = Indicator(1.0, log)
                    v.setInst((name, index))
                    if (not name in self.indicator):
                        self.indicator[name] = dict()
                    self.indicator[name][index] = v
                else:
                    continue
                self.lineToVariable[i] = v
                numToVariable[int(terms[2])] = v
                
                
        # Store the parameters, indicators and gates in one list with the order
        # given in the ac file.
        variables = []

        f = open(ac)
        # Skip the line that shows the properties of this AC
        line = f.readline()
        if (line.startswith("cc")):    
            f.readline()
        for i, line in enumerate(f.readlines()):
            terms = line.strip().split(" ")
            if (terms[0].lower() == "l"):
                variables.append(numToVariable[int(terms[1])])
            # A node will know both its parents and its children.
            elif (terms[0] == "*" or terms[0].lower() == "a"):
                g = mulGate(log)
                for j in terms[2:]:
                    g.addChild(variables[int(j)])
                    variables[int(j)].addParent(g)
                variables.append(g)
            elif (terms[0] == "+" or terms[0].lower() == "o"):
                g = addGate(log)
                for j in terms[3:]:
                    g.addChild(variables[int(j)])
                    variables[int(j)].addParent(g)
                variables.append(g)
            else:
                raise Exception("Can not identify the starting letter " + terms[0] +
                                " of line " + str(i + 2) + " in the ac file")
        self.root = variables[-1]
        self.getLevels()
        
    # Get the correspondence btween the CPT and the parameters.
    def loadPmap(self, pmap):
        f = open(pmap)
        self.CPTToVariable = dict()
        for line in f.readlines():
            temp = line.strip().split(" ")
            line = int(temp[0])
            cpt = temp[1].replace("|", "")
            cpt = cpt.replace(",", "")
            cpt = cpt[1:]
            v = self.lineToVariable[line]
            v.setCPT(cpt)
            self.CPTToVariable[cpt] = v
        
    # Run EM learning with data from the file dat. Parameters that are fixed are
    # specified in the constant.
    def EM(self, dat, constant, maxit, threshold, batch_size, c = converter(), smooth = 1.0):
 
        cases = c.loadHugin(dat)
        
        # A dictionary for what are fixed.
        fixed = dict()
        count = dict()
        
        # Intialize fixed and count. Keys are the parents and values are
        # the children.
        for inst in self.CPTToVariable.keys():
            terms = inst.split("$")
            key = "$".join(terms[2:])
            if (not key in fixed):
                fixed[key] = dict()
            if (not terms[0] in fixed[key]):
                fixed[key][terms[0]] = dict()
            fixed[key][terms[0]][terms[1]] = False
            if (not key in count):
                count[key] = dict()
            if (not terms[0] in count[key]):
                count[key][terms[0]] = dict()
            count[key][terms[0]][terms[1]] = smooth
        
        # Set some fixed to true according to the given constant.
        for c in constant:
            terms = c.split("$")
            key = "$".join(terms[2:])
            fixed[key][terms[0]][terms[1]] = True
        
        if (not self.log):
            return self.EM_loopNormal(cases, maxit, threshold, batch_size, smooth, fixed, count)
        else:
            return self.EM_loopLog(cases, maxit, threshold, batch_size, smooth, fixed, count)
    
    # EM learning in normal space.
    def EM_loopNormal(self, cases, maxit, threshold, batch_size, smooth, fixed, count):     
        # EM learning
        it = 0
        t = 1
        llog = 0
        llog_old = 0
        llogs = []
        
        while (it < maxit and t > threshold):

            # Clean count
            for v1 in count.values():
                for v2 in v1.values():
                    for k in v2.keys():
                        v2[k] = smooth

            # # Loop through all the cases
            # for i, case in enumerate(cases):
            #     p = self.getMar(case)
            #     if (abs(p) <= TOLERANCE):
            #         continue
            #     llog -= log(p)
            #     self.evaluateDr()
            #     for inst in self.CPTToVariable:
            #         v = self.CPTToVariable[inst]
            #         terms = inst.split("$")
            #         key = "$".join(terms[2:])
            #         count[key][terms[0]][terms[1]] += v.getValue() * v.getDr() / p
            
            i = 0
            n = len(cases)
            while (i < n):
                end = min(i + batch_size, n)
                p = self.getMar(cases[i:end])
                llog += np.log(p).sum()
                self.root.setDr(np.array([1.0] * (end - i)))
                self.evaluateDr()
                for inst in self.CPTToVariable:
                     v = self.CPTToVariable[inst]
                     terms = inst.split("$")
                     key = "$".join(terms[2:])
                     count[key][terms[0]][terms[1]] += (v.getValue() * v.getDr() / p).sum()

                
                i = end

            # Update CPT
            for parents, children in count.items():
                for child, cpt in children.items():
                    s = 0.0
                    d = 1.0
                    for index, prob in cpt.items():
                        inst = child + "$" + index + ("" if parents == "" else "$" + parents)
                        if (fixed[parents][child][index]):
                            d -= self.CPTToVariable[inst].getValue()
                        else:
                            s += prob
                    
                    if (s == 0.0):
                        continue
                    else:
                        for index, prob in cpt.items():
                            inst = child + "$" + index + ("" if parents == "" else "$" + parents)
                            if (not fixed[parents][child][index]):
                                self.CPTToVariable[inst].setValue(prob * d / s)            
            
            # Compute percentage change in log likelihood.
            if (it == 0):
                t = 1
            else:
                t = abs(llog - llog_old) / llog
            #print("iteration " + str(it))
            #print("\t -log likelihood = " + str(llog) + ", percentage change = " + str(t))
            llogs.append(llog)
            llog_old = llog
            llog = 0
            it += 1
            
        for p in self.parameter:
            if (not isinstance(p.value, float)):
                p.value = p.value[0]
                
        return llog_old, llogs
            
    # EM learning in log space.
    def EM_loopLog(self, cases, maxit, threshold, batch_size, smooth, fixed, count):       
        # EM learning    
        it = 0
        t = 1
        llog = 0
        llog_old = 0
        llogs = []
        for v1 in count.values():
                for v2 in v1.values():
                    for k in v2.keys():
                        if (smooth == 0):
                            v2[k] = NEGINF
                        else:
                            v2[k] = np.log(smooth)

                            
        while (it < maxit and t > threshold):
            # Clean count
            for v1 in count.values():
                for v2 in v1.values():
                    for k in v2.keys():
                        if (smooth == 0):
                            v2[k] = NEGINF
                        else:
                            v2[k] = np.log(smooth)
            
            # # Loop through all the cases
            # for i, case in enumerate(cases):
            #     p = self.getMar(case)
            #     if (p == NEGINF):
            #         continue
            #     llog -= p
            #     self.evaluateDr()
            #     for inst in self.CPTToVariable:
            #         v = self.CPTToVariable[inst]
            #         terms = inst.split("$")
            #         key = "$".join(terms[2:])
            #         count[key][terms[0]][terms[1]] = logAdd(count[key][terms[0]][terms[1]], v.getValue() + v.getDr() - p)
            
            i = 0
            n = len(cases)
            while (i < n):
                end = min(i + batch_size, n)
                p = self.getMar(cases[i:end])
                
                llog += p.sum()
                self.root.setDr(np.array([1.0] * (end - i)))
                self.evaluateDr()
                for inst in self.CPTToVariable:
                     v = self.CPTToVariable[inst]
                     terms = inst.split("$")
                     key = "$".join(terms[2:])
                     if (np.logaddexp.reduce(v.getValue() + v.getDr() - p, axis = 0) != np.NINF):
                         pass
                     count[key][terms[0]][terms[1]] = \
                     np.logaddexp(count[key][terms[0]][terms[1]], \
                     np.logaddexp.reduce(v.getValue() + v.getDr() - p, axis = 0))
                
                i = end
                
            # Update CPT
            for parents, children in count.items():
                for child, cpt in children.items():
                    s = np.NINF
                    d = 1.0
                    for index, prob in cpt.items():
                        inst = child + "$" + index + ("" if parents == "" else "$" + parents)
                        if (fixed[parents][child][index]):
                            d -= np.exp(self.CPTToVariable[inst].getValue())
                        else:
                            s = np.logaddexp(s, prob)
                    
                    if (s == NEGINF):
                        continue
                    else:
                        for index, prob in cpt.items():
                            inst = child + "$" + index + ("" if parents == "" else "$" + parents)
                            if (not fixed[parents][child][index]):
                                self.CPTToVariable[inst].setValue(d * np.exp(prob - s))            
            
            # Compute percentage change in log likelihood.
            if (it == 0):
                t = 1
            else:
                t = abs(llog - llog_old) / llog
            #print("iteration " + str(it))
            #print("\t -log likelihood = " + str(llog) + ", percentage change = " + str(t))
            llogs.append(llog)
            llog_old = llog
            llog = 0
            it += 1   
            
        for p in self.parameter:
            if (not isinstance(p.value, float)):
                p.value = p.value[0]
                
        return llog_old, llogs

    # Compute marginals
    def getMar(self, queries):
        #self.cleanIndicator()
        self.setParameters(queries)
        
        # A bottom-up pass to compute the marginal.
        for i in range(len(self.levels) - 1, -1, -1):
            nodes = self.levels[i]
            for n in nodes:
                n.evaluateValue()
            
        return self.root.getValue()
        
    # Compute partial derivative
    def evaluateDr(self):
        #self.root.setDr(1)
        for i in range(1, len(self.levels)):
            nodes = self.levels[i]
            for n in nodes:
                n.evaluateDr()
                
    # Set the indicator given evidence.
    def setParameters(self, evidences):
        n = len(evidences)
        
        indicator_values = dict.fromkeys(self.indicator.keys())
        for key in indicator_values.keys():
            indicator_values[key] = dict()
            for state in self.indicator[key].keys():
                indicator_values[key][state] = []
        
        nodes = set(self.indicator.keys())
        for evidence in evidences:
            appeared = set()
            
            for (name, index) in evidence:
                v = indicator_values[name]
                appeared.add(name)
                for key in v:
                    if (key != index):
                        v[key].append(0.0)
                    else:
                        v[key].append(1.0)
            for name in nodes - appeared:
                v = indicator_values[name]
                for key in v:
                    v[key].append(1.0)
                        
        for key in self.indicator:
            for i in self.indicator[key]:
                self.indicator[key][i].setValue(np.array(indicator_values[key][i]))
                
        for p in self.parameter:
                p.setValue(np.array([p.backup] * n))
        
        # for (name, index) in evidence:
        #     v = self.indicator[name]
        #     for key in v:
        #         if (key != index):
        #             v[key].setValue(0.0)
                    
    # Set all the indicators back to 1.
    def cleanParameters(self):
        for v1 in self.indicator.values():
            for v2 in v1.values():
                v2.setValue(1.0)
                
    # clean up the circuit
    def clean(self):
        visited = set()
        self.root.clean()
        visited.add(self.root)
        
        # Run a top-down pass(BFS) to clean up the circuit
        old = self.root.children
        new = []
        
        while (len(old) > 0):
            for c in old:
                c.clean()
                new += self.getUnvisitedChildren(c, visited)
            old = new.copy()
            new = []
    
    # Return a list of nodes that are the children of the parent and are not visited. 
    def getUnvisitedChildren(self, parent, visited):
        unvisited = []
        for c in parent.children:
            if (not c in visited):
                unvisited.append(c)
        return unvisited
            
    # Return a list of nodes in the list that all of its parents are evaluated.
    def allParentsReady(self, nodes, visited):
        # Only update the vistied after the entire loop so that we can ensure
        # a parent and a child will not be in one level.
        new = []
        ready = []
        for n in nodes:
            r = True
            for p in n.parents:
                if (not p in visited):
                    r = False
                    break
            if (r):
                ready.append(n)
                new.append(n)
        
        visited.update(new)
        return ready
    
    # Compute a list such that list[i] is a list of all the nodes in level i.
    def getLevels(self):
        visited = set()
        visited.add(self.root)
        
        self.levels = []
        old = [self.root]
        new = set()
        while (len(old) > 0):
            self.levels.append(old)
            for n in old:
                new.update(self.getUnvisitedChildren(n, visited))
            old = self.allParentsReady(new, visited)
            new = set()
    
    # Return the names of all the nodes
    def getNames(self):
        return [x for x in self.indicator.keys()]
    
    # Return the number of state for each node.
    def numStatesForEachNode(self):
        return {x:len(self.indicator[x]) for x in self.indicator}
    
    # Save this circuit.
    def save(self, lmapDest):
        writef = open(lmapDest, "w")
        readf = open(self.lmap, "r")
        for i, line in enumerate(readf.readlines()):
            if (i in self.lineToVariable):
                splits = line.split("$")
                splits[3] = str(self.lineToVariable[i].value)
                writef.write("$".join(splits))
            else:
                writef.write(line)
                
    def numOfEdges(self):
        num = 0
        for level in self.levels:
            for node in level:
               num += len(node.children)
        return num
            
        
    