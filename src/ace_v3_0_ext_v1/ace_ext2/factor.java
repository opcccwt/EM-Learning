package ace_v3_0_ext_v1.ace_ext2;

import java.util.*;

class Factor {
    // variable for the CPT
    private Variable f_var;
    // parents for the variable
    private List<Variable> f_parents;
    // value combination for parents and child
    private List<String> f_inst;
    // numerical value for the inst
    private Double f_value;
    // dummy numerical value for the inst
    private Double f_dummy_value;
    // associated words in the lmap - this is just a template
    // need to replace with the required value
    // specific prob value was replaced with "@"
    private String f_lmap;
    // whether or not the entry is functional
    private boolean is_fixed;

    // constructor
    public Factor(Variable var, List<Variable> parents, boolean fixed){
	f_var = var;
	f_parents = parents;
	f_inst = new ArrayList<String>();
	is_fixed = fixed;
    }

    // modify the lmap string to adjust for the new f_value
    // if dummy = true, then modify the f_dummy_lmap instead
    private void modify_lmap(boolean dummy){
	
    }

    // display the factor
    public void display(){
	System.out.println(f_inst + ": " + f_value + ' ' + f_dummy_value);
    }
    // setters
    public void set_value(Double val){
	f_value = val;
	modify_lmap(false);
    }
    public void set_dummy_value(Double val){
	f_dummy_value = val;
	modify_lmap(true);
    }
    public void set_lmap(String s){
	f_lmap = s;
    }
    public void add_inst(String s){
	f_inst.add(s);
    }
    // getters
    public Double get_value(){
	return f_value;
    }
    public Double get_dummy_value(){
	return f_dummy_value;
    }
    public String get_lmap(){
	String lmap = f_lmap.replace("@",String.valueOf(f_value));
	return lmap;
    }
    public String get_dummy_lmap(){
	String dummy_lmap = f_lmap.replace("@",String.valueOf(f_dummy_value));
	return dummy_lmap;
    }
    public List<String> get_inst(){
	return f_inst;
    }
    public boolean isfixed(){
	return is_fixed;
    }
    public List<String> get_variable_names(){
	List<String>all_vars = new ArrayList<String>();
	for (Variable p : f_parents)
	    all_vars.add(p.get_name());
	all_vars.add(f_var.get_name());
	return all_vars;
    }
    public List<Integer> get_inst_index(){
	List<Integer>inst_index = new ArrayList<Integer>();
	for (int i = 0; i < f_inst.size()-1; i ++){
	    String par_value = f_inst.get(i);
	    List<String> vals = f_parents.get(i).get_values();
	    int j = 0;
	    for (j = 0; j < vals.size(); j ++)
		if (par_value.equals(vals.get(j)))
		    break;
	    inst_index.add(j);	    
	}
	String chi_value = f_inst.get(f_inst.size()-1);
	List<String> vals = f_var.get_values();	
	int j = 0;
	for (j = 0; j < vals.size(); j ++)
	    if (chi_value.equals(vals.get(j)))
		break;
	inst_index.add(j);
	return inst_index;
    }
}
