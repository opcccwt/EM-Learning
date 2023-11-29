================================================
==> Make sure encoding is ok
================================================

Manually edit mildew.hugin to produce ok net.  Old version is in mildew-orig.hugin

================================================
==> Normalize, convert to .net, and remove noisymin:
================================================

java mark.reason.apps.BnFilter alarm.xdsl alarm.net
java mark.reason.apps.BnFilter hailfinder.xdsl hailfinder.net
java mark.reason.apps.BnFilter pathfinder.xdsl pathfinder.net
java mark.reason.apps.BnFilter tcc4f.obfuscated.xdsl tcc4f.obfuscated.net -f mark.reason.flt.FltToTables

java mark.reason.apps.BnFilter diabetes.hugin diabetes.net
java mark.reason.apps.BnFilter mildew.hugin mildew.net
java mark.reason.apps.BnFilter munin1.hugin munin1.net
java mark.reason.apps.BnFilter munin2.hugin munin2.net
java mark.reason.apps.BnFilter munin3.hugin munin3.net
java mark.reason.apps.BnFilter munin4.hugin munin4.net
java mark.reason.apps.BnFilter pigs.hugin pigs.net
java mark.reason.apps.BnFilter water.hugin water.net

(blockmap, mastermind, and students were already in this format)

================================================================================
==> Create no local structure versions
================================================================================

ls *.net | xargs -t -IFFF -n 1 java -Xmx512M mark.reason.apps.BnFilter -pw mark.reason.net.PwHugin -f mark.reason.flt.FltRemoveLocalStructure FFF FFF-gs.net

================================================
==> Evidence generated as follows:
================================================


ls *.net | xargs -t -n 1 java -Xmx700M mark.reason.apps.BnConstructEvidence -seed 6  \
-e '1,mark.reason.query.EgNull,mark.reason.query.VsNull' \
-e '5,mark.reason.query.EgUniform,(mark.reason.query.VsAnd mark.reason.query.VsRoot mark.reason.query.VsNoZero)' \
-e '5,mark.reason.query.EgModel,mark.reason.query.VsOneToOneHalf' \
-e '5,mark.reason.query.EgModel,mark.reason.query.VsSink' \
mark.bridge.samiam.EwInst


ls mildew.net | xargs -t -n 1 java -Xmx700M mark.reason.apps.BnConstructEvidence -seed 6  \
-e '1,mark.reason.query.EgNull,mark.reason.query.VsNull' \
-e '5,mark.reason.query.EgUniform,(mark.reason.query.VsAnd mark.reason.query.VsRoot mark.reason.query.VsNoZero)' \
-e '5,mark.reason.query.EgModel,mark.reason.query.VsOneToOneHalf' \
-e '5,mark.reason.query.EgModel,mark.reason.query.VsSink' \
mark.bridge.samiam.EwInst


But note that I had to manually (in textedit) edit mildew.net-0007.inst and mildew.net-0008.inst to convert them to UTF8.  They were in some other encoding.

================================================
==> Generated elimination orders as follows:
================================================

ls *.net | xargs -t -IFFF -n 1 java mark.reason.apps.BnConstructEliminationOrder '(mark.reason.structuraleMinfill 1000)' FFF FFF.eo

================================================
==> Validate elimination orders
================================================

gool:~/Documents/dev/data/bn-2005-ijcai chavira$ ls *.net | mystatseo
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile alarm.net.eo) alarm.net
net=alarm.net numVars=37 minCard=2 maxCard=4 aveCard=2.8378378378378377 nodes=37 detNodes=0 edges=46 constants=0 leafVars=11 roots=12 detRoots=0 parms=752 zeroParms=5 oneParms=2 otherParms=745 otherParmsDistinctInCpt=183 maxParmsInCpt=108 aveParmsInCpt=20.324324324324323 orderLogMaxCluster=7.169925001442312
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile blockmap_05_03.net.eo) blockmap_05_03.net
net=blockmap_05_03.net numVars=1005 minCard=2 maxCard=2 aveCard=2.0 nodes=1005 detNodes=990 edges=1729 constants=0 leafVars=25 roots=28 detRoots=28 parms=6972 zeroParms=3471 oneParms=3471 otherParms=30 otherParmsDistinctInCpt=30 maxParmsInCpt=8 aveParmsInCpt=6.937313432835821 orderLogMaxCluster=19.0
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile diabetes.net.eo) diabetes.net
net=diabetes.net numVars=413 minCard=3 maxCard=21 aveCard=11.336561743341404 nodes=413 detNodes=24 edges=602 constants=0 leafVars=2 roots=76 detRoots=0 parms=461069 zeroParms=352224 oneParms=8109 otherParms=100736 otherParmsDistinctInCpt=17749 maxParmsInCpt=7056 aveParmsInCpt=1116.3898305084747 orderLogMaxCluster=17.235144769020817
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile hailfinder.net.eo) hailfinder.net
net=hailfinder.net numVars=56 minCard=2 maxCard=11 aveCard=3.982142857142857 nodes=56 detNodes=7 edges=66 constants=0 leafVars=13 roots=17 detRoots=0 parms=3741 zeroParms=501 oneParms=86 otherParms=3154 otherParmsDistinctInCpt=850 maxParmsInCpt=1188 aveParmsInCpt=66.80357142857143 orderLogMaxCluster=11.673750739438065
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile mastermind_03_08_03.net.eo) mastermind_03_08_03.net
net=mastermind_03_08_03.net numVars=1220 minCard=2 maxCard=2 aveCard=2.0 nodes=1220 detNodes=1166 edges=2068 constants=0 leafVars=48 roots=27 detRoots=0 parms=8326 zeroParms=4109 oneParms=4109 otherParms=108 otherParmsDistinctInCpt=81 maxParmsInCpt=8 aveParmsInCpt=6.824590163934427 orderLogMaxCluster=19.0
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile mildew.net.eo) mildew.net
net=mildew.net numVars=35 minCard=3 maxCard=100 aveCard=17.6 nodes=35 detNodes=0 edges=46 constants=0 leafVars=1 roots=16 detRoots=0 parms=547158 zeroParms=509234 oneParms=826 otherParms=37098 otherParmsDistinctInCpt=9318 maxParmsInCpt=280000 aveParmsInCpt=15633.085714285715 orderLogMaxCluster=20.744518528779924
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile munin1.net.eo) munin1.net
net=munin1.net numVars=189 minCard=1 maxCard=21 aveCard=5.264550264550264 nodes=189 detNodes=65 edges=282 constants=0 leafVars=33 roots=34 detRoots=23 parms=19466 zeroParms=10910 oneParms=2030 otherParms=6526 otherParmsDistinctInCpt=3993 maxParmsInCpt=600 aveParmsInCpt=102.994708994709 orderLogMaxCluster=26.224350318552016
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile munin2.net.eo) munin2.net
net=munin2.net numVars=1003 minCard=2 maxCard=21 aveCard=5.359920239282154 nodes=1003 detNodes=414 edges=1244 constants=0 leafVars=182 roots=249 detRoots=228 parms=83920 zeroParms=46606 oneParms=6496 otherParms=30818 otherParmsDistinctInCpt=21422 maxParmsInCpt=600 aveParmsInCpt=83.6689930209372 orderLogMaxCluster=18.943064208162003
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile munin3.net.eo) munin3.net
net=munin3.net numVars=1044 minCard=1 maxCard=21 aveCard=5.367816091954023 nodes=1044 detNodes=429 edges=1315 constants=0 leafVars=189 roots=262 detRoots=254 parms=85855 zeroParms=47581 oneParms=6601 otherParms=31673 otherParmsDistinctInCpt=22581 maxParmsInCpt=600 aveParmsInCpt=82.23659003831418 orderLogMaxCluster=17.258566033889934
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile pathfinder.net.eo) pathfinder.net
net=pathfinder.net numVars=109 minCard=2 maxCard=63 aveCard=4.110091743119266 nodes=109 detNodes=6 edges=195 constants=0 leafVars=77 roots=1 detRoots=0 parms=97851 zeroParms=43070 oneParms=11835 otherParms=42946 otherParmsDistinctInCpt=2186 maxParmsInCpt=8064 aveParmsInCpt=897.7155963302753 orderLogMaxCluster=14.977279923499918
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile students_03_02.net.eo) students_03_02.net
net=students_03_02.net numVars=376 minCard=2 maxCard=2 aveCard=2.0 nodes=376 detNodes=304 edges=647 constants=0 leafVars=2 roots=14 detRoots=11 parms=2616 zeroParms=1187 oneParms=1187 otherParms=242 otherParmsDistinctInCpt=192 maxParmsInCpt=8 aveParmsInCpt=6.957446808510638 orderLogMaxCluster=21.0
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile tcc4f.obfuscated.net.eo) tcc4f.obfuscated.net
net=tcc4f.obfuscated.net numVars=105 minCard=2 maxCard=2 aveCard=2.0 nodes=105 detNodes=0 edges=193 constants=0 leafVars=69 roots=36 detRoots=0 parms=3236 zeroParms=7 oneParms=7 otherParms=3222 otherParmsDistinctInCpt=1114 maxParmsInCpt=512 aveParmsInCpt=30.81904761904762 orderLogMaxCluster=10.0
java -Xmx1500M mark.reason.apps.BnStats -kv -nonormalize -eoe (mark.reason.struct.EoeFile water.net.eo) water.net
net=water.net numVars=32 minCard=3 maxCard=4 aveCard=3.625 nodes=32 detNodes=6 edges=66 constants=0 leafVars=8 roots=8 detRoots=6 parms=13484 zeroParms=6970 oneParms=318 otherParms=6196 otherParmsDistinctInCpt=3530 maxParmsInCpt=3072 aveParmsInCpt=421.375 orderLogMaxCluster=20.75488750216347
