import java.io.IOException;
import java.util.*;

import edu.ucla.belief.StateNotFoundException;
import javafx.util.Pair;
import edu.ucla.belief.io.NetworkIO;
import edu.ucla.belief.BeliefNetwork;
import edu.ucla.belief.io.hugin.HuginNode;
import edu.ucla.belief.learn.Simulator;
import edu.ucla.belief.learn.LearningData;

public class test {
    public static void main(String[] args) throws IOException, StateNotFoundException {
        List<String> L = new LinkedList<>();
        L.add("1");
        L.add("2");
        System.out.println(L);
        change(L);
        System.out.println(L);

    }
    public static void change(List<String> L)
    {
        L.remove(0);
    }
}
