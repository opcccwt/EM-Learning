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

def netToAc(net, var):
    os.chdir("src/")
    os.system("java -cp .:inflib.jar ace_v3_0_ext_v1/ace_ext2/Ace_Ext " + net + " " + " ".join(var))
    os.chdir("../")

        
