#!/bin/python3

# Author: # Author: David SB Lee
# First Compiled: 12/21/2017
# Last Updated: 
# Updated Content: 
# Updated Content: 
# Purpose: Skull Strip and create Mask using bet

# Things to change when runing on different data set
	# 0. USE PYTHON3
	# 1. all paths
	# 2. all splits
	# 3. Choose bet setting that best fits your data, Here it's 0.3

import glob
import os
import os.path

path = '/study4/midusref/midusref_imaging_public'
subPath = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/anat'%(path))
analysis_path = '/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis'

# This part is for T1w
for sub in subPath:
	subNumFull = sub.split('/')[4]
	subNum = subNumFull[9:14]
	
	if os.path.isfile("%s/%s/anat/%s_T1w_0.3_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == True:
		print ("----------Brain Extraction for T1w Already Completed for", subNum, "----------")

	elif os.path.isfile("%s/%s/anat/%s_T1w_0.3_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == False:
		#os.system("bet %s/%s_T1w.nii.gz %s/%s_T1w_brain.nii.gz -R -m"%(sub, subNumFull, sub, subNumFull))
		os.makedirs("%s/%s/anat"%(analysis_path, subNumFull), exist_ok = True)
		"""
		if not os.path.exists("%s/%s/anat"%(analysis_path, subNumFull)):
			"----------Creating anat Diretory----------"
			os.makedirs("%s/%s/anat"%(analysis_path, subNumFull))
		"""

		print ("----------Brain Extraction for T1w Initiatd for", subNum, "----------")
		#os.system("bet %s/%s_T1w.nii.gz %s/%s/anat/%s_T1w_0.3_brain.nii.gz -R -m"%(sub, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("bet %s/%s_T1w.nii.gz %s/%s/anat/%s_T1w_0.3_brain.nii.gz -m -f 0.3 -R"%(sub, subNumFull, analysis_path, subNumFull, subNumFull))

# This part is for T1w_2
for sub in subPath:
	subNumFull = sub.split('/')[4]
	subNum = subNumFull[9:14]

	if os.path.isfile("%s/%s/anat/%s_T1w_2_0.3_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == True:
		print ("----------Brain Extraction for T1w_2 Already Completed for", subNum, "----------")
	
	elif os.path.isfile("%s/%s/anat/%s_T1w_2_0.3_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == False:
		#os.system("bet %s/%s_T1w_2.nii.gz %s/%s_T1w_2_brain.nii.gz -R -m"%(sub, subNumFull, sub, subNumFull))
		os.makedirs("%s/%s/anat"%(analysis_path, subNumFull), exist_ok = True)
		"""
		if not os.path.exists("%s/%s/anat"%(analysis_path, subNumFull)):
			"----------Creating anat Diretory----------"
			os.makedirs("%s/%s/anat"%(analysis_path, subNumFull))
		"""

		print ("----------Brain Extraction for T1w_2 Initiatd for", subNum, "----------")
		#os.system("bet %s/%s_T1w_2.nii.gz %s/%s/anat/%s_T1w_2_0.3_brain.nii.gz -R -m"%(sub, subNumFull, analysis_path, subNumFull, subNumFull))
		os.system("bet %s/%s_T1w_2.nii.gz %s/%s/anat/%s_T1w_2_0.3_brain.nii.gz -m -f 0.3 -R"%(sub, subNumFull, analysis_path, subNumFull, subNumFull))

### Jeanette's comments ###

# If you want to try out freesurfer, here's the command line code that
# you can adapt to the loop via os.system.  Mostly, you'll need to put actual paths in.

# I think it needs unzipped files (double check this)
# gunzip path/to/anatomy/highres001.nii.gz

# This takes a while (~15 minutes?)
# recon-all -autorecon1 -i path/to/anatomy/highres001.nii -subjid autorecon   -sd /path/to/anatomy/
# This will actually create the skull stripped brain (you won't get a mask)

#mri_convert  /path/to/anatomy/autorecon/mri/brainmask.mgz  --reslice_like /path/to/anatomy/highres001.nii /path/to/anatomy/highres001_brain.nii

# I'm deleting the files it created
#rm -rf /path/to/anatomy/autorecon/

# zipping up the skull stripped image and original image
#gzip /path/to/anatomy/*.nii