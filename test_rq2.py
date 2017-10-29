import pickle
import numpy as np

data_family = pickle.load( open( "rq2_sqlite_rank.p", "rb" ) )

family = data_family.keys()
assert(len(family) == 1), "Something is wrong"
family = family[0]


train_datasets = sorted(data_family[family].keys())

# print 'X', ''.join([t+' . . ' for t in train_datasets])
print 'X', ' '.join([t for t in train_datasets])
# print 'X', 'source target diff ' * len(train_datasets)
for ttd in train_datasets:
    print ttd,
    # assert(len(data_family[family][td].keys())+1 == len(train_datasets)), "Something is wrong"
    for td in train_datasets:
        if ttd not in data_family[family][td].keys(): print 'X',
        else:
            s = round(np.mean(data_family[family][td][ttd]['source']), 3)
            t = round(np.mean(data_family[family][td][ttd]['target']), 3)
            print s-t,
    print

