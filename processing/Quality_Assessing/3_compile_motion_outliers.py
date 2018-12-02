#!/bin/python3

# Author: David SB Lee
# First Compiled: 01/11/18
# Purpose: Compiles #of motion outliers for each BOLD data and create an output

import glob
import os
import sys
import subprocess

# The script takes an argument
print(sys.argv)
subId = sys.argv[1]

# Set global variables (paths)
path = '/study4/midusref/midusref_imaging_public'
analysis_path = '/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis'
QA_path = '/study4/midusref/midusref_imaging_public/QA'
boldfiles = sorted(glob.glob('%s/sub-MRID-%s/func/*run*bold.nii.gz'%(path, subId)))
restingfiles = sorted(glob.glob('%s/sub-MRID-%s/func/*rest*bold.nii.gz'%(path, subId)))

# Set global variable (output paths)
outlier_task_list = "%s/MIDUSREF_subjects_Task_number_outliers_FD_0.5.csv"%(QA_path)
outlier_task_higher_list = "%s/MIDUSREF_subjects_Task_number_outliers_FD_0.9.csv"%(QA_path)
outlier_rest_list = "%s/MIDUSREF_subjects_Rest_number_outliers.csv"%(QA_path)

if __name__ == "__main__":
    for resting in restingfiles:
        print (resting)

        # Strip off .nii.gz from file name (makes code below easier)
        resting_no_ext = resting[:-7]
        print(resting_no_ext)
        runNumResting = "4"

         # Extract output Path
        extendedPathResting = resting[41:90]

        output = subprocess.check_output("grep -o 1 %s/sub-MRID-%s/func/QA/%s_confound_rest_with_FD_0.2.txt | wc -l"%(analysis_path, subId, runNumResting), shell=True)
        num_scrub = [int(s) for s in output.split() if s.isdigit()]
        if num_scrub[0]>0:
            with open(outlier_rest_list, "a") as myfile:
                print ("compiling subjects")
                myfile.write("%s_resting %s\n\n"%(subId, str(num_scrub)))

    for bold in boldfiles:
        print (bold)

        # Strip off .nii.gz from file name (makes code below easier)
        bold_no_ext = bold[:-7]
        print(bold_no_ext)

        #extract run number
        runNum = bold_no_ext[-6:-5]
        runNum = int(runNum)
        print(runNum)

         # Extract output Path
        extendedPathBold = bold[41:105]


        output = subprocess.check_output("grep -o 1 %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.5.txt | wc -l"%(analysis_path, subId, runNum), shell=True)
        num_scrub = [int(s) for s in output.split() if s.isdigit()]
        if num_scrub[0] >= 0:
            with open(outlier_task_list, "a") as myfile:
                print ("compiling subjects")
                myfile.write("%s_task_%s %s\n"%(subId, runNum, str(num_scrub)))

        output = subprocess.check_output("grep -o 1 %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.9.txt | wc -l"%(analysis_path, subId, runNum), shell=True)
        num_scrub = [int(s) for s in output.split() if s.isdigit()]
        if num_scrub[0] >= 0:
            with open(outlier_task_higher_list , "a") as myfile:
                print ("compiling subjects")
                myfile.write("%s_task_%s %s\n"%(subId, runNum, str(num_scrub)))



