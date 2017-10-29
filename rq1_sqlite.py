import pandas as pd
import numpy as np
import os
import pickle

reps = 5
familys = ['sqlite']
data_family = {}

for family in familys:
    files = ['./data/' + file for file in os.listdir('./data/') if family in file]
    data_family[family] = {}
    for file in files:
        data_family[family][file] = {}
        rest = [f for f in files if file!=f]
        assert(len(rest)+1 == len(files)), "Something is wrong"

        train_content = pd.read_csv(file)
        train_cols = train_content.columns.values.tolist()
        ctrain_indep = [c for c in train_cols if '<$' not in c]
        ctrain_dep = [c for c in train_cols if '<$' in c]
        assert(len(ctrain_dep) == 1), "Something is wrong"
        ctrain_dep = ctrain_dep[0]
        train_indep = train_content[ctrain_indep]
        train_dep = train_content[ctrain_dep]

        for r in rest:
            print "train: ", file, " test: ", r,
            data_family[family][file][r] = []
            for _ in xrange(reps):
                print ". ",
                from sklearn.tree import DecisionTreeRegressor
                tree = DecisionTreeRegressor()
                tree.fit(train_indep, train_dep)

                test_content = pd.read_csv(r)
                test_cols = test_content.columns.values.tolist()
                ctest_indep = [c for c in test_cols if '<$' not in c]
                ctest_dep = [c for c in test_cols if '<$' in c]
                assert (len(ctest_dep) == 1), "Something is wrong"
                ctest_dep = ctest_dep[0]

                assert(len(ctrain_indep) == len(ctest_indep)), "Somethign is wrong"

                test_content = test_content.sort(ctest_dep)
                test_indep = test_content[ctest_indep]
                test_dep = test_content[ctest_dep]

                test_predict_dep = tree.predict(test_indep)
                ranks = [i[0] for i in sorted(enumerate(test_predict_dep), key=lambda x: x[1])]

                trank = ranks[0]

                data_family[family][file][r].append(np.mean(trank))
            print
            print data_family[family][file][r]
            print
    print "-- " * 20

    pickle.dump(data_family, open(family + "rank.p", "wb"))