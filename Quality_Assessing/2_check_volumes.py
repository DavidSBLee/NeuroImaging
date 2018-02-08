#!/bin/python3

# Author: David SB Lee
# First Compiled: 11/14/17
# Purpose: Compiles the #of TRs for BOLD data (trimmed & untrimmed) and outputs a .txt

import glob
import os
import sys
import subprocess

# Overwrites an output .txt file
f = open('/study4/midusref/midusref_imaging_public/QA/check_volumes1.txt', 'w')
sys.stdout = f

path = '/study4/midusref/midusref_imaging_public/'
analysis_path = '/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis/'
boldfiles = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-emotion-regulation_run-[0-9]_bold.nii.gz'%(path))
trimmedBoldFiles = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-emotion-regulation_run-[0-9]_mod.nii.gz'%(analysis_path))

restfiles = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-rest_bold.nii.gz'%(path))
trimmedRestFiles = glob.glob("%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-rest_bold_mod.nii.gz"%(analysis_path))

def run(command, volumes):
    cmd_args_lst = command.split()
    #print("Executing : ", cmd_args_lst)
    ex = subprocess.Popen(cmd_args_lst, stdout=subprocess.PIPE)
    out, err = ex.communicate()
    decodedOut = int(out[0:3].decode('utf-8'))
    if int(out[0:3].decode('utf-8')) != int(volumes):
        print(subNum + " " + runNum)
        print("Bad:Irregular Number of Volumes")
        print("Volumes: " + str(decodedOut) + "\n")
    elif int(out[0:3].decode('utf-8')) == int(volumes):
        print (subNum + " " + runNum)
        print("Volumes: " + str(decodedOut) + "\n")

if __name__ == "__main__":

    print ("----------Volumes of Bold Files----------")
    for file in boldfiles:
        subNum = file[70:75]
        runNum = file[100:105]
        run("fslnvols %s"%(file), 231)
    print ("")

    print ("----------Volumes of Trimmed Bold Files----------")
    for trimmed in trimmedBoldFiles:
        subNum = trimmed[96:101]
        runNum = trimmed[126:131] + "_Trimmed"
        run("fslnvols %s"%(trimmed), 227)
    print ("")

    print ("----------Volumes of Resting State Files----------")
    for restfile in restfiles:
        subNum = restfile.split('-')[2][0:5]
        runNum = "Resting"
        run("fslnvols %s"%(restfile), 240)
    print ("")

    print ("----------Volumes of Trimmed Resting State Files----------")
    for trimmedrest in trimmedRestFiles:
        subNum = trimmedrest.split('-')[2][0:5]
        runNum = "Resting_Trimmed"
        run("fslnvols %s"%(trimmedrest), 236)
    print ("")

f.close()
