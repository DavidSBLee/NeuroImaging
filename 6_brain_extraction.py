#!/bin/python

# First Compiled: 10/16/2017
# Last Updated: 
# Updated Content: () 
# Purpose: Skull Strip and Mask Creation

# Things to change when runing on different data set
	# 1. all paths
	# 2. all splits
	# 3. Choose bet setting that best fits your data

import glob
import os
import os.path

path = '/study/midus3/processed_data/MIDUS3_Imaging/'
subPath = glob.glob('%s/sub-[0-9][0-9][0-9]/anat'%(path))

for sub in subPath:
	subNumFull = sub.split('/')[5]
	subNum = subNumFull[4:7]
	if os.path.isfile("%s/%s_T1w_brain.nii.gz"%(sub, subNumFull)) == True:
		print "----------Brain Extraction Already Completed for", subNum, "----------"

	elif os.path.isfile("%s/%s_T1w_brain.nii.gz"%(sub, subNumFull)) == False:
		# If bet 
		os.system("bet %s/%s_T1w.nii.gz %s/%s_T1w_brain.nii.gz -R -m"%(sub, subNumFull, sub, subNumFull))

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