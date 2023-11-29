import math
import numpy as np

# For float comparsion
TOLERANCE = 0.0000000000001
NEGINF = float("-inf")

class Node:
    id = 0
    def __init__(self):
        self.children = []
        self.parents = []
        self.value = None
        self.dr = None
        #self.bit = 0
        self.bit = [0]
        self.id = Node.id
        self.log = False
        Node.id += 1
    
    def addChild(self, child):
        self.children.append(child)
    
    def addParent(self, parent):
        self.parents.append(parent)
        
    def setValue(self, value):
        if (not self.log):
            self.value = value
            self.bit = (value <= TOLERANCE)
            # if (value <= TOLERANCE):
            #     self.bit = 1
            # else:
            #     self.bit = 0
        else:
            self.value = np.log(value)
            self.bit = (value <= TOLERANCE)
            # if (value == 0):
            #     self.value = NEGINF
            #     self.bit = 1
            # else:
            #     self.value = math.log(value)
            #     self.bit = 0
    
    def setBit(self, bit):
        self.bit = bit
        
    def setDr(self, dr):
        if (not self.log):
            self.dr = dr
        else:
            # if (dr == 0):
            #     self.dr = NEGINF
            # else:
            #     self.dr = math.log(dr)
            self.dr = np.log(dr)
        
    def getValue(self):
        return self.value
    
    def getBit(self):
        return self.bit
    
    def getDr(self):
        return self.dr

    # Evalute the value of node.
    def evaluateValue(self):
        pass
    
    # Evaluate the partial derivative
    def evaluateDr(self):
        if (not self.log):
            self.evaluateDrNormal()
        else:
            self.evaluateDrLog()
            
    def evaluateDrNormal(self):
        #self.setDr(0.0)
        self.setDr(np.array(0.0))
        # for p in self.parents:
        #     if (isinstance(p, addGate)):
        #         self.dr += p.dr
        #     elif (p.getValue() != 0):
        #         if (p.getBit() == 0):
        #             self.dr += p.getValue() * p.getDr() / self.value
        #         elif (self.value == 0 or self.bit == 1):
        #             self.dr += p.getValue() * p.getDr()
        
        # Doing all the calculations above in numpy array.
        addGates = np.array([isinstance(p, addGate) for p in self.parents])
        n = len(self.parents)
        bits = np.array([p.getBit() for p in self.parents])
        drs = np.array([p.getDr() for p in self.parents])
        values = np.array([p.getValue() for p in self.parents])
        mulGates = np.logical_and(np.logical_not(addGates).reshape(n, -1), abs(values) > TOLERANCE)
        
        zero = np.logical_or(abs(values) <= TOLERANCE,
                             np.logical_and(np.logical_and(self.value != 0, self.bit == 0),
                                            bits == 1))
        
        
        drs[mulGates] = drs[mulGates] * values[mulGates]
        mulGates = mulGates.reshape(n, -1)
        drs[np.logical_and(mulGates, bits == 0, np.logical_not(zero))] = \
        drs[np.logical_and(mulGates, bits == 0, np.logical_not(zero))] / \
        np.tile(self.value, (n, 1))[np.logical_and(mulGates, bits == 0, np.logical_not(zero))]
        drs[zero] = 0

        
        self.dr = self.dr + drs.sum(axis = 0)
        
                    
    def evaluateDrLog(self):
        #self.setDr(0.0)
        self.setDr(np.array(0.0))
        # for p in self.parents:
        #     if (isinstance(p, addGate)):
        #         self.dr = logAdd(self.dr, p.dr)
        #     elif (p.getValue() != NEGINF):
        #         if (p.getBit() == 0):
        #             self.dr = logAdd(self.dr, p.getValue() + p.getDr() - self.value)
        #         elif (self.value == NEGINF or self.bit == 1):
        #             self.dr = logAdd(self.dr, p.getValue() + p.getDr())
        
        # Doing all the calculations above in numpy array.
        addGates = np.array([isinstance(p, addGate) for p in self.parents])
        
        bits = np.array([p.getBit() for p in self.parents])
        drs = np.array([p.getDr() for p in self.parents])
        values = np.array([p.getValue() for p in self.parents])
        n = len(self.parents)
        
        mulGates = np.logical_and(np.logical_not(addGates).reshape(n, -1), values != np.NINF)
        
        zero = np.logical_or(values == np.NINF,
                             np.logical_and(np.logical_and(self.value != np.NINF, self.bit == 0),
                                            bits == 1))
        
        
        drs[mulGates] = drs[mulGates] + values[mulGates]
        mulGates = mulGates.reshape(n, -1)
        drs[np.logical_and(mulGates, bits == 0, np.logical_not(zero))] = \
        drs[np.logical_and(mulGates, bits == 0, np.logical_not(zero))] - \
        np.tile(self.value, (n, 1))[np.logical_and(mulGates, bits == 0, np.logical_not(zero))]

        drs[zero] = np.NINF
        
        self.dr = np.logaddexp(self.dr, np.logaddexp.reduce(drs, axis = 0))
    
    # clean the node.
    def clean(self):
        pass
    
    def __hash__(self):
        return self.id  
        
class Variable(Node):
    def __init__(self, value, log = False):
        super().__init__()
        self.log = log
        if (log):
            # if (value == 0):
            #     self.value = NEGINF
            #     self.bit = 1
            # else:
            #     self.value = math.log(value)
            self.backup = value
            self.value = np.log(value)
            self.bit = (value <= TOLERANCE)
        else:
            # self.value = value
            # if (self.value <= TOLERANCE):
            #     self.bit = 1
            self.backup = value
            self.value = value
            self.bit = (value <= TOLERANCE)
    
    def clean(self):
        pass

    
        
class Parameter(Variable):

        
    # CPT is a string of the form "name$index$name$index$..." where the first name
    # and index are the ones of the child and the others are the ones of the parents.
    def setCPT(self, CPT):
        self.CPT = CPT
    
    def getCPT(self):
        return self.CPT
        
    def clean(self):
        self.dr = None
        
    def setValue(self, value):
        if (not self.log):
            self.value = value
            self.bit = (value <= TOLERANCE)
            # if (value <= TOLERANCE):
            #     self.bit = 1
            # else:
            #     self.bit = 0
            if (not isinstance(self.value, float)):
                self.backup = self.value[0]
            else:
                self.backup = self.value
        else:
            self.value = np.log(value)
            self.bit = (value <= TOLERANCE)
            # if (value == 0):
            #     self.value = NEGINF
            #     self.bit = 1
            # else:
            #     self.value = math.log(value)
            #     self.bit = 0
            if (not isinstance(self.value, float)):
                self.backup = np.exp(self.value[0])
            else:
                self.backup = np.exp(self.value)

        
class Indicator(Variable):
    
    # inst is what this indicator represents.
    # inst[0] is the name of the variable and inst[1] is the index of its state.
    def setInst(self, inst):
        self.inst = inst
        
    def getInst(self):
        return self.inst
    
    def clean(self):
        self.dr = None
        self.value = [1]
        

class Gate(Node):
    def __init__(self, log = False):
        super().__init__()
        self.bit = None
        self.log = log

class addGate(Gate):
    # Evaluate the value of an addGate.
    def evaluateValue(self):
        if (not self.log):
            self.evaluateValueNormal()
        else:
            self.evaluateValueLog()
            
    def evaluateValueNormal(self):
        #self.value = 0.0
        self.value = np.array(0.0)
        
        # for c in self.children:
        #     if (c.bit == 0):
        #         self.value += c.value
        bits = np.array([c.getBit() for c in self.children])
        values = np.array([c.getValue() for c in self.children])
        self.value = self.value + ((bits == 0) * values).sum(axis = 0)
        
        # if (self.value <= TOLERANCE):
        #     self.bit = 1
        # else:
        #     self.bit = 0
        
        self.bit = (self.value <= TOLERANCE)
            
    # The only difference is how to add two values.      
    def evaluateValueLog(self):
        #self.value = NEGINF
        self.value = np.array(NEGINF)
        
        # for c in self.children:
        #     if (c.bit == 0):
        #         self.value = logAdd(self.value, c.value)
        bits = np.array([c.getBit() for c in self.children])
        values = np.array([c.getValue() for c in self.children])
        values[bits == 1] = np.NINF
        
        self.value = np.logaddexp.reduce(np.logaddexp(self.value, values), axis = 0)       
                
        # if (self.value == NEGINF):
        #     self.bit = 1
        # else:
        #     self.bit = 0
        self.bit = np.isneginf(self.value)
        
    def clean(self):
        self.value = None
        self.dr = None
        self.bit = np.array(1)
            
                

class mulGate(Gate):
    
    # Evaluate the value of a mulGate
    def evaluateValue(self):
        if (not self.log):
            self.evaluateValueNormal()
        else:
            self.evaluateValueLog()
                
    def evaluateValueNormal(self):
        #self.value = 1.0
        self.value = np.array(1.0)
        
        # zero_count = 0
        # # bit will be used for evluating partial derivative.
        # for c in self.children:
        #     if (c.bit == 1 or c.value <= TOLERANCE):
        #         zero_count += 1
        #     else:
        #         self.value *= c.value
        
        bits = np.array([c.bit for c in self.children])
        values = np.array([c.value for c in self.children])
        zero_count = np.logical_or(bits == 1, values <= TOLERANCE).sum(axis = 0)

        values[bits == 1] = 1
        self.value = self.value * values.prod(axis = 0)
        
        # if (zero_count == 1):
        #     self.bit = 1
        # else:
        #     self.bit = 0
        #     if (zero_count > 1):
        #         self.value = 0.0
        self.bit = (zero_count == 1)
        self.value = (self.value * (zero_count <= 1))
                
    # Multiplication is add in log space.
    def evaluateValueLog(self):
        #self.value = 0.0
        self.value = np.array(0.0)
        
        # neginf_count = 0
        # for c in self.children:
        #     if (c.bit == 1 or c.value == NEGINF):
        #         neginf_count += 1
        #     else:
        #         self.value += c.value
        
        bits = np.array([c.bit for c in self.children])
        values = np.array([c.value for c in self.children])
        neginf_count = np.logical_or(bits == 1, np.isneginf(values)).sum(axis = 0)
        values[bits == 1] = 0
        self.value = self.value + values.sum(axis = 0)
        
        # if (neginf_count == 1):
        #     self.bit = 1
        # else:
        #     self.bit = 0
        #     if (neginf_count > 1):
        #         self.value = NEGINF     
        
        self.bit = (neginf_count == 1)
        self.value[neginf_count > 1] =  np.NINF
        
        
    def clean(self):
        self.value = None
        self.dr = None
        self.bit = None

if __name__ == "__main__":
    log = True
    p1 = Parameter(np.array([3, 3]), log)
    p2 = Parameter(np.array([4, 4]), log)
    I1 = Indicator(np.array([1, 0]), log)
    I2 = Indicator(np.array([0, 1]), log)
    p1.setValue(np.array([3, 3]))
    p2.setValue(np.array([4, 4]))
    
    g1 = addGate(log)
    g2 = mulGate(log)
    g3 = addGate(log)
    g4 = mulGate(log)
    g5 = addGate(log)
    g6 = mulGate(log)
    
    p1.addParent(g1)
    I1.addParent(g1)
    I1.addParent(g2)
    p2.addParent(g2)
    p2.addParent(g3)
    I2.addParent(g3)
    g1.addParent(g4)
    g2.addParent(g4)
    g2.addParent(g5)
    g3.addParent(g5)
    g4.addParent(g6)
    g5.addParent(g6)
    
    g6.addChild(g4)
    g6.addChild(g5)
    g4.addChild(g1)
    g4.addChild(g2)
    g5.addChild(g2)
    g5.addChild(g3)
    g1.addChild(p1)
    g1.addChild(I1)
    g2.addChild(I1)
    g2.addChild(p2)
    g3.addChild(p2)
    g3.addChild(I2)
    
    g1.evaluateValue()
    g2.evaluateValue()
    g3.evaluateValue()
    g4.evaluateValue()
    g5.evaluateValue()
    g6.evaluateValue()
    
    g6.setDr(np.array([1, 1]))
    g5.evaluateDr()
    g4.evaluateDr()
    g3.evaluateDr()
    g2.evaluateDr()
    g1.evaluateDr()
    p1.evaluateDr()
    I1.evaluateDr()
    p2.evaluateDr()
    I2.evaluateDr()
    
    print(p1.value)
    print(p1.bit)
    print(I1.value)
    print(I1.bit)
    print(p2.value)
    print(p2.bit)
    print(I2.value)
    print(I2.bit)
    print(g1.value)
    print(g1.bit)
    print(g2.value)
    print(g2.bit)
    print(g3.value)
    print(g3.bit)
    print(g4.value)
    print(g4.bit)
    print(g5.value)
    print(g5.bit)
    print(g6.value)
    print(g6.bit)
    
    print(p1.dr)
    print(I1.dr)
    print(p2.dr)
    print(I2.dr)
    print(g1.dr)
    print(g2.dr)
    print(g3.dr)
    print(g4.dr)
    print(g5.dr)
    print(g6.dr)
    
    
    