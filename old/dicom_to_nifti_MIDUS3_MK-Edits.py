#!/bin/python
# First Created: 4/11/2017
# Last Updated: 6/19/2017--Updated Loops for fmap. Script had been breaking b/c it was trying to create fmap folder twice. Added loop to check if folder exists already prior to creating it--MK
# AUTHOR: D.Lee
# Purpose: When new raw scan data --> convert DICOMs to NIFTIs

import os
import glob

# raw DICOMs in an array 
rawDir = glob.glob("/study/midus3/raw-data/[0-9][0-9][0-9]") # or just wildcard it
dicoms = set([int(raw.split('/')[4][0:]) for raw in rawDir]) # extracts INTEGERS w/o "0"
#dicoms.sort()
print dicoms


"""
dicoms = []
for raw in rawDir:
	split = raw.split('/')
	dicoms.append(int(split[4][0:]))
dicoms.sort() # or x = sorted(dicoms)
print dicoms
"""
	
# NIFTIs
niftiDir = glob.glob("/study/midus3/processed_data/my_dataset/sub-[0-9][0-9][0-9]")
niftis = set([int(nifti.split('/')[5][4:7]) for nifti in niftiDir]) # in python the set is called hash table
#niftis.sort()
print niftis

"""
niftis = []
for nifti in list(niftiDir):
	splitNifti = nifti.split('/')
	niftiName = splitNifti[5]
	subNumNifti = niftiName[4:7]
	print subNumNifti # this prints p01 etc.
"""	

# Checking and Processing	

for f in dicoms:
	if f not in niftis:
		name = str(f) # string casting
		var = ["0" for _ in range(3-len(name))] + [name] # var = ["0"]*(3-len(name)) (do this b/c just printing f will give me numbers without 0)
		subNum = ''.join(var) # join the numbers without space!
		print "Subject Number: " + subNum # This is for me to check 
		
		dicomFolderName = subNum + "_unprocessed_dicoms"
		niftiFolderName = "sub-" + subNum
		dicomPath = "/study/midus3/processed_data/dicomdir/"
		niftiPath = "/study/midus3/processed_data/my_dataset/"

		os.chdir(dicomPath)
		os.makedirs(dicomFolderName) # Create ###_unprocessed_dicoms folders
		os.chdir(dicomFolderName)

		direc = glob.glob("/study/midus3/raw-data/" + subNum + "/dicoms/*/*.tgz")
		for d in direc:
			scanName = d.split('/')[6][6:] # Extract scanname
			#dcmConvert = "dcm2niix -f " + niftiFolderName+ "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/anat/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName
 			
			#if "LOCALIZER" not in scanName: # Skip Localizers
			if "T1w" in scanName:
				#os.chdir("/stduy/midus3/processed_data/unprocessed_dicoms/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				os.makedirs(niftiFolderName)
				os.chdir(niftiFolderName)
				os.makedirs("anat")
				os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/anat/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print "----------" + scanName + " Conversion Complete----------"

			if "task-ER_run-1_bold" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				os.makedirs("func")
				os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/func/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print  "----------" + scanName + " Conversion Complete----------"

			if "task-ER_run-2_bold" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				#os.makedirs("func")
				os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/func/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print  "----------" + scanName + " Conversion Complete----------"

			if "task-ER_run-3_bold" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				#os.makedirs("func")
				os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/func/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print  "----------" + scanName + " Conversion Complete----------"

			if "task-rest_bold" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				#os.makedirs("func")
				os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/func/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print  "----------" + scanName + " Conversion Complete----------"

			if "dwi" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				os.makedirs("dwi")
				os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/dwi/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print  "----------" + scanName + " Conversion Complete----------"

			if "WATER__fmap" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				if os.path.isdir("%s/%s/fmap/"%(niftiPath, niftiFolderName)) == False: # If fmap folders do NOT exist...create famp
				    os.makedirs("fmap")
				
				os.system("dcm2niix -f " + niftiFolderName + "_magnitude" + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/fmap/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print  "----------" + scanName + " Conversion Complete----------"
			
			if "FieldMap__fmap" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				if os.path.isdir("%s/%s/fmap/"%(niftiPath, niftiFolderName)) == False: # If fmap folders do NOT exist...create famp
				    os.makedirs("fmap")
				
				os.system("dcm2niix -f " + niftiFolderName + "_fieldmap" + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/fmap/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
				print  "----------" + scanName + " Conversion Complete----------"
			
			if "asl" in scanName:
				os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
				os.makedirs(scanName)
				os.chdir(scanName)
				os.system("tar -xvzf " + d) # unzip .tgz's
				os.chdir(niftiPath)
				#os.makedirs("sub-" + subNum)
				os.chdir(niftiFolderName)
				os.makedirs("asl")
				os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/my_dataset/" + "sub-" + subNum + "/asl/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
			
print "----------" + subNum + " Coversion Complete----------"

		# Things to Fix
		# 1. CHMOD the whole thing afterwards
		# 2. One problem: the script breaks when there already is "###_unprocessed_dicoms"
		# 3. Delete DICOM folders? b/c they take up space. I can put it in at the end of each loop 
		# 4. What's better than if loop? I might use switch???

		# Some Extra Codes that might* be useful down the road
        # var.append(scanName)
        # if not os.path.exists(scanName) --> I need this checking method in case it overwrites
		
		# How to use dcm commands
		#dcm2niix -f "filename" -o /home/mkelly/Desktop/DICOM_conversion_test/p04/func/ -z y ~/Desktop/p04_dicoms/00008.RESTING_STATE_FMRI/00008.RESTING_STATE_FMRI/
		#(-f --> filename; -o -->output directory; -z y -->tells it to zip files)

