import os, fnmatch
import gzip
import shutil

dir_out = '/media/sf_Downloads/__effis/Mask_waterWorld_2000/tiles/'

def find_files(directory, pattern='*'):
    if not os.path.exists(directory):
        raise ValueError("Directory not found {}".format(directory))

    matches = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            if fnmatch.filter([full_path], pattern):
                matches.append(os.path.join(root, filename))
    return matches

files_gz=find_files('/media/sf_Downloads/__effis/Mask_waterWorld_2000/downloaded','*.gz')

for file_gz in files_gz:
    # nome_tif = os.path.splitext(file_gz)[0].split("/")[-1:]
    nome_tif = file_gz.split("/")[-1:][0].split(".")[0]
    # print nome_tif
    finale = dir_out + nome_tif + ".tif"
    # print finale
    with gzip.open(file_gz, 'rb') as f_in:
        with open(finale, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
