import edu.ucla.belief.*;
import edu.ucla.belief.inference.JEngineGenerator;
import edu.ucla.belief.inference.JoinTreeInferenceEngineImpl;
import edu.ucla.belief.inference.JoinTreeSettings;
import edu.ucla.belief.inference.map.InitializationMethod;
import edu.ucla.belief.inference.map.MapRunner;
import edu.ucla.belief.inference.map.SearchMethod;
import edu.ucla.belief.io.NetworkIO;
import edu.ucla.util.AbstractStringifier;
import edu.ucla.belief.io.hugin.HuginNode;
import edu.ucla.belief.EOGenerator;
import java.io.*;
import java.util.*;
import javafx.util.Pair;
import edu.ucla.belief.learn.Simulator;
import edu.ucla.belief.learn.LearningData;


public class Utility {
    /*
    An interface to call these functions by command line arguments
     */
    public static void main(String[] args) throws StateNotFoundException, IOException {
        if (args.length > 0)
        {
            if (args[0].equals("generateCase"))
            {
                BeliefNetwork bn = null;
                try{
                    /* Use NetworkIO static method to read network file. */
                    bn = NetworkIO.read( args[1] );
                }catch( Exception e ){
                    System.err.println( "Error, failed to read \"" + args[1] + "\": " + e );
                    return;
                }

                simulate(bn, Integer.parseInt(args[2]), Float.parseFloat(args[3]), args[4]);
            }

        }
        return;
    }

    /*
    Run MAP for bn with evidence1 on mapVariable. If dest is null, then it won't store the result. Otherwise, it will
    store the result in the hugin format.
    */
    public static void MAP(BeliefNetwork bn, List<Pair<String, String>> evidence1, List<String> mapVariable, String dest) {

        /*
        Get evidence and map variables.
        */
        Map<FiniteVariable, Object> evidence = convertEvidence(bn, evidence1);
        Set<Variable> setMAPVariables = convertMapVariables(bn, mapVariable);

        /* Approximate MAP. */

        /* Prune first. */
        BeliefNetwork networkUnpruned = bn;
        Set<Variable> varsUnpruned = setMAPVariables;
        Map<FiniteVariable, Object> evidenceUnpruned = evidence;

        Map<FiniteVariable, Object> oldToNew = new HashMap<>(networkUnpruned.size());
        Map<FiniteVariable, Object> newToOld = new HashMap<>(networkUnpruned.size());
        Set<Variable> queryVarsPruned = new HashSet<>(varsUnpruned.size());
        Map<FiniteVariable, Object> evidencePruned = new HashMap<>(evidenceUnpruned.size());
        BeliefNetwork networkPruned = Prune.prune(networkUnpruned, varsUnpruned, evidenceUnpruned, oldToNew, newToOld, queryVarsPruned, evidencePruned);

        bn = networkPruned;
        setMAPVariables = queryVarsPruned;
        evidence = evidencePruned;

        /* Construct the right kind of inference engine. */
        JEngineGenerator generator = new JEngineGenerator();
        JoinTreeInferenceEngineImpl engine = generator.makeJoinTreeInferenceEngineImpl(bn, new JoinTreeSettings());

        /* Set evidence. */
        setEvidence(bn, evidence);


        /*
        Define the search method, one of:
        HILL (Hill Climbing), TABOO (Taboo Search)
        */
        SearchMethod searchmethod = SearchMethod.TABOO;

        /*
        Define the initialization method, one of:
        RANDOM (Random), MPE (MPE), ML (Maximum Likelihoods), SEQ (Sequential)
        */
        InitializationMethod initializationmethod = InitializationMethod.MPE;

        /* Define a limit on the number of search steps (default 25). */
        int steps = 25;

        /* Construct a MapRunner and run the query. */
        MapRunner maprunner = new MapRunner();
        System.out.println("Start approximate Map");
        MapRunner.MapResult mapresult = maprunner.approximateMap(bn, engine, setMAPVariables, evidence, searchmethod, initializationmethod, steps);
        System.out.println("Approximate Map Done");
        Map instantiation = mapresult.instantiation;
        double score = mapresult.score;

        /* Print the results. */
        System.out.println("Approximate MAP, P(MAP,e)= " + score);
        System.out.println("\t P(MAP|e)= " + (score / engine.probability()));
        VariableImpl.setStringifier(AbstractStringifier.VARIABLE_ID);
        System.out.println("\t instantiation: " + instantiation);

        /* Print timings. */
        System.out.println();
        System.out.println("Initialization time, cpu: " + mapresult.initDurationMillisProfiled + ", elapsed: " + mapresult.initDurationMillisElapsed);
        System.out.println("Search time, cpu: " + mapresult.searchDurationMillisProfiled + ", elapsed: " + mapresult.searchDurationMillisElapsed);
        System.out.println();

        /* Clean up to avoid memory leaks. */
        engine.die();

        /* Store the result */
        if (dest != null) {
            PrintWriter writer = null;
            try {
                writer = new PrintWriter(dest);
            } catch (Exception e) {
                System.out.println("Fail to open the file " + dest);
                return;
            }

            Iterator i = instantiation.keySet().iterator();
            while (i.hasNext()) {
                String v = ((HuginNode) i.next()).getLabel();
                writer.write(v);
                if (i.hasNext()) {
                    writer.write(",");
                }
            }
            writer.write("\n");

            i = instantiation.keySet().iterator();
            while (i.hasNext()) {
                writer.write((String) instantiation.get(i.next()));
                if (i.hasNext()) {
                    writer.write(",");
                }
            }
            writer.close();

        }
        /* Clean up to avoid memory leaks. */
        engine.die();

        return;
    }

    /*
    evidence1 is a file in hugin format which specifies the variables and the values.
    mapVariable is a file that specifies the map variable in the format: v_1,v_2,v_3,...
    As long as the file mapVariable has the map variable in the first line, other lines do not matter.
    */
    public static void MAP(BeliefNetwork bn, String evidence, String mapVariable, String dest) throws IOException {

        List<Pair<String, String>> evidenceL = loadEvidence(evidence);
        List<String> mapVariableL = loadMapVariables(mapVariable);
        MAP(bn, evidenceL, mapVariableL, dest);
    }

    /*
    Generate simulated cases based on the probability distribution only. Save the cases in hugin format in dest.
    */
    public static void simulate(BeliefNetwork bn, int numCases, double fractionMissing, String dest) throws StateNotFoundException, IOException {
        Simulator s = new Simulator(bn);
        LearningData d = s.simulate(numCases, fractionMissing);
        File f = new File(dest);

        d.writeData(f);
    }

    /*
    Set evidence for the bn.
    */
    public static void setEvidence(BeliefNetwork bn, Map<FiniteVariable, Object> evidence)
    {
        /* Set evidence. */
        try {
            bn.getEvidenceController().setObservations(evidence);
        } catch (StateNotFoundException e) {
            System.err.println("Error, failed to set evidence: " + e);
            return;
        }
    }

    public static void setEvidence(BeliefNetwork bn, List<Pair<String, String>> evidence1)
    {
        setEvidence(bn, convertEvidence(bn, evidence1));
    }

    public static void setEvidence(BeliefNetwork bn, String evidence) throws IOException {
        setEvidence(bn, convertEvidence(bn, loadEvidence(evidence)));
    }

    /*
    convert all the variables and values in the file evidence into a list of pair.
    */
    public static List<Pair<String, String>> loadEvidence(String evidence) throws IOException
    {

        File evidenceF = new File(evidence);
        BufferedReader br = new BufferedReader(new FileReader(evidenceF));
        String variables = br.readLine().trim();
        String[] var = variables.split(",");
        String values = br.readLine().trim();
        String[] val = values.split(",");

        if (var.length != val.length) {
            System.out.println("Number of variables does not match the number of values in the evidence");
        }
        List<Pair<String, String>> evidenceL = new LinkedList<>();
        for (int i = 0; i < var.length; i++) {
            evidenceL.add(new Pair<String, String>(var[i], val[i]));
        }
        return evidenceL;
    }

    public static List<String> loadMapVariables(String mapVariable) throws IOException {
        /*
        Put all the map variables in the file mapVariable in a list.
        */
        File mapVariableF = new File(mapVariable);
        BufferedReader br = new BufferedReader(new FileReader(mapVariableF));
        String variables = br.readLine().trim();
        String[] var = variables.split(",");
        List<String> mapVariableL = new LinkedList<>();
        for (int i = 0; i < var.length; i++) {
            mapVariableL.add(var[i]);
        }
        return mapVariableL;
    }

    public static Map<FiniteVariable, Object> convertEvidence(BeliefNetwork bn, List<Pair<String, String>> evidence1)
    {
        Map<FiniteVariable, Object> evidence = new HashMap<>(2);
        FiniteVariable var = null;
        for (int i = 0; i < evidence1.size(); i++) {
            Pair<String, String> p = evidence1.get(i);
            var = (FiniteVariable) bn.forID(p.getKey());
            evidence.put(var, var.instance(p.getValue()));
        }
        return evidence;
    }

    public static Set<Variable> convertMapVariables(BeliefNetwork bn, List<String> mapVariable)
    {
        Set<Variable> setMAPVariables = new HashSet<>();
        for (int i = 0; i < mapVariable.size(); i++) {
            Variable a = bn.forID(mapVariable.get(i));
            if (a == null)
            {
                System.out.print(mapVariable.get(i));
            }
            setMAPVariables.add(bn.forID(mapVariable.get(i)));
        }
        return setMAPVariables;
    }


}
