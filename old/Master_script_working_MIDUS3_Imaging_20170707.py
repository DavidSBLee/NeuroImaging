#!/bin/python
# MASTER SCRIPT FOR PROCESSING DATA FROM SCAN DAYS.
# First Compiled: 6/19/17
# Authors: David Lee and Michael Kelly
# Purpose: Compile as many pre-processing steps as possible into one script

# dicom_to_nifti
# First Created: 4/11/2017
# Last Updated: 6/19/2017--Updated Loops for fmap. Script had been breaking b/c it was trying to create fmap folder twice. Added loop to check if folder exists already prior to creating it. Also updated code so that 3 functional, 1 resting state, and 1 dwi scans all get put in 'Orientation_To_Fix' folder; from here, we can then fix orientation problems and delete ones that are incorrect (while preserving BIDS Data Structure)--MK
# AUTHOR: D.Lee
# Purpose: When new raw scan data --> convert DICOMs to NIFTIs

import os
import glob
import shutil

# raw DICOMs in an array 
rawDir = glob.glob("/study/midus3/raw-data/[0-9][0-9][0-9]") # or just wildcard it
dicoms = set([int(raw.split('/')[4][0:]) for raw in rawDir]) # extracts INTEGERS w/o "0"
#dicoms.sort()
print dicoms


#dicoms = []
#for raw in rawDir:
	#split = raw.split('/')
	#dicoms.append(int(split[4][0:]))
#dicoms.sort() # or x = sorted(dicoms)
#print dicoms


# NIFTIs
niftiDir = glob.glob("/study/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]")
niftis = set([int(nifti.split('/')[5][4:7]) for nifti in niftiDir]) # in python the set is called hash table
#niftis.sort()
print niftis


#niftis = []
#for nifti in list(niftiDir):
	#splitNifti = nifti.split('/')
	#niftiName = splitNifti[5]
	#subNumNifti = niftiName[4:7]
	#print subNumNifti # this prints p01 etc.
	

# Checking and Processing	

for f in dicoms:
    name = str(f) # string casting
    var = ["0" for _ in range(3-len(name))] + [name] # var = ["0"]*(3-len(name)) (do this b/c just printing f will give me numbers without 0)
    subNum = ''.join(var) # join the numbers without space!
    print "Subject Number: " + subNum # This is for me to check
    
    dicomFolderName = subNum + "_unprocessed_dicoms"
    dicomPath = "/study/midus3/processed_data/dicomdir/"
    dicomSet = glob.glob(dicomPath + dicomFolderName)
    
    if f not in niftis:
        niftiFolderName = "sub-" + subNum
        niftiPath = "/study/midus3/processed_data/MIDUS3_Imaging/"
        
        os.chdir(dicomPath)
        os.makedirs(dicomFolderName) # Create ###_unprocessed_dicoms folders
        os.chdir(dicomFolderName)
        
        direc = glob.glob("/study/midus3/raw-data/" + subNum + "/dicoms/*/*.tgz")
        for d in direc:
            scanName = d.split('/')[6][6:] # Extract scanname
            #dcmConvert = "dcm2niix -f " + niftiFolderName+ "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/anat/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName
            
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
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/anat/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
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
                os.chdir("func")
                os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/func/Orientation_To_Fix/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
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
                os.chdir("func")
                #os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/func/Orientation_To_Fix/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
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
                os.chdir("func")
                #os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/func/Orientation_To_Fix/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
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
                os.chdir("func")
                #os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/func/Orientation_To_Fix/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
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
                os.chdir("dwi")
                os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/dwi/Orientation_To_Fix/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
                print  "----------" + scanName + " Conversion Complete----------"
                
            if "WATER__fmap" in scanName:
                os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
                os.makedirs(scanName)
                os.chdir(scanName)
                os.system("tar -xvzf " + d) # unzip .tgz's
                os.chdir(niftiPath)
                #os.makedirs("sub-" + subNum)
                os.chdir(niftiFolderName)
                if os.path.isdir("%s/%s/fmap/"%(niftiPath, niftiFolderName)) == False:
                    os.makedirs("fmap")
                
                os.system("dcm2niix -f " + niftiFolderName + "_magnitude" + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/fmap/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
                print  "----------" + scanName + " Conversion Complete----------"
                
            if "FieldMap__fmap" in scanName:
                os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
                os.makedirs(scanName)
                os.chdir(scanName)
                os.system("tar -xvzf " + d) # unzip .tgz's
                os.chdir(niftiPath)
                #os.makedirs("sub-" + subNum)
                os.chdir(niftiFolderName)
                if os.path.isdir("%s/%s/fmap/"%(niftiPath, niftiFolderName)) == False:
                    os.makedirs("fmap")
                    
                os.system("dcm2niix -f " + niftiFolderName + "_fieldmap" + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/fmap/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
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
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/asl/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
                print  "----------" + scanName + " Conversion Complete----------"
        print "----------" + subNum + " Coversion Complete----------"
       
for f in dicoms:
    if f in niftis and os.path.isdir("/study3/midus3/processed_data/dicomdir/%s_unprocessed_dicoms"%(subNum)) == True:
        print "Removing unzipped dicoms for" + subNum
        shutil.rmtree("/study3/midus3/processed_data/dicomdir/%s_unprocessed_dicoms/"%(subNum))

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




#orientation_fix
# First Created: 6/14/2017
# Last Updated: 6/19/2017
# Author: D.Lee
# Purpose: For all functional data --> fix the orientations

import glob
import os
import shutil

masterPath = '/study/midus3/processed_data/MIDUS3_Imaging'
subPath = glob.glob('%s/sub-[0-9][0-9][0-9]'%(masterPath))

for sub in subPath:
    subNum = sub[48:51]
    if os.path.isdir("%s/func/Orientation_To_Fix/"%(sub)) == True:
        print "..........Fixing functional scan orientations for " + sub + "..................."
        os.chdir("%s/func/Orientation_To_Fix/"%(sub))
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-1_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-ER_run-1_bold.nii.gz")
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-2_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-ER_run-2_bold.nii.gz")
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-3_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-ER_run-3_bold.nii.gz")
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-rest_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-rest_bold.nii.gz")
        if os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-ER_run-1_bold.nii.gz") == True: #and os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-ER_run-2_bold.nii.gz") == True and os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-ER_run-3_bold.nii.gz" == True) and os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-rest_bold.nii.gz" == True):
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-1_bold.json", "/%s/func/"%(sub))
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-2_bold.json", "/%s/func/"%(sub))
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-3_bold.json", "/%s/func/"%(sub))
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-rest_bold.json", "/%s/func/"%(sub))
            shutil.rmtree("%s/func/Orientation_To_Fix/"%(sub))
        
#MK-Edits to include dwi/dti. Currently placing files in 'Orientation_Fixed' folder (as with func scans), but may want to just replace old files or place 'fixed' files in same directory w/ new name.

    if os.path.isdir("%s/dwi/Orientation_To_Fix"%(sub)) == True: #and os.path.isfile("%s/dwi/Orientation_Fixed/sub-"%(sub) + subNum + "_dwi.nii.gz") == False:
        print "..........Fixing dwi orienatation for " +  sub + "............"
        os.chdir("%s/dwi/Orientation_To_Fix/"%(sub))
        #os.makedirs("Orientation_Fixed")
        os.system("fslreorient2std %s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.nii.gz %s/dwi/sub-"%(sub) + subNum + "_dwi.nii.gz")
        if os.path.isfile("%s/dwi/sub-"%(sub) + subNum + "_dwi.nii.gz") == True:
            shutil.copy2("/%s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.json", "/%s/dwi/"%(sub))
            shutil.rmtree("%s/dwi/Orientation_To_Fix/"%(sub))                

# Maybe I can count the diretoreis?
# And whenever there is one more directory....counter increases....then





#Create .tsv files to be used to make onset files
# First Created: 6/14/2017
# Last Updated: 6/19/2017 (.tsv files are now saved in 'func' directory (not beh) in order to properly follow BIDS data structure)
# AUTHOR: Mike Kelly
# Purpose: Convert eprime .txt files from MRI Scans to .tsv files (which will be used to create onset files for fmri processing)                

#Note: This script works under the assumption that the particpants already have a 'func' directory, as the NIfTI files should have been converted before running this script. If Pp did not have any functional scans, there should be no need to create this .tsv file.

import os
import glob
import os.path



#Set paths to .txt files and .tsv files

raw_path = '/study3/midus3/raw-data/scan_eprime/data/'
txt_files = glob.glob(r"%s/midus3_order[1-2]_eyetracking_v0[0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9].txt"%(raw_path))




#Check that .tsv files have not already been created. If no .tsv file, script will create .tsv file in 'func' directory (using the .txt file from raw-data). If .tsv file already exists, no action will be taken. As a check for user, script will print names of those subjects for which directories are being created.

for file in txt_files:
    name = file.split('_')[4]
    name = name.split('-')
    tsv_path = "/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/"%(name[1])
    if os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_events.tsv"%(name[1], name[1])) == False:
        print "Creating .tsv file for sub-" + name[1]
        os.chdir(tsv_path)
        tsv = "/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_events.tsv"%(name[1], name[1])
        os.system("eprime2tabfile " + file + " > " + tsv)
        

    

