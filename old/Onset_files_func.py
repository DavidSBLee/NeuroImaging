##!/bin/python
# First Created: 6/14/2017
# Last Updated: 6/19/2017 (.tsv files are now saved in 'func' directory (not beh) in order to properly follow BIDS data structure)
# AUTHOR: Mike Kelly
# Purpose: Convert eprime .txt files from MRI Scans to .tsv files (which will be used to create onset files for fmri processing)

#NOTE: This script works under the assumption that the particpants already have a 'func' directory, as the NIfTI files should have been converted before running this script. If Pp did not have any functional scans, there should be no need to create this .tsv file.

import os
import glob
import os.path



#Set paths to .txt files and .tsv files

raw_path = '/study3/midus3/raw-data/scan_eprime/data/'
txt_files = glob.glob(r"%s/midus3_order[1-2]_eyetracking_v0[0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9].txt"%(raw_path))



#Check that .tsv files have not already been created. If no .tsv file, script will create .tsv file in 'func' directory (using the .txt file from raw-data). If .tsv file already exists, no action will be taken. As a check for user, script will print names of those subjects for which directories are being created.

for file in txt_files:
    name = file.split('_')[4]
    name = name.split('-')
    tsv_path = "/study3/midus3/processed_data/my_dataset/sub-%s/func/"%(name[1])
    if os.path.isfile("/study3/midus3/processed_data/my_dataset/sub-%s/func/sub-%s_task-ER_events.tsv"%(name[1], name[1])) == False:
        print "Creating .tsv file for sub-" + name[1]
        os.chdir(tsv_path)
        tsv = "/study3/midus3/processed_data/my_dataset/sub-%s/func/sub-%s_task-ER_events.tsv"%(name[1], name[1])
        os.system("eprime2tabfile " + file + " > " + tsv)
