#!/bin/python 
# First Created: 6/14/2017
# Last Updated: 6/14/2017
# Author: D.Lee
# Purpose: For all functional data --> fix the orientations

import glob
import os

masterPath = '/study/midus3/processed_data/my_dataset'
subPath = glob.glob('%s/sub-[0-9][0-9][0-9]'%(masterPath))

for sub in subPath:
	subNum = sub[44:47]
	
	print "MIDUS3 subject " + subNum + ".................Fixing Orientations................."
	
	os.chdir("%s/func/"%(sub))
	os.makedirs("Orientation_Fixed")
	os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-ER_run-1_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-ER_run-1_bold")
	os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-ER_run-2_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-ER_run-2_bold")
	os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-ER_run-3_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-ER_run-3_bold")
	os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-rest_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-rest_bold_brain")
	
	# Maybe I can count the diretoreis?
	# And whenever there is one more directory....counter increases....then 