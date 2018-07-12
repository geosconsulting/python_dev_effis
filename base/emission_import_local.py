import os, fnmatch
import gzip
import shutil

# dir_out = '~/Documents/emission_cp/2018/'


def find_files(directory, pattern='*'):

    if not os.path.exists(directory):
        raise ValueError("Directory not found {}".format(directory))

    matches = []
    # for root, dirnames, filenames in os.walk(directory):
    for dirnames in os.walk(directory):
        for dirname in dirnames:
            print dirname
            # for filename in os.walk(dirname):
            #     print filename
                # full_path = os.path.join(root, filename)
                # if fnmatch.filter([full_path], pattern):
                #     matches.append(os.path.join(root, filename))
    return matches

files_shp = find_files('/home/jrc/Documents/emission_cp/2018', '*.shp')



