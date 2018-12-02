#!/bin/python3

# Author: David SB Lee
# First Compiled: 12/14/17
# Purpose: Motion Assesement of BOLD with FD > 0.9 & FD > 0.5 criteria

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
    # Create func directory if it doesnbold't exist
    os.makedirs("%s/sub-MRID-%s/func"%(analysis_path, subId), exist_ok = True)

    # Create QA, (delete and re-create, basically overwriting)
    os.system("rm -rf %s/sub-MRID-%s/func/QA"%(analysis_path, subId))
    os.makedirs("%s/sub-MRID-%s/func/QA"%(analysis_path, subId), exist_ok = True)

    # Html with motion summaries, one for each subject (I'll cat them later)
    outhtml = "%s/sub-MRID-%s/func/QA/motion_task.html"%(analysis_path, subId)
    outhtml2 = "%s/sub-MRID-%s/func/QA/motion_rest.html"%(analysis_path, subId)
    #os.system("rm -f %s"%(outhtml))

    for resting in restingfiles:
        #print (resting)

        # Strip off .nii.gz from file name (makes code below easier)
        resting_no_ext = resting[:-7]
        #print(resting_no_ext)
        runNumResting = "4"
        print (runNumResting)

         # Extract output Path
        extendedPathResting = resting[41:90]

        os.system("fsl_motion_outliers -i %s/%s_mod -o %s/sub-MRID-%s/func/QA/%s_confound_rest_with_FD_0.2.txt --fd --thresh=0.2 -p %s/sub-MRID-%s/func/QA/fd_plot_FD_0.2_%s -v > %s/sub-MRID-%s/func/QA/outlier_output_FD_0.2_%s.txt"%(analysis_path, extendedPathResting, analysis_path, subId, runNumResting, analysis_path, subId, runNumResting, analysis_path, subId, runNumResting))
        os.system("cat %s/sub-MRID-%s/func/QA/outlier_output_FD_0.2_%s.txt >> %s"%(analysis_path, subId, runNumResting, outhtml2))
        os.system("echo '<br><br> FD plot %s %s <br><IMG BORDER=0 SRC=%s/sub-MRID-%s/func/QA/fd_plot_FD_0.2_%s.png WIDTH=100%s></BODY></HTML> <p>==========================================================<p>' >> %s"%(subId, runNumResting, analysis_path, subId, runNumResting,'%', outhtml2))
        if os.path.isfile("%s/sub-MRID-%s/func/QA/%s_confound_rest_with_FD_0.2.txt"%(analysis_path, subId, runNumResting))==False:
            os.system("touch %s/sub-MRID-%s/func/QA/%s_confound_rest_with_FD_0.2.txt"%(analysis_path, subId, runNumResting))

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

        # Asses Motion
        os.system("fsl_motion_outliers -i %s/%s_mod -o %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.9.txt --fd --thresh=0.9 -p %s/sub-MRID-%s/func/QA/fd_plot_FD_0.9_%s -v > %s/sub-MRID-%s/func/QA/outlier_output_FD_0.9_%s.txt"%(analysis_path, extendedPathBold, analysis_path, subId, runNum, analysis_path, subId, runNum, analysis_path, subId, runNum))
        os.system("cat %s/sub-MRID-%s/func/QA/outlier_output_FD_0.9_%s.txt >> %s"%(analysis_path, subId, runNum, outhtml))
        os.system("echo '<br><br> FD plot %s %s <br><IMG BORDER=0 SRC=%s/sub-MRID-%s/func/QA/fd_plot_FD_0.9_%s.png WIDTH=100%s></BODY></HTML> <p>==========================================================<p>' >> %s"%(subId, runNum, analysis_path, subId, runNum,'%', outhtml))
        if os.path.isfile("%s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.9.txt"%(analysis_path, subId, runNum))==False:
            os.system("touch %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.9.txt"%(analysis_path, subId, runNum))

        os.system("fsl_motion_outliers -i %s/%s_mod -o %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.5.txt --fd --thresh=0.5 -p %s/sub-MRID-%s/func/QA/fd_plot_FD_0.5_%s -v > %s/sub-MRID-%s/func/QA/outlier_output_FD_0.5_%s.txt"%(analysis_path, extendedPathBold, analysis_path, subId, runNum, analysis_path, subId, runNum, analysis_path, subId, runNum))
        os.system("cat %s/sub-MRID-%s/func/QA/outlier_output_FD_0.5_%s.txt >> %s"%(analysis_path, subId, runNum, outhtml))
        os.system("echo '<br><br> FD plot %s %s <br><IMG BORDER=0 SRC=%s/sub-MRID-%s/func/QA/fd_plot_FD_0.5_%s.png WIDTH=100%s></BODY></HTML> <p>==========================================================<p>' >> %s"%(subId, runNum, analysis_path, subId, runNum,'%', outhtml))
        if os.path.isfile("%s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.5.txt"%(analysis_path, subId, runNum))==False:
            os.system("touch %s/sub-MRID-%s/func/QA/%s_confound_task_with_FD_0.5.txt"%(analysis_path, subId, runNum))
