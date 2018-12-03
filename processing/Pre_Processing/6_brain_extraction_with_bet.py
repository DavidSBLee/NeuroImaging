#!/bin/python3

# Author: # Author: David SB Lee
# First Compiled: 10/16/2017

# Things to change when runing on different data set
	# 0. USE PYTHON3
	# 1. all paths
	# 2. all splits
	# 3. Choose bet setting that best fits your data
	# 4. Make sure to copy over the original T1 to analysis folder

import glob
import os
import os.path

# Set global variables (paths)
path = '/study/midus3/processed_data/MIDUS3_Imaging'
subPath = glob.glob('%s/sub-[0-9][0-9][0-9]/anat'%(path))
analysis_path = '/study/midus3/processed_data/MIDUS3_Imaging_Analysis'

if __name__ == "__main__":
	for sub in subPath:
		subNumFull = sub.split('/')[5]
		subNum = subNumFull[4:7]
		
		if os.path.isfile("%s/%s/anat/%s_T1w_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == True:
			print ("----------Brain Extraction Already Completed for", subNum, "----------")

		elif os.path.isfile("%s/%s/anat/%s_T1w_brain.nii.gz"%(analysis_path, subNumFull, subNumFull)) == False:
			os.makedirs("%s/%s/anat"%(analysis_path, subNumFull), exist_ok = True)
			print ("----------Brain Extraction Initiatd for", subNum, "----------")
			# The nuemric "0.3" may be changed to 0.35 or other numbers to account for eye coverage
			os.system("bet %s/%s_T1w.nii.gz %s/%s/anat/%s_T1w_brain.nii.gz -m -f 0.3 -R"%(sub, subNumFull, analysis_path, subNumFull, subNumFull))

