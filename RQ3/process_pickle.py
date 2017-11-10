from __future__ import division
import pickle
import os


if __name__ == '__main__':
    pickle_lockers = ['./FlashLocker/', './BWLocker/']
    for pickle_locker in pickle_lockers:
        pickle_folders = [pickle_locker + d + '/' for d in os.listdir(pickle_locker)]
        for pickle_folder in pickle_folders:
            system = pickle_folder.split('/')[-2]
            content_dict = {}
            if system not in content_dict.keys(): content_dict[system] = {}
            pickle_files = [ pickle_folder + f for f in os.listdir(pickle_folder) if '.p' in f]
            for pickle_file in pickle_files:
                print pickle_file
                content = pickle.load(open(pickle_file))
                t_pickle_file = pickle_file.replace('./FlashLocker/sac/', '').replace('.p', '')
                target = t_pickle_file.split('|')[0]
                rep = t_pickle_file.split('|')[1]
                budget = t_pickle_file.split('|')[2]

                if target not in content_dict[system].keys():  content_dict[system][target] = {}
                if budget not in content_dict[system][target].keys(): content_dict[system][target][budget] = {}
                if rep not in content_dict[system][target][budget].keys(): content_dict[system][target][budget][rep] = None

                content_dict[system][target][budget][rep] = content
            processed_pickle_file = './Processed/' + pickle_locker.replace('./', '').replace('Locker/','') + '_' + system + '.p'
            pickle.dump(content_dict, open(processed_pickle_file, 'w'))
