#!/bin/python3

# Author: David SB Lee
# First Compiled: 01/11/18
# Purpose: Compiles BOLD runs that needs be scrubbed based on high motion criteria
# High motion criteria: if 25% or more TRs pass the threshold(FD>0.5 for task & FD>0.2 for resting), scrub that run

import glob
import os
import sys
import subprocess

# The script takes an argument
print(sys.argv)
subId = sys.argv[1]

# Set global variables (input paths)
path = '/study4/midusref/midusref_imaging_public'
analysis_path = '/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis'
QA_path = '/study4/midusref/midusref_imaging_public/QA'
restingfiles = glob.glob('%s/sub-MRID-%s/func/*rest*bold.nii.gz'%(path, subId))
boldfiles = glob.glob('%s/sub-MRID-%s/func/*run*bold.nii.gz'%(path, subId))

# Set global variable (output paths)
out_bad_bold_list = "%s/MIDUSREF_subjects_Task_high_motion_57_FD_0.5_scrub.txt"%(QA_path)
out_bad_bold_higher_fd_list = "%s/MIDUSREF_subjects_Task_high_motion_57_FD_0.9_scrub.txt.txt"%(QA_path)
out_bad_rest_list = "%s/MIDUSREF_subjects_Rest_high_motion_59_scrub.txt"%(QA_path)

if __name__ == "__main__":
    # Create func directory if it doesn't exist
    os.makedirs("%s/sub-MRID-%s/func"%(analysis_path, subId), exist_ok = True)

    for resting in restingfiles:
        #print (resting)

        # Strip off .nii.gz from file name (makes code below easier)
        resting_no_ext = resting[:-7]
        #print(resting_no_ext)
        runNumResting = "4"
        print (runNumResting)

         # Extract output Path
        extendedPathResting = resting[41:90]

        # Create a list of subjects who exceeded motion threshold
        output = subprocess.check_output("grep -o 1 %s/sub-MRID-%s/func/QA/%s_confound_rest_with_FD_0.2.txt | wc -l"%(analysis_path, subId, runNumResting), shell=True)
        num_scrub = [int(s) for s in output.split() if s.isdigit()]
        if num_scrub[0]>=59:
            with open(out_bad_rest_list, "a") as myfile:
                print ("compiling bad resting runs")
                myfile.write("Which NIfTI: %s_resting_%s\nHow many motion outliers: %s\n"%(subId, runNumResting, str(num_scrub)))

for bold in boldfiles:
    #print (bold)

    # Strip off .nii.gz from file name (makes code below easier)
    bold_no_ext = bold[:-7]
    #print(bold_no_ext)

    #extract run number
    runNum = bold_no_ext[-6:-5]
    runNum = int(runNum)
    print(runNum)

     # Extract output Path
    extendedPathBold = bold[41:105]

    # For FD > 0.5
    output = subprocess.check_output("grep -o 1 %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.5.txt | wc -l"%(analysis_path, subId, runNum), shell=True)
    num_scrub = [int(s) for s in output.split() if s.isdigit()]
    if num_scrub[0]>=57:
        with open(out_bad_bold_list, "a") as myfile:
            print ("compiling bad task runs")
            myfile.write("Which NIfTI: %s_bold_%s\nHow many motion outliers: %s\n"%(subId, runNum, str(num_scrub)))

    # For FD > 0.9
    output = subprocess.check_output("grep -o 1 %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.9.txt | wc -l"%(analysis_path, subId, runNum), shell=True)
    num_scrub = [int(s) for s in output.split() if s.isdigit()]
    if num_scrub[0]>=57:
        with open(out_bad_bold_higher_fd_list, "a") as myfile:
            print ("compiling bad task runs")
            myfile.write("Which NIfTI: %s_bold_%s\nHow many motion outliers: %s\n"%(subId, runNum, str(num_scrub)))