from __future__ import division
import pandas as pd
from os import listdir

def run(filename):
    pdcontent = pd.read_csv(filename)
    indepcolumns = [col for col in pdcontent.columns if "<$" not in col]
    depcolumns = [col for col in pdcontent.columns if "<$" in col]

    # For fast lookup. Better way would be to use pandas
    data = {}
    for id in xrange(pdcontent.shape[0]):
        item = pdcontent.iloc[id]
        indep = ','.join(map(str, map(int, item[indepcolumns].tolist())))
        if indep not in data.keys():
            data[indep] = [id]
        else:
            data[indep].append(id)

    # display
    print filename
    for key in data.keys():
        if len(data[key]) > 1:
            print key, data[key]
    print '----- + ' * 20


if __name__ == "__main__":
    data_folder = "../Data/"
    filenames = [data_folder + f for f in listdir(data_folder) if '.csv' in f]
    for filename in filenames:
        run(filename)
        raw_input()
