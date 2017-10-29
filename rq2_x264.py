import pandas as pd
import numpy as np
import os
import pickle
from random import randint

reps = 30
familys = ['x264']
data_family = {}

for family in familys:
    files = ['./data/' + file for file in os.listdir('./data/') if family in file]
    data_family[family] = {}
    for file in files:
        data_family[family][file] = {}
        rest = [f for f in files if file!=f]
        assert(len(rest)+1 == len(files)), "Something is wrong"

        # Read the content of the source
        source_content = pd.read_csv(file)
        # Find the column names of the source
        source_cols = source_content.columns.values.tolist()
        csource_indep = [c for c in source_cols if '<$' not in c]
        csource_dep = [c for c in source_cols if '<$' in c]
        assert(len(csource_dep) == 1), "Something is wrong"
        csource_dep = csource_dep[0]
        # Extract the indep and dep columns of the source_content
        source_indep = source_content[csource_indep]
        source_dep = source_content[csource_dep]

        for r in rest:
            print "train: ", file, " test: ", r,
            data_family[family][file][r] = {}
            data_family[family][file][r]['source'] = []
            data_family[family][file][r]['target'] = []
            for _ in xrange(reps):
                print ". ",
                from sklearn.tree import DecisionTreeRegressor
                tree1 = DecisionTreeRegressor(random_state=randint(0, 100))
                tree1.fit(source_indep, source_dep)

                target_content = pd.read_csv(r)
                target_cols = target_content.columns.values.tolist()
                ctarget_indep = [c for c in target_cols if '<$' not in c]
                ctarget_dep = [c for c in target_cols if '<$' in c]
                assert (len(ctarget_dep) == 1), "Something is wrong"
                ctarget_dep = ctarget_dep[0]

                assert(len(csource_indep) == len(ctarget_indep)), "Somethign is wrong"

                indexes = range(len(target_content))
                from random import shuffle
                shuffle(indexes)
                ttrain_indexes = indexes[:int(len(target_content) * 0.4)]
                ttest_indexes = indexes[int(len(target_content) * 0.4):]

                ttrain_content = target_content.ix[ttrain_indexes]
                ttest_content = target_content.ix[ttest_indexes]

                ttrain_indep = ttrain_content[ctarget_indep]
                ttrain_dep = ttrain_content[ctarget_dep]

                ttest_content = ttest_content.sort(ctarget_dep)
                ttest_indep = ttest_content[ctarget_indep]
                ttest_dep = ttest_content[ctarget_dep]

                tree2 = DecisionTreeRegressor(random_state=randint(0, 100))
                tree2.fit(ttrain_indep, ttrain_dep)

                source_predict_dep = tree1.predict(ttest_indep)
                source_ranks = [i[0] for i in sorted(enumerate(source_predict_dep), key=lambda x: x[1])]
                target_predict_dep = tree2.predict(ttest_indep)
                target_ranks = [i[0] for i in sorted(enumerate(target_predict_dep), key=lambda x: x[1])]

                data_family[family][file][r]['source'].append(source_ranks[0])
                data_family[family][file][r]['target'].append(target_ranks[0])
            print
            # print data_family[family][file][r]['source']
            # print data_family[family][file][r]['target']

        print "-- " * 20

    pickle.dump(data_family, open('rq2_' + family + "_rank.p", "wb"))