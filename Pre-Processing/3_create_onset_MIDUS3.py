#!/usr/bin/env python3

# Author: David SB Lee
# First Compiled: 8/29/17
# Last Updated: 10/24/2017
# Updated Content: (10/20/2017) Added authorship
# Updated Content: (10/24/2017) Changed Temporary Path to fit BIDS validation
# Purpose: Create onsetfiles from E-prime.txt files

import glob
import os

# Convert eprime .txt files from MRI Scans to .tsv files (which will be used to create onset files for fmri processing) 

# Set paths to .txt files and .tsv files
versionNumber = 1
onsetPath = '/study3/midus3/raw-data/scan_eprime/data/'
niftiPath = '/study3/midus3/processed_data/MIDUS3_Imaging'
temporaryBigPath = "/study/midus3/processed_data/Temporary/Big/" 
temporarySmallPath = "/study/midus3/processed_data/Temporary/Small/"

txt_files = glob.glob("%s/midus3_order[1-2]_eyetracking_v[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9]*.txt"%(onsetPath))
    
# Check that .tsv files have not already been created. If no .tsv file, script will create .tsv file in 'func' directory (using the .txt file from raw-data). If .tsv file already exists, no action will be taken. As a check for user, script will print names of those subjects for which directories are being created.
for file in txt_files:
    name = file.split('_')[4] 
    name = name.split('-')
    name = name[1]
    #version = file[79] # extracts version numbers for each of multiple task data
    tsv_path = niftiPath + "/sub-%s/func/"%(name) # name extracts first ###

    if os.path.isfile(temporaryBigPath + "/sub-%s_task-ER_events.tsv"%(name)) == True:
        print ("----------No E-prime Conversion for", name, "Needed----------")

    elif os.path.isfile(temporaryBigPath + "/sub-%s_task-ER_events.tsv"%(name)) == False:
        print ("----------Converting----------")
        # Don't do anything when .tsv is already there
        if os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events.tsv"%(name, name)) == True:
            print (".tsv file(s) already exists for " + name)
        
        # Don't do anything when .tsv with any version number is already there
        elif os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events_1.tsv"%(name, name)) == True and os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events_2.tsv"%(name, name)) == True:
            print (".tsv file(s) already exists for " + name)

        # Convert when .tsv is not there
        elif os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events.tsv"%(name, name)) == False:
            if "009" in name: # Currently hardcoded for 009 --> more global approach needed using file counter
                print ("----------Creating .tsv file for " + name + "----------")
                os.chdir(tsv_path)
                tsv = temporaryBigPath + "/sub-%s_task-ER_events_%s.tsv"%(name, versionNumber)
                os.system("eprime2tabfile " + file + " > " + tsv)
                versionNumber += 1
            else: 
                print ("----------Creating .tsv file for " + name + "----------")
                os.chdir(tsv_path)
                tsv = temporaryBigPath + "/sub-%s_task-ER_events.tsv"%(name)
                os.system("eprime2tabfile " + file + " > " + tsv)


"""
# Extract subject number from eprime scan files
subNum = set([int(txts.split('/')[6][30:33]) for txts in txt_files])
print subNum

# Extract subject number from single onset files
onset_files = glob.glob("/study3/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]/func/*tsv")
subNum2 = set([int(onset.split('/')[7][4:7]) for onset in onset_files])
print subNum2

# Cross Check onset files vs. eprime scan files
for num in subNum:
    if num in subNum2:
        print "Onset files already exist"
    # Only initiate conversion if there isn't an onset file already
    if num not in subNum2:
        print "Converting..."
 """   