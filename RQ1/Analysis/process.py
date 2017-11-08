from __future__ import division
import pickle
import os
import numpy as np


def draw(pickle_file, measure):
    import matplotlib.pyplot as plt
    name = pickle_file.split('/')[-1].replace('.p', '')
    content = pickle.load(open(pickle_file))
    sources = sorted(content.keys())

    heatmap_arr = []
    for source in sources:
        t = []
        for target in sources:

            try:
                t.append(np.median(content[source][target][measure]))
            except:
                t.append(4000)
        heatmap_arr.append(t)

    # # remove outliers
    # for i, h in enumerate(heatmap_arr):
    #     m = sum([hhh for hhh in h if 2000 != hhh]) / (len(h) - 1)
    #     for j, hh in enumerate(h):
    #         if hh > 4000:
    #             heatmap_arr[i][j] = 8000

    # imgplot = plt.imshow(heatmap_arr, cmap='seismic', interpolation='nearest')
    # plt.xticks(range(len(sources)), sources, fontsize=12, rotation=90)
    # plt.yticks(range(len(sources)), sources, fontsize=12)
    # plt.colorbar(imgplot)
    # plt.show()

    fig, ax = plt.subplots()
    # Using matshow here just because it sets the ticks up nicely. imshow is faster.
    imgplot = ax.matshow(heatmap_arr, cmap='seismic')

    for (i, j), z in np.ndenumerate(heatmap_arr):
        if z == 4000:
            ax.text(j, i, 'X', ha='center', va='center', color='white')
        else:
            ax.text(j, i, '{:0.0f}'.format(z), ha='center', va='center', color='white')

    plt.colorbar(imgplot)
    plt.xticks(range(len(sources)), sources, fontsize=12, rotation=90)
    plt.yticks(range(len(sources)), sources, fontsize=12)

    plt.ylabel('Source')
    plt.xlabel('Target')
    fig.set_size_inches(40, 40)
    plt.savefig('../Figures/' + name + '_' + measure + '.png', )


pickle_folder = '../Processed/'
pickle_files = [
    # '../Processed/spear.p',
    # '../Processed/sac.p',
    '../Processed/sqlite.p',
    # '../Processed/x264.p'
]

measures = ['rank', 'mmre', 'abs_res']
for measure in measures:
    for pickle_file in pickle_files:
        draw(pickle_file, measure)



