#!/usr/bin/env python3
import subprocess
import glob
import sys
import os

print(sys.argv)
subNum = sys.argv[1]

path = "/study4/midusref/DATA/mri/processed/david/%s"%(subNum)
os.system("antsApplyTransforms -d 3 -i "%s/%s_T1w_fslanat_brain_nii.gz"%(path, subNum) -r /home/slee/Desktop/xMAYO_T/template_brain_MIDUS3_resampled.nii.gz -o ["/study4/midusref/DATA/mri/processed/david/%s/%s_concetenated.nii.gz"%(subNum, subNum), 1] -t "/study4/midusref/DATA/mri/processed/david/%s/%s_structural_to_resampled_template_1Warp.nii.gz"%(subNum, subNum) -t "/study4/midusref/DATA/mri/processed/david/%s/%s_structural_to_resampled_template_0GenericAffine.mat"%(subNum, subNum)")
