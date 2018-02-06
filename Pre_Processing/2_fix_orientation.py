#!/usr/bin/env python3

# Author: David SB Lee
# First Compiled: 8/29/17
# Purpose: Fix Orientations of the 3 Task-fMRi and 1 Resting-State-fMRI run

# Things to change when runing on different data set
# 1. all paths
# 2. all splits

import os
import glob
import shutil
import os.path

# Set global variables (paths)
processed_data = '/study3/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]'
subPath = glob.glob(processed_data)

# Functions
def fix_orientation(sub, subNumFull, versionNum):
    os.system("fslreorient2std %s/func/Orientation_To_Fix/%s_task-emotion-regulation_run-%s_bold.nii.gz"%(sub, subNumFull, versionNum) + " %s/func/%s_task-emotion-regulation_run-%s_bold.nii.gz"%(sub, subNumFull, versionNum))

def copy_bold_files(sub, subNum, versionNum):
    shutil.copy2("/%s/func/Orientation_To_Fix/%s_task-emotion-regulation_run-%s_bold.json"%(sub, subNumFull, versionNum), "/%s/func/"%(sub))

def fix_resting_orientation(sub, subNum):
    os.system("fslreorient2std %s/func/Orientation_To_Fix/%s_task-rest_bold.nii.gz"%(sub, subNumFull) + " %s/func/%s_task-rest_bold.nii.gz"%(sub, subNumFull))

def copy_resting_files(sub, subNum):
    shutil.copy2("/%s/func/Orientation_To_Fix/%s_task-rest_bold.json"%(sub, subNumFull), "/%s/func/"%(sub))

def fix_dti_orientation(sub, subNum):
    os.system("fslreorient2std %s/dwi/Orientation_To_Fix/%s_dwi.nii.gz"%(sub, subNumFull) + " %s/dwi/%s_dwi.nii.gz"%(sub, subNumFull))

def copy_dti_files(sub, subNum):
    shutil.copy2("/%s/dwi/Orientation_To_Fix/%s_dwi.json"%(sub, subNumFull), "/%s/dwi/"%(sub))

if __name__ == "__main__":
    for sub in subPath:
        subNumFull = sub.split('/')[5]
        subNum = subNumFull[4:7]

        if os.path.isdir("%s/func/Orientation_To_Fix/"%(sub)) == True:
            print ("----------Fixing functional scan orientations for " + subNum + "----------")
            fix_orientation(sub, subNumFull, "01")
            fix_orientation(sub, subNumFull, "02")
            fix_orientation(sub, subNumFull, "03")
            fix_resting_orientation(sub, subNum)

            if os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-emotion-regulation_run-01_bold.nii.gz") == True:
                copy_bold_files(sub, subNum, "01")
                copy_bold_files(sub, subNum, "02")
                copy_bold_files(sub, subNum, "03")
                copy_resting_files(sub, subNum)
                shutil.rmtree("%s/func/Orientation_To_Fix/"%(sub))


        if os.path.isdir("%s/dwi/Orientation_To_Fix"%(sub)) == True:
            print ("----------Fixing dwi orienatation for " + subNum + "----------")
            fix_dti_orientation(sub, subNum)
            
            if os.path.isfile("%s/dwi/sub-"%(sub) + subNum + "_dwi.nii.gz") == True:
                copy_dti_files(sub, subNum)
                # BVECs and BVALSs created here are not usable
                #shutil.copy2("/%s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.bval", "/%s/dwi/"%(sub))
                #shutil.copy2("/%s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.bvec", "/%s/dwi/"%(sub))
                shutil.rmtree("%s/dwi/Orientation_To_Fix/"%(sub))   
