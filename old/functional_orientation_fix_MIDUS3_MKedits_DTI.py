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
#MK: If we're going to build in a check (i.e., to make sure we aren't           duplicating scans that have already been fixed), we should add it here.         That way, we can visually look at which subjects are being processed and        make sure that it makes sense (e.g., if we see sub-001, we know                 something is wrong!). Or, maybe we shouldn't do this for the whole thing, but by each scan, since some Pp will not have all scans.
	#print "MIDUS3 subject " + subNum + ".................Fixing Orientations................."
	
	#os.chdir("%s/func/"%(sub))
	#os.makedirs("Orientation_Fixed")
	#os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-ER_run-1_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-ER_run-1_bold")
	#os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-ER_run-2_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-ER_run-2_bold")
	#os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-ER_run-3_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-ER_run-3_bold")
	#os.system("fslreorient2std %s/func/sub-"%(sub) + subNum + "_task-rest_bold %s/func/Orientation_Fixed/sub-"%(sub) + subNum + "_task-rest_bold_brain")
        
#MK-Edits to include dwi/dti. Currently placing files in 'Orientation_Fixed' folder (as with func scans), but may want to just replace old files or place 'fixed' files in same directory w/ new name.
        if os.path.isdir("%s/dwi"%(sub)) == True and os.path.isfile("%s/dwi/Orientation_Fixed/sub-"%(sub) + subNum + "_dwi.nii.gz") == False:
                print "Converting dwi for " +  sub
                os.chdir("%s/dwi/"%(sub))
                os.makedirs("Orientation_Fixed")
                os.system("fslreorient2std %s/dwi/sub-"%(sub) + subNum + "_dwi %s/dwi/Orientation_Fixed/sub-"%(sub) + subNum + "_dwi")
	
	# Maybe I can count the diretoreis?
	# And whenever there is one more directory....counter increases....then
