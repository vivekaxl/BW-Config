from __future__ import division
import pickle
import os
import numpy as np
import matplotlib.pyplot as plt

pickle_folder = '../Processed/'
pickle_files = [pickle_folder + f for f in os.listdir(pickle_folder) if '.p' in f]

for pickle_file in pickle_files:
    content = pickle.load(open(pickle_file))
    sources = sorted(content.keys())
    heatmap_arr = []
    for source in sources:
        t = []
        for target in sources:
            try:
                t.append(np.median(content[source][target]['rank']))
            except:
                t.append(2000)
        heatmap_arr.append(t)

    # remove outliers
    for i, h in enumerate(heatmap_arr):
        m = sum([hhh for hhh in h if 2000 != hhh])/(len(h)-1)
        for j, hh in enumerate(h):
            if hh > 2 * m:
                heatmap_arr[i][j] = 2000

    imgplot = plt.imshow(heatmap_arr, cmap='hot', interpolation='nearest')
    plt.colorbar(imgplot)
    plt.show()

    import pdb
    pdb.set_trace()
