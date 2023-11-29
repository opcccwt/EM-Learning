== ACE Extension for Training  v1.1 ==

Components:
  * ace_ext.java
    contains the main class "Ace_Ext", which includes the following methods:
    	  - constructor Ace_Ext
	    We first parse the network file and then generate an lmap file.
	    We construct a one-to-one correspondance between the CPT values and
	    the weights in the lmap file.
	    This requires the execution of compile from ACE
	    
	     parameters:
	        String net_file: the file location for the .NET network file
		String[] variables: a list of variable names whose CPTs may vary during training
	    	 		
          - updated_CPTs
	    We update the CPT values for the variables, this happens when we want to
	    update the parameters during the training
	    The function will create a new lmap file without recompiling the AC

             parameters:
	        Map<String,List<Double>> params: maps each variable name to a flattened CPT (1D-List)

          - evaluate
	    We run marginal queries on variables after asserting evidence
	    This requires the execution of evaluate from ACE

 	     parameters:
	        List<String>query_nodes: a set of query nodes 
		Map<String,String>evidence: maps each variable to a value of that variable,
		                            meaning asserting evidence on the variable
             return:
		Map<String,List<Double>>: maps each variable name to a probability vector for each value
		                                              (1D-list of probability distribution)
          - generate_pmap
	     we create a .pmap file that maps each line number (in .lmap) to a CPT instantiation
	     the procedure creates the required file
							      
  * variable.java
     contains class Variable which includes the following attributes:
        - name
	- parents
	- values
	- isVariable
	- factors (CPTs)

  * factor.java
     contains class Factor which includes the following attributes:
        - var (child)
	- parents
	- instantiation (values for parents and child)
	- value (numeric probability for the instantiation)
	- lmap  (lmap string associated with the factor)
	- is_fixed (whether the value can be varied)

  * utils.java
     contains class Utils which includes the helper functions


Notes on the formats of lmap and AC
  - lmap
     e.g., cc$T$m24541$196  represents the 196th value of variable m24541
  - AC
     - literal: (L 15826)  represents the literal corresponding to line 15826 in the .lmap file
     - AND gate (A n T1 ... Tn) where n represents the number of arguments and T1,...,Tn are the
         line number of the arguments
     - OR gate (O xx n T1 ... Tn) where xx can be ignored and T1 ... Tn represent the line number
        of the arguments	
