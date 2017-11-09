from __future__ import division
from sk import rdivDemo
import os
import pickle
import numpy as np

rouge_systems = ['sac_0', 'sac_1', 'sac_2', 'sac_3']

def run(pickle_file, measure):
    content = pickle.load(open(pickle_file))
    source_name = content.keys()[0]
    target_names = sorted(content[source_name].keys())
    for rouge_system in rouge_systems:
        if rouge_system in target_names: target_names.remove(rouge_system)

    wins = []
    losses = []

    for target_name in target_names:

        results = []
        fractions = sorted(content[source_name][target_name].keys(), key=lambda x: int(x))
        bellwether = content[source_name][target_name][fractions[0]][measure]['bellwether']
        results.append(['BW'] + bellwether)
        for fraction in fractions:
            # print fraction,
            target = content[source_name][target_name][fraction][measure]['target']
            results.append(['T_' + fraction] + target)

        ret = rdivDemo(target_name, results, globalMinMax=False, isLatex=False, print_option=False)

        t_rank = -1
        for r in ret:
            if r[2].name == 'BW': t_rank = r[2].rank

        if t_rank == 0: wins.append(target_name)
        else: losses.append([target_name, t_rank])

    print source_name, len(wins), len(losses)


pickle_folder = '../Processed/'
pickle_files = [
    # '../Processed/spear.p',
    '../Processed/sac.p',
    # '../Processed/x264.p'
]

for pickle_file in pickle_files:
    run(pickle_file, 'rank')