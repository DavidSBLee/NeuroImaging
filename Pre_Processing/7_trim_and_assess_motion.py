#!/bin/python3
# Things this script does
# (1) Trims first 4 volumes off of BOLD data
# (2) Motion Assesement


import glob
import os
import sys
import subprocess

# Permissions
#os.system("umask 002")

# Set global Path
path = '/study/midus3/processed_data/MIDUS3_Imaging'
analysis_path = '/study/midus3/processed_data/MIDUS3_Imaging_Analysis'
QA_path = '/study/midus3/processed_data/QA'

# Takes an input argument such as "001"
#print ("Script Name:", sys.argv[0])
print ("Input Subject Number:", sys.argv[1] )
subId = sys.argv[1]

boldfiles = glob.glob('%s/sub-%s/func/*run*bold.nii.gz'%(path, subId))
restingfiles = glob.glob('%s/sub-%s/func/*rest*bold.nii.gz'%(path, subId))

# Create func directory if it doesn't exist
os.makedirs("%s/sub-%s/func"%(analysis_path, subId), exist_ok = True)

# Create QA, (delete and re-create, basically overwriting)
os.system("rm -rf %s/sub-%s/func/QA"%(analysis_path, subId))
os.system("mkdir %s/sub-%s/func/QA"%(analysis_path, subId))

# Html with motion summaries, one for each subject (I'll cat them later)
outhtml = " %s/sub-%s/func/QA/motion.html"%(analysis_path, subId)
os.system("rm -f %s"%(outhtml))

# .txt for any subjects with high motion
out_bad_bold_list = " %s/MIDUS3_subjects_Task_high_motion_57_scrub.txt"%(QA_path)
out_bad_rest_list = "%s/MIDUS3_subjects_Rest_high_motion_59_scrub..txt"%(QA_path)

for bold in boldfiles:
    #print (bold)
    # Strip off .nii.gz from file name (makes code below easier)
    bold_no_ext = bold[:-7]
    #print(bold_no_ext)
    runNum = bold_no_ext.split("_")[4]
    runNum = runNum.split("-")[1]
    #print (runNum)

    # Extract output Path
    extendedPath = bold[44:99]

    # Trim 4 Volumes
    print ("----------Trimming Frist 4 Volumes for run-%s----------"%(runNum))
    os.system("fslroi %s %s/%s_mod 4 -1"%(bold_no_ext, analysis_path, extendedPath))

    # Asses Motion
    print ("----------Assessing Motion for run-%s----------"%(runNum))
    os.system("fsl_motion_outliers -i %s/%s_mod -o %s/sub-%s/func/QA/%s_confound.txt --fd --thresh=0.5 -p %s/sub-%s/func/QA/fd_plot_%s -v > %s/sub-%s/func/QA/outlier_output_%s.txt"%(analysis_path, extendedPath, analysis_path, subId, runNum, analysis_path, subId, runNum, analysis_path, subId, runNum))
    os.system("cat %s/sub-%s/func/QA/outlier_output_%s.txt >> %s"%(analysis_path, subId, runNum, outhtml))
    os.system("echo '<br><br> FD plot %s %s <br><IMG BORDER=0 SRC=%s/sub-%s/func/QA/fd_plot_%s.png WIDTH=100%s></BODY></HTML> <p>==========================================================<p>' >> %s"%(subId, runNum, analysis_path, subId, runNum,'%', outhtml))

    # Change Permissions for Output
    #os.system("chmod +775 -R {}/sub-{}/func".format(analysis_path, subId))

    # Create empty counfound file in case of "no motion outlier" b/c fsl_motion_outlier function does NOT create one for "no motion outlier"
    if os.path.isfile("%s/sub-%s/func/QA/%s_confound.txt"%(analysis_path, subId, runNum))==False:
      os.system("touch %s/sub-%s/func/QA/%s_confound.txt"%(analysis_path, subId, runNum))


for resting in restingfiles:
    #print (resting)

    # Strip off .nii.gz from file name (makes code below easier)
    resting_no_ext = resting[:-7]
    #print(resting_no_ext)

    runNumResting = "04"
    #print (runNumResting)

     # Extract output Path
    extendedPathResting = resting[44:79]

    # Trim 4 Volumes
    print ("----------Trimming Frist 4 Volumes for resting-state-fMRI----------")
    os.system("fslroi %s %s/%s_mod 4 -1"%(resting_no_ext, analysis_path, extendedPathResting))

    # Assess Motion
    print ("----------Assessing Motion for resting-state-fMRI----------")
    os.system("fsl_motion_outliers -i %s/%s_mod -o %s/sub-%s/func/QA/%s_confound.txt --fd --thresh=0.2 -p %s/sub-%s/func/QA/fd_plot_%s -v > %s/sub-%s/func/QA/outlier_output_%s.txt"%(analysis_path, extendedPathResting, analysis_path, subId, runNumResting, analysis_path, subId, runNumResting, analysis_path, subId, runNumResting))
    os.system("cat %s/sub-%s/func/QA/outlier_output_%s.txt >> %s"%(analysis_path, subId, runNumResting, outhtml))
    os.system("echo '<br><br> FD plot %s %s <br><IMG BORDER=0 SRC=%s/sub-%s/func/QA/fd_plot_%s.png WIDTH=100%s></BODY></HTML> <p>==========================================================<p>' >> %s"%(subId, runNumResting, analysis_path, subId, runNumResting,'%', outhtml))

    #Change Permissions for Output
    #os.system("chmod +775 -R {}/sub-{}/func".format(analysis_path, subId))

    # Create empty counfound file in case of "no motion outlier" b/c fsl_motion_outlier function does NOT create one for "no motion outlier"
    if os.path.isfile("%s/sub-%s/func/QA/%s_confound.txt"%(analysis_path, subId, runNumResting))==False:
      os.system("touch %s/sub-%s/func/QA/%s_confound.txt"%(analysis_path, subId, runNumResting))

print ("----------Trim and Motion Assessment for %s complete----------"%(subId))
