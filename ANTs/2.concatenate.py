#!/bin/python3

# Author: David SB Lee
# First Compiled: 12/13/2017
# Purpose: Apply the calculated Linear & Non-Linear transforms 

# Things to change when running on different data set
# 1. All Paths

import subprocess
import glob
import sys
import os

print(sys.argv)
subNum = sys.argv[1]

path = "/study4/midusref/DATA/mri/processed/david/%s"%(subNum)

# Apply transformation
# GenericAffine.mat == composite linear transform
# 1Warp.nii.gz == nonlinear forward warp

os.system("antsApplyTransforms -d 3 -i "%s/%s_T1w_fslanat_brain_nii.gz"%(path, subNum) 
          -r "/path/to/template/nifti"
          -o ["/study4/midusref/DATA/mri/processed/david/%s/%s_concetenated.nii.gz"%(subNum, subNum), 1] 
          -t "/study4/midusref/DATA/mri/processed/david/%s/%s_structural_to_resampled_template_1Warp.nii.gz"%(subNum, subNum) 
          -t "/study4/midusref/DATA/mri/processed/david/%s/%s_structural_to_resampled_template_0GenericAffine.mat"%(subNum, subNum)")

# Bash Example code
          # {nm} == naming prefix, it can be subject number or filename of your choice
          # {AP} == Path to ANTs binaries, wherever you installed ANTs
          
# ${AP}antsApplyTransforms -d $dim -i $m -r $f -n linear -t ${nm}1Warp.nii.gz -t ${nm}0GenericAffine.mat -o ${nm}_warped.nii.gz --float1
