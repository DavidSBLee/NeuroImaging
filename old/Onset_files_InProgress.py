#NOTE: Check BIDS formatting and make sure all files and filepaths follow the proper format!!!

import csv
import sys
import glob
import os

raw_path = '/study3/midus3/raw-data/scan_eprime/data'
#Note: Ideally, would like this to go into 'behav' folder, or something similar. Just putting file in sub_### folder for testing purposes.
processed_path = glob.glob('/study3/midus3/processed_data/my_dataset/sub-[0-9][0-9][0-9]/test_sub-[0-9][0-9][0-9].tsv')

txt_files = glob.glob(r"%s/midus3_order[1-2]_eyetracking_v0[0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9].txt"%(raw_path))
#tsv_files = r"%s/"%(processed_path)

for file in txt_files:
    os.system("eprime2tabfile " + file + ">" + processed_path)
