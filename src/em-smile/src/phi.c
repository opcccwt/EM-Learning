#include <iostream>
#include "libs/smile/smile.h"
#include "libs/smile/smilearn.h"

using namespace std;

const char* DATASET_FILE = "simulatedData/em_data.dat";
const char* NETWORK_FILE = "simulatedData/em_bayes_network.net";
const char* OUTPUT_FILE  = "output/em_learned_parameters.net";

int main()
{
	
	DSL_dataset ds;
    
    if (ds.ReadFile(DATASET_FILE) != DSL_OKAY) {
        cout << "Cannot read data file."<<endl;
        exit(1);
    }

	DSL_network net;
  	if (net.ReadFile(NETWORK_FILE, DSL_HUGIN_FORMAT) != DSL_OKAY) {
		cout << "Cannot read network... exiting." << endl;
		exit(1);
  	}

	vector<DSL_datasetMatch> matches;
  	string err;
  	if (ds.MatchNetwork(net, matches, err) != DSL_OKAY) {
     	cout << "Cannot match network... exiting." << endl;
     	exit(1);
  	}

	DSL_em em;
  	if (em.Learn(ds, net, matches) != DSL_OKAY) {
     	cout << "Cannot learn parameters... exiting." << endl;
     	exit(1);
  	}
  	net.WriteFile(OUTPUT_FILE, DSL_HUGIN_FORMAT);
}
