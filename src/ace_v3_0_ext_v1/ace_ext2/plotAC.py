import networkx as nx
import graphviz
import sys

def plotAC(lmap_file,ac_file):
    # Depending on the format of AC, may modify the following map
    LIT = "L" # literal
    AND = "A" # AND gate
    OR =  "O" # OR gate
    # maps each id to the value / either parameter or indicator
    map_dict = dict()
    # first parse the lmap_file and record the indicators
    with open(lmap_file,"r") as f:
        lines = f.readlines()
        for l in lines:
            words = l.strip().split("$")
            if words[0] == "cc":
                # indicator
                if words[1] == "I":
                    map_dict[words[2]] = words[-2]+"_"+words[-1]
                # parameter
                if words[1] == "C":
                    map_dict[words[2]] = words[3]
                    
    # construct the AC now
    # map each line id to a node
    fname = ac_file+".plot"
    AC = graphviz.Graph("AC", filename=fname)
    line_map = dict()
    with open(ac_file,"r") as f:
        lines = f.readlines()
        #print(lines)
        for i,l in enumerate(lines[1:]):
            words = l.strip().split(" ")
            # if literal
            if words[0] == LIT:
                #print(words[1],map_dict[words[1]])
                AC.node(name=str(i), label=map_dict[words[1]])
            # depending on the format of AC, may replace "O" by "+" below
            if words[0] == OR:
                AC.node(name=str(i), label="+")
                for j in words[3:]:
                    AC.edge(str(i),j)
            # depending on the format of AC, may replace "A" by "*" below
            if words[0] == AND:
                AC.node(name=str(i), label="*")
                for j in words[2:]:
                    AC.edge(str(i),j)
    AC.render(fname, view=False)

def main():
    args = sys.argv[1:]
    assert (len(args) == 2) # exactly two arguments
    lmap_file,ac_file = args[0], args[1]
    plotAC(lmap_file, ac_file)
    
if __name__ == "__main__":
    main()
