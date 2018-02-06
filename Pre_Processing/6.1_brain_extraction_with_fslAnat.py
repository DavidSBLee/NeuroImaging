#!/bin/python3

# Author: # Author: David SB Lee
# First Compiled: 10/24/2017
# Purpose: Brain Extraction(Skull-Stripping) and Mask Creation using fslanat as an alternative to "Bet"

# Things to change when runing on different data set
	# 1. all paths
	# 2. all splits
	# 3. Choose bet setting that best fits your data

# Set global variables (paths)
import glob
import os
import os.path

path = '/study/midus3/processed_data/MIDUS3_Imaging'
subPath = glob.glob('%s/sub-[0-9][0-9][0-9]/anat'%(path))
analysis_path = '/study/midus3/processed_data/MIDUS3_Imaging_Analysis'

if __name__ == "__main__":
	for sub in subPath:
		subNumFull = sub.split('/')[5]
		subNum = subNumFull[4:7]
		if os.path.isfile("%s/%s/anat/%s_T1w_fslanat_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == True:
			print ("----------Brain Extraction Already Completed for", subNum, "----------")

		elif os.path.isfile("%s/%s/anat/%s_T1w_fslanat_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == False: 
			os.makedirs("%s/%s/anat"%(analysis_path, subNumFull), exist_ok = True)
			print ("----------Brain Extraction Initiated for", subNum, "----------")
			# FSLANAT function
			os.system("fsl_anat -i %s/%s_T1w.nii.gz -o %s/%s/anat/TMPDIR --noseg --nosubcortseg"%(sub, subNumFull, analysis_path, subNumFull))
			# Copying the ones I need for analysis and delete the rest
			os.system("cp %s/%s/anat/TMPDIR.anat/T1_biascorr.nii.gz %s/%s/anat/%s_T1w_fslanat.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
			os.system("cp %s/%s/anat/TMPDIR.anat/T1_biascorr_brain.nii.gz %s/%s/anat/%s_T1w_fslanat_brain.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
			os.system("cp %s/%s/anat/TMPDIR.anat/T1_biascorr_brain_mask.nii.gz  %s/%s/anat/%s_T1w_fslanat_brain_mask.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
			os.system("rm -rf %s/%s/anat/TMPDIR.anat"%(analysis_path, subNumFull))

