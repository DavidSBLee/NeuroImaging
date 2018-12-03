#!/usr/bin/env python3

# Author: David SB Lee
# First Compiled: 8/29/17
# Purpose: Convert task-fMRI behavioral data to tsv

# Things to change when runing on different data set
# 1. all paths
# 2. all splits

import glob
import os

# Set global variables (paths)
versionNumber = 1
onsetPath = '/study3/midus3/raw-data/scan_eprime/data/'
niftiPath = '/study3/midus3/processed_data/MIDUS3_Imaging'
temporaryBigPath = "/study/midus3/processed_data/Temporary/Big/" 
temporarySmallPath = "/study/midus3/processed_data/Temporary/Small/"
txt_files = glob.glob("%s/midus3_order[1-2]_eyetracking_v[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9]*.txt"%(onsetPath))

if __name__ == "__main__":
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
       