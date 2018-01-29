#!/bin/python3

# Author: # Author: David SB Lee
# First Compiled: 12/21/2017
# Last Updated: 1/9/18 (Mike Kelly)
# Updated Content: Script will now create masks for T1w_2s in addition to T1ws
# Purpose: Skull Strip and Mask Creation using fslanat b/c bet didnt work too well

# Things to change when runing on different data set
	# 1. all paths
	# 2. all splits

import glob
import os
import os.path

path = '/study4/midusref/midusref_imaging_public'
subPath = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/anat'%(path))
analysis_path = '/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis'

for sub in subPath:
	subNumFull = sub.split('/')[4]
	subNum = subNumFull[9:14]
	if os.path.isfile("%s/%s/anat/%s_T1w_fslanat_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == True:
		print ("----------Brain Extraction Already Completed for", subNum, "----------")

	elif os.path.isfile("%s/%s/anat/%s_T1w_fslanat_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == False:
		os.makedirs("%s/%s/anat"%(analysis_path, subNumFull), exist_ok = True)
		#os.system("bet %s/%s_T1w.nii.gz %s/%s_T1w_brain.nii.gz -R -m"%(sub, subNumFull, sub, subNumFull))
		print ("----------Brain Extraction Initiated for", subNum, "----------")
		os.system("fsl_anat -i %s/%s_T1w.nii.gz -o %s/%s/anat/TMPDIR --noseg --nosubcortseg"%(sub, subNumFull, analysis_path, subNumFull))
		os.system("cp %s/%s/anat/TMPDIR.anat/T1_biascorr.nii.gz %s/%s/anat/%s_T1w_fslanat.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("cp %s/%s/anat/TMPDIR.anat/T1_biascorr_brain.nii.gz %s/%s/anat/%s_T1w_fslanat_brain.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("cp %s/%s/anat/TMPDIR.anat/T1_biascorr_brain_mask.nii.gz  %s/%s/anat/%s_T1w_fslanat_brain_mask.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("rm -rf %s/%s/anat/TMPDIR.anat"%(analysis_path, subNumFull))

for sub in subPath:
	subNumFull = sub.split('/')[4]
	subNum = subNumFull[9:14]
	if os.path.isfile("%s/%s/anat/%s_T1w_2_fslanat_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == True:
		print ("----------Brain Extraction Already Completed for", subNum, "----------")

	elif os.path.isfile("%s/%s/anat/%s_T1w_2_fslanat_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == False:
		os.makedirs("%s/%s/anat"%(analysis_path, subNumFull), exist_ok = True)
		#os.system("bet %s/%s_T1w.nii.gz %s/%s_T1w_brain.nii.gz -R -m"%(sub, subNumFull, sub, subNumFull))
		print ("----------Brain Extraction Initiated for", subNum, "----------")
		os.system("fsl_anat -i %s/%s_T1w_2.nii.gz -o %s/%s/anat/TMPDIR2 --noseg --nosubcortseg"%(sub, subNumFull, analysis_path, subNumFull))
		os.system("cp %s/%s/anat/TMPDIR2.anat/T1_biascorr.nii.gz %s/%s/anat/%s_T1w_2_fslanat.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("cp %s/%s/anat/TMPDIR2.anat/T1_biascorr_brain.nii.gz %s/%s/anat/%s_T1w_2_fslanat_brain.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("cp %s/%s/anat/TMPDIR2.anat/T1_biascorr_brain_mask.nii.gz  %s/%s/anat/%s_T1w_2_fslanat_brain_mask.nii.gz"%(analysis_path, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("rm -rf %s/%s/anat/TMPDIR2.anat"%(analysis_path, subNumFull))
