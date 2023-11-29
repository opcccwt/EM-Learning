#define _GLIBCXX_USE_CXX11_ABI 0
#include <iostream>
#include <sstream>
#include <time.h>
#include "smile.h"
#include "smilearn.h"

#include "math.h"
   
using namespace std;

void print_stats(DSL_em em) {
  cout << "=======================" << endl;
  cout << "equivalent sample size: " << em.GetEquivalentSampleSize() << endl;
  cout << " randomized parameters: " << em.GetRandomizeParameters() << endl;
  cout << "                  seed: " << em.GetSeed() << endl;
  cout << "             relevance: " << em.GetRelevance() << endl;
  cout << " uniformize parameters: " << em.GetUniformizeParameters() << endl;
  cout << "         learning rate: " << em.GetLearningRate() << endl;
  cout << "initial learning point: " << em.GetInitialLearningPoint() << endl;
  cout << "=======================" << endl;
}

double compute_log_likelihood(DSL_dataset &data, DSL_network &net) {

  double ll = 0.0;
  double pe;

  //cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << endl;
  int num_vars = data.GetNumberOfVariables();
  int num_recs = data.GetNumberOfRecords();
  for (int rec = 0; rec < num_recs; rec++) {
    for (int i = 0; i < num_vars; i++) {
      ostringstream os;
      os << "x" << i;
      int var = net.FindNode(os.str().c_str());
      int val = data.GetInt(var,rec);
      if ( val == -1 )
        net.GetNode(var)->Value()->ClearEvidence();
      else
        net.GetNode(var)->Value()->SetEvidence(val);
    }
    net.UpdateBeliefs();
    net.CalcProbEvidence(pe);
    ll += log(pe);
  }
  cout << "            LL: " << ll << endl;
  //cout << "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%" << endl;
  for (int var = 0; var < num_vars; var++)
    net.GetNode(var)->Value()->ClearEvidence();
  return ll;
}


void em(char* const data_set_filename,
        char* const seed_net_filename,
        int n, int N, int k, int seed) {
  clock_t c1, c2;
  string err;
  int error;

  // open the data sets
  DSL_dataset data;
  c1 = clock();
  if ( data.ReadFile(data_set_filename) != DSL_OKAY )
    { cout << "Cannot read data file... exiting." << endl; exit(1); }
  c2 = clock();
  float data_time = (float)(c2-c1)/CLOCKS_PER_SEC;
  cout << "read data time: " << data_time << "\n";

  // open the network:
  c1 = clock();
  DSL_network net;
  if ( net.ReadFile(seed_net_filename, DSL_HUGIN_FORMAT ) != DSL_OKAY )
    { cout << "Cannot read network... exiting." << endl; exit(1); }

  // match the data set and the network:
  vector<DSL_datasetMatch> matches;
  if ( data.MatchNetwork(net,matches,err) != DSL_OKAY )
    { cout << "Cannot match network... exiting." << endl; exit(1); }
  c2 = clock();
  float read_time = (float)(c2-c1)/CLOCKS_PER_SEC;
  cout << " read net time: " << read_time << "\n";

  // learn parameters:
  DSL_em em;
  //em.SetEquivalentSampleSize(0.0);
  em.SetRandomizeParameters(false);
  //em.SetSeed(0);
  //em.SetRelevance(true);
  print_stats(em);

  double ll;
  float learn_time;

  //compute_log_likelihood(data,net);

  c1 = clock();
  error = em.Learn(data,net,matches,&ll);
  if (error != DSL_OKAY) {
    cout << "Cannot learn parameters... exiting." << endl;
    exit(1);
  }
  c2 = clock();
  learn_time = (float)(c2-c1)/CLOCKS_PER_SEC;
  cout << "    learn time: " << learn_time << "\n";

  c1 = clock();
  //compute_log_likelihood(data,net);
  c2 = clock();
  float ll_time = (float)(c2-c1)/CLOCKS_PER_SEC;
  cout << "       ll time:  " << ll_time << endl;

  cout << "csv:";
  cout << " n=" << n;
  cout << " N=" << N;
  cout << " k=" << k;
  cout << " seed=" << seed;
  cout << " ll=" << ll;
  cout << " time=" << learn_time;
  cout << endl;

  net.WriteFile("tmp.net", DSL_HUGIN_FORMAT);
}

int main(int argc, char* const argv[]) {
  if (argc != 7) {
    cout << "usage: " << argv[0] << " DATA SEED n N k seed\n";
    exit(1);
  }
  int n = atoi(argv[3]);
  int N = atoi(argv[4]);
  int k = atoi(argv[5]);
  int seed = atoi(argv[6]);
  em(argv[1],argv[2],n,N,k,seed);
}
