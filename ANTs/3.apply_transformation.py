#!/bin/python3

# Author: David SB Lee
# First Compiled: 12/15/2017
# Purpose: Normalization Final Steap
#          Apply the cconcatenated transform (calculated Linear & Non-Linear transforms) to the origianl T1w 

# Things to change when running on different data set
# 1. All Paths

import subprocess
import glob
import sys

print(sys.argv)
subNum = sys.argv[1]

path = "/path/to/subdir"

# Apply concatenated transform and begin Normalization
subprocess.call(["antsApplyTransform", "-d", "3", "-i", "/path/to/T1w/nifti, 
                 "-r", "/path/to/template/nifti", 
                 "-t", "/path/to/concatenated.nii.gz", # output of step 2 concatenation
                 "-o", "/path/to/final.nii.gz"]) # final output
