#!/bin/python3

# Author: David SB Lee
# First Compiled: 12/13/2017
# Purpose: Generate registration calculations for SyN (Type of Nonlinear Registration: Symmetric Normalization)
# SyN Based Warping == Linear + Non-Linear bidirectional mapping

# Things to change when running on different data set
# 1. All Paths

import subprocess
import glob
import sys
import os

print(sys.argv)
subNum = sys.argv[1]

path = "/path/to/subdir"

subprocess.call(["antsRegistrationSyN.sh", "-d", "3", "-f", "/path/to/template/nifti", 
                 "-m", "/path/to/template/nifti", 
                 "-o", "/path/to/output/nifti, "-t", "s"])

### Example
#path = "/study4/midusref/DATA/mri/processed/david/Post_Anonymization/%s/"%(subNum)
#subprocess.call(["antsRegistrationSyN.sh", "-d", "3", "-f", 
#                "/study4/midusref/DATA/mri/processed/david/scripts/Mayo_T1w_resampled_template.nii.gz", 
#                "-m", "%s/%s_T1w.nii.gz"%(path, subNum), 
#                "-o", "/study4/midusref/DATA/mri/processed/david/Post_Anonymization/%s/%s_structural_to_resampled_template_"%(subNum,subNum), "-t", "s"])
                 
                 
