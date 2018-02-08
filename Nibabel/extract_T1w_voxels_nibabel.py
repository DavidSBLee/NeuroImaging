#!/bin/python3

# Author: David SB Lee
# First Compiled: 02/08/18
# Purpose: Extract T1w voxel intensities by coordinate

# Things to change when runing on different data set
	# 1. all paths
	# 2. all splits

import nibabel as nib
import glob

# Set global variables (paths)
path = "/path/to/T1w.niig.gz"

if __name__ == "__main__":
	# Put the images in a list
	files = sorted(glob.glob(file))

	# Create a list of subject numbers
	subNumList = [file.split('/')[4] for file in files]
	# If you don't want to use list comprehension
	subNumList = []
	for file in files:
		subNum = file.split('/')[8]
		subNumList.append(subNum)
	# If you want to add a label to the list
	subNumList.insert(0, 'SubjectID')
	
	# Put voxel coordinates and inetnsities in a separate
	for file in files:

		# Load T1w as nibabel image
		img = nib.load(file)
		data = img.get_data()

		# Check data dimensions
		img.shape
		data.shape

		intensity_list= []
		coordinate_list = []

		# Start extratcion
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				for k in range(img.shape[2]):
					x = str(i + 1)
					y = str(j + 1)
					z = str(k + 1)
					each_coordinate = (x,y,z)
					each_coordinate = " ".join(each_coordinate)
					coordinate_list.append(each_coordinate)
					intensity_list.append(data[i][j][k])
					print (each_coordinate, data[i][j][k])
