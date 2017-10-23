##!/bin/python
# First Created: 6/14/2017
# Last Updated: 6/15/2017
# AUTHOR: Mike Kelly
# Purpose: Convert eprime .txt files from MRI Scans to .tsv files (which will be used to create onset files for fmri processing)

import os
import glob
import os.path



#Set paths to .txt files and .tsv files

raw_path = '/study3/midus3/raw-data/scan_eprime/data/'
txt_files = glob.glob(r"%s/midus3_order[1-2]_eyetracking_v0[0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9].txt"%(raw_path))



#Check that .tsv files have not already been created. If no .tsv file, script will create 'beh' folder in subject's data directory and create .tsv file in said directory (using the .txt file from raw-data). If .tsv file already exists, no action will be taken. As a check for user, script will print names of those subjects for which directories are being created.

for file in txt_files:
    name = file.split('_')[4]
    name = name.split('-')
    beh_path = "/study3/midus3/processed_data/my_dataset/sub-%s/"%(name[1])
    if os.path.isfile("/study3/midus3/processed_data/my_dataset/sub-%s/beh/task-ER_events.tsv"%(name[1])) == False:
        print "Creating .tsv file for sub-" + name[1]
        os.chdir(beh_path)
        os.makedirs("beh")
        tsv = "/study3/midus3/processed_data/my_dataset/sub-%s/beh/task-ER_events.tsv"%(name[1])
        os.system("eprime2tabfile " + file + " > " + tsv)
