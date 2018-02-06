#!/bin/python3

# Author: David SB Lee
# First Compiled: 12/13/17
# Purpose: Trim first 4 volmues off of BOLD data to account for scanner warm up

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
boldfiles = glob.glob('%s/sub-MRID-%s/func/*run*bold.nii.gz'%(path, subId))
restingfiles = glob.glob('%s/sub-MRID-%s/func/*rest*bold.nii.gz'%(path, subId))

if __name__ == "__main__":
    # Create func directory if it doesn't exist
    os.makedirs("%s/sub-MRID-%s/func"%(analysis_path, subId), exist_ok = True)

    for bold in boldfiles:
        print (bold)

        # Strip off .nii.gz from file name (makes code below easier)
        bold_no_ext = bold[:-7]
        print(bold_no_ext)

        #extract run number
        runNum = bold_no_ext[-6:-5]
        print(runNum)

         # Extract output Path
        extendedPathBold = bold[41:105]

        # Fix orientation (Only not done in the pre-processing steps)
        #os.system("fslswapdim %s z -x -y %s_mod"%(bold_no_ext, bold_no_ext))

        # Trim 4 Volumes
        os.system("fslroi %s %s/%s_mod 4 -1"%(bold_no_ext, analysis_path, extendedPathBold))

    for resting in restingfiles:
        print (resting)

        # Strip off .nii.gz from file name (makes code below easier)
        resting_no_ext = resting[:-7]
        print(resting_no_ext)
        runNumResting = "4"

         # Extract output Path
        extendedPathResting = resting[41:90]

        # Fix orientation (Only not done in the pre-processing steps)
        #os.system("fslswapdim %s z -x -y %s_mod"%(bold_no_ext, bold_no_ext))

        # Trim 4 Volumes
        os.system("fslroi %s %s/%s_mod 4 -1"%(resting_no_ext, analysis_path, extendedPathResting))
        