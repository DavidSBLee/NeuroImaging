#!/bin/python3

# Author: David SB Lee
# First Compiled: 12/13/2017
# Purpose: Concatenate the calculated Linear & Non-Linear transforms 

# Things to change when running on different data set
# 1. All Paths

import subprocess
import glob
import sys
import os

print(sys.argv)
subNum = sys.argv[1]

path = "/path/to/subdir"

# Concatenate transformation
# GenericAffine.mat == composite linear transform
# 1Warp.nii.gz == nonlinear forward warp

os.system("antsApplyTransforms -d 3 -i "/path/to/T1w/nifti" 
          -r "/path/to/template/nifti"
          -o ["/path/to/output/nifti, 1] 
          -t "/path/to/nonlinear_forward_map/nifti"
          -t "/path/to/linear_transform.mat")
              
### Python Example 
#def concetanation(subNum):
              #os.system("antsApplyTransforms -d 3 -i 
#             /study4/midusref/DATA/mri/processed/david/Post_Anonymization/%s/%s_T1w.nii.gz 
#             -r /study4/midusref/DATA/mri/processed/david/scripts/Mayo_T1w_resampled_template.nii.gz 
#             -o [/study4/midusref/DATA/mri/processed/david/Post_Anonymization/%s/%s_concatenated.nii.gz, 1] 
#             -t /study4/midusref/DATA/mri/processed/david/Post_Anonymization/%s/%s_structural_to_resampled_template_1Warp.nii.gz -t /study4/midusref/DATA/mri/processed/david/Post_Anonymization/%s/%s_structural_to_resampled_template_0GenericAffine.mat"%(subNum,subNum,subNum,subNum,subNum,subNum,subNum,subNum))
#concetanation(subNum)
              
### Bash Example 
          # {nm} == naming prefix, it can be subject number or filename of your choice
          # {AP} == Path to ANTs binaries, wherever you installed ANTs
          
# ${AP}antsApplyTransforms -d $dim -i $m -r $f -n linear 
#              -t ${nm}1Warp.nii.gz -t ${nm}0GenericAffine.mat 
#              -o ${nm}_warped.nii.gz --float1
