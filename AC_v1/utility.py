import numpy as np
# Convert the value of the state
# to the index of the state.
class converter:
    def __init__(self):
        self.convert = None
    # c should be a dictonary about the conversion.
    def setConvert(self, c):
        self.convert = c
    def loadHugin(self, dat):
        f = open(dat)
        variables = f.readline().strip().split(",")
        if (self.convert is None):
            converter = {"n0": 0, "n1": 1, "n2": 2, "n3": 3, "n4": 4, "n5": 5, "n6": 6, 
                         "n7": 7, "n8": 8, "n9": 9, "n10": 10, "n11": 11, "None": 12, "Cont": 13}
        else:
            converter = self.convert
    
        cases = []
        for line in f.readlines():
            case = []
            values = line.strip().split(",")
            if (len(variables) != len(values)):
                raise Exception("The number of variabies does not match the number of values")
            for i in range(len(values)):
                if (values[i] != "*" and values[i] != "N/A"):
                    case.append((variables[i], converter[values[i]]))
            cases.append(case)
        return cases

        