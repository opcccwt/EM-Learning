import edu.ucla.belief.*;
import edu.ucla.belief.io.NetworkIO;
import java.io.File;
import java.io.IOException;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException, StateNotFoundException {
        String path = "/mnt/d/academic/Master/UCLA/CapstoneProject/Harmonization/learned_sample.net";

        BeliefNetwork bn = null;
        try{
            /* Use NetworkIO static method to read network file. */
            bn = NetworkIO.read( path );
        }catch( Exception e ){
            System.err.println( "Error, failed to read \"" + path + "\": " + e );
            return;
        }

        String source = "/mnt/d/academic/Master/UCLA/CapstoneProject/Harmonization/POP909-Dataset-master/POP909_Hugin/";
        List<Integer> exception = Arrays.asList(48, 71, 77, 102, 120, 320, 372, 408, 437, 500, 503, 519, 691, 850, 879);
        for (int i = 2; i < 3; i++)
        {
            if (exception.contains(i)) { continue;}
            String s = source + String.format("%03d", i) + "/" + String.format("%03d", i) + "alteredcut";
            /*
            BeliefNetwork temp = bn.deepClone();
            Utility.setEvidence(temp, s + ".mel");
            int numCases = 1;
            double fractionMissing = 0.0;
            System.out.println("Generate " + numCases + " simulated cases for " + s);
            Utility.simulate(temp, numCases, fractionMissing, s + ".result");
            System.out.println("Done");
             */
            System.out.println(s + ".mel");
            System.out.println(s + ".har");
            System.out.println(s + "1.result");
            Utility.MAP(bn, s + ".mel", s + ".har", s + "1.result");
        }
    }
}