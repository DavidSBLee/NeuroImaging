#!/bin/python3

# Author: David SB Lee
# First Compiled: 12/12/2017
# Purpose: Resample a nifti image with a new voxel dimension

# Things to change when running on different data set
# 1. All Paths

import os

# Resample a template image with 1x1x1 voxel dimension
# Change the voxel dimension of your choice
# The change in the voxel dimension will change the number of total dimensions
os.system("ResampleImage 3 /path/to/template /path/to/resampled/template 1x1x1")
