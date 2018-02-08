#!/usr/bin/env python3

# Author: David SB Lee
# First Compiled: 02/08/18
# Purpose: extract voxel coordinates and corresponding intensities of T1W image

# Things to change when runing on different data set
# 1. all paths
# 2. all splits

import nibabel as nib
import glob

# Set global variables (paths)
path = "/Users/SB/Desktop/[0-9][0-9][0-9][0-9][0-9]/*T1w.nii.gz"

# Put T1w into a list
files = sorted(glob.glob(path))

# Construct a list of subject numbers
subNumList = [file.split('/')[4] for file in files]
subNumList
# If you don't want list comprehension use below
"""
subNumList = []
for file in files:
	subNum = file.split('/')[8]
	subNumList.append(subNum)
"""
# If a label for the list is needed
#subNumList.insert(0, 'SubjectID')

# Construct a list for coordinates and intensities respectively
for file in files:

	#Load each T1w as nibabel image and access 
	img = nib.load(file)
	data = img.get_data()

	# Check data dimensions
	img.shape
	data.shape

	intensity_list= []
	coordinate_list = []

	# Intesnity and coordinate Extraction
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			for k in range(img.shape[2]):
				x = str(i + 1)
				y = str(j + 1)
				z = str(k + 1)

				each_coordinate = (x,y,z)
				each_coordinate = " ".join(each_coordinate)
				print (each_coordinate, data[i][j][k])

				coordinate_list.append(each_coordinate)
				intensity_list.append(data[i][j][k])



