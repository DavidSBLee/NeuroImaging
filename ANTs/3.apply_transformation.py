#!/usr/bin/env python3
import subprocess
import glob
import sys

print(sys.argv)
subNum = sys.argv[1]

path = "/study4/midusref/DATA/mri/processed/Daphnee/%s/anat"%(subNum)
brain = glob.glob("%s/T1_brain.nii.gz"%(path))

subprocess.call(["antsApplyTransform", "-d", "3", "-i", "%s/T1_brain.nii.gz"%(path), "-r", "/home/slee/Desktop/xMAYO_T/template_brain_MIDUS3_resampled.nii.gz", "-t", "/home/slee/Desktop/david/sub-%s_concatenated.nii.gz", "-o", "/home/slee/Desktop/david/sub-%s_final.nii.gz"])