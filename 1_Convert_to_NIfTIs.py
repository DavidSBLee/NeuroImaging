#!/usr/bin/env python

# First Compiled: 6/20/17
# Last Updated: 10/14/2017
# Updated Content: (10/14/2017) Created several functions to make the code more readable and efficient
# Purpose: Convert DICOMs to NIfTIs

# Things to change when runing on different data set
# 1. all paths
# 2. all splits
# 3. dicom foldername


import os
import glob
import shutil
import os.path
import csv
import pandas as pd

### 1. Convert DICOMs to NIFTIs ###

rawData = "/study/midus3/raw-data/[0-9][0-9][0-9]" # path to raw data
processedData= "/study/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]" # path to processed data
dicomPath = "/study/midus3/processed_data/dicomdir/" # path to unzipped dicoms
niftiPath = "/study/midus3/processed_data/MIDUS3_Imaging/" # path to nifti directories 

# raw DICOMs in an array 
rawDir = glob.glob(rawData) # or just wildcard it
dicoms = set([int(raw.split('/')[4][0:]) for raw in rawDir]) # extracts INTEGERS w/o "0"
#dicoms.sort()
print dicoms

# NIFTIs
niftiDir = glob.glob(processedData)
niftis = set([int(nifti.split('/')[5][4:7]) for nifti in niftiDir]) # in python the set is called hash table
#niftis.sort()
print niftis

def dicom_unzip(dicomSet, scanName, files, niftiPath, niftiFolderName):
    os.chdir(dicomSet)
    os.makedirs(scanName)
    os.chdir(scanName)
    os.system("tar -xvzf " + files) # unzip .tgz's
    os.chdir(niftiPath)
    os.chdir(niftiFolderName)

def func_conversion(dicomSet, scanName, files, niftiPath, niftiFolderName):
    os.chdir(dicomSet)
    os.makedirs(scanName)
    os.chdir(scanName)
    os.system("tar -xvzf " + files) # unzip .tgz's
    os.chdir(niftiPath)
    os.chdir(niftiFolderName)
    os.chdir("func")
    os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o " + niftiSet + "/func/Orientation_To_Fix/" + " -z y " + dicomSet + "/" + scanName)
    print  "----------" + scanName + " Conversion Complete----------"

def print_conversion_completion(scanName):
    print  "----------" + scanName + " Conversion Complete----------"

# Checking and Processing   

for dicom in dicoms:
    name = str(dicom) # string casting
    number = ["0" for _ in range(3-len(name))] + [name] # var = ["0"]*(3-len(name)) (do this b/c just printing name will give me numbers without 0)
    subNum = ''.join(number) # join the numbers without space!
    #print "Subject Number: " + subNum # This is for me to check
    
    dicomFolderName = subNum + "_unprocessed_dicoms"
    dicomSet = dicomPath + dicomFolderName
 
    niftiFolderName = "sub-" + subNum
    niftiSet = niftiPath + niftiFolderName
    # Delete Unzziped Dicoms 
   
    if dicom in niftis: # if niftis already exists just prints so
        print "----------NIfTIs for " + subNum + " exist, so NO conversion needed----------"

    elif dicom not in niftis: # but if niftis are not there, start the conversion
        print "----------Initiating Conversion for " + subNum + "----------"
        os.chdir(dicomPath)
        if os.path.exists(dicomSet): # Prevents script from breaking when there is a dicom folder already
            print "----------Removing unzipped dicoms for " + subNum + "----------"
            shutil.rmtree(dicomSet)

        os.makedirs(dicomSet) # Create ###_unprocessed_dicoms folders
        os.chdir(dicomFolderName)
        
        unzippedDicoms = glob.glob("/study/midus3/raw-data/" + subNum + "/dicoms/*/*.tgz")
        for files in unzippedDicoms:
            scanName = files.split('/')[6][6:] # Extract scanname
            #dcmConvert = "dcm2niix -f " + niftiFolderName+ "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/anat/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName
            
            #if "LOCALIZER" not in scanName: # Skip Localizers
            if "T1w" == scanName: # Had to do this becuase there is additional raw-data folder named T1w since 027
                #os.chdir("/stduy/midus3/processed_data/unprocessed_dicoms/" + dicomFolderName)
                os.makedirs(scanName)
                os.chdir(scanName)
                os.system("tar -xvzf " + files) # unzip .tgz's
                os.chdir(niftiPath)
                os.makedirs(niftiFolderName)
                os.chdir(niftiFolderName)
                os.makedirs("anat")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o " + niftiSet + "/anat/" + " -z y " + dicomSet + "/" + scanName)
                print_conversion_completion(scanName)
                
            if "task-ER_run-1_bold" in scanName:
                scanName = scanName.replace('1', '01')
                dicom_unzip(dicomSet, scanName, files, niftiPath, niftiFolderName)
                os.makedirs("func")
                os.chdir("func")
                os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o " + niftiSet + "/func/Orientation_To_Fix/" + " -z y " + dicomSet + "/" + scanName)
                print_conversion_completion(scanName)
                
            if "task-ER_run-2_bold" in scanName:
                scanName = scanName.replace('2', '02')
                func_conversion(dicomSet, scanName, files, niftiPath, niftiFolderName)
                
            if "task-ER_run-3_bold" in scanName:
                scanName = scanName.replace('3', '03')
                func_conversion(dicomSet, scanName, files, niftiPath, niftiFolderName)
                
            if "task-rest_bold" in scanName:
                func_conversion(dicomSet, scanName, files, niftiPath, niftiFolderName)
                
            if "dwi" in scanName:
                dicom_unzip(dicomSet, scanName, files, niftiPath, niftiFolderName)
                os.makedirs("dwi")
                os.chdir("dwi")
                os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o " + niftiSet + "/dwi/Orientation_To_Fix/" + " -z y " + dicomSet + "/" + scanName)
                print_conversion_completion(scanName)
                                
            if "WATER__fmap" in scanName:
                dicom_unzip(dicomSet, scanName, files, niftiPath, niftiFolderName)
                if os.path.isdir("%s/%s/fmap/"%(niftiPath, niftiFolderName)) == False:
                    os.makedirs("fmap")
                
                os.system("dcm2niix -f " + niftiFolderName + "_magnitude" + " -o " + niftiSet + "/fmap/" + " -z y " + dicomSet + "/" + scanName)
                print_conversion_completion(scanName)
                                
            if "FieldMap__fmap" in scanName:
                dicom_unzip(dicomSet, scanName, files, niftiPath, niftiFolderName)
                if os.path.isdir("%s/%s/fmap/"%(niftiPath, niftiFolderName)) == False:
                    os.makedirs("fmap")
                    
                os.system("dcm2niix -f " + niftiFolderName + "_fieldmap" + " -o " + niftiSet + "/fmap/" + " -z y " + dicomSet + "/" + scanName)
                print_conversion_completion(scanName)
                                
            if "asl" in scanName:
                dicom_unzip(dicomSet, scanName, files, niftiPath, niftiFolderName)
                os.makedirs("asl")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o " + niftiSet + "/asl/" + " -z y " + dicomSet + "/" + scanName)
                print_conversion_completion(scanName)
        print "----------" + subNum + " Coversion Complete----------"
    
    if os.path.exists(dicomSet):
        print "----------Removing unzipped dicoms for " + subNum + "----------"
        shutil.rmtree(dicomSet)
        print "----------DICOM Removal Complete----------"