#!/usr/bin/env python3

# Author: David SB Lee
# First Compiled: 6/20/17
# Last Updated: 11/13/2017
# Updated Content: (10/14/2017) Created several functions to make the code more readable and efficient
# Updated Content: (10/25/2017) Implemented new dcm command created by Nate Vacks
# Updated Content: (10/27/2017) Function Organization
# Updated Content: (11/13/2017) Python3 Compatiablity
# Purpose: Convert DICOMs to NIfTIs

# Things to change when runing on different data set
# 1. all paths
# 2. all splits
# 3. dicom foldername


import os
import glob
import shutil
#import os.path
import csv
import pandas as pd
import subprocess

### 1. Convert DICOMs to NIFTIs ###

rawData = "/study/midus3/raw-data/[0-9][0-9][0-9]" # path to raw data
processedData= "/study/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]" # path to processed data
#dicomPath = "/study/midus3/processed_data/dicomdir/" # path to unzipped dicoms
niftiPath = "/study/midus3/processed_data/MIDUS3_Imaging/" # path to nifti directories 

# Functions
def structural_conversion(dicoms, niftiPath, suNum, scanName):
    os.system("convert_dcm2niix %s %s/sub-%s/anat/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))

def functional_conversion(dicoms, niftiPath, subNum, versionNum):
    os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-emotion-regulation_run-%s_bold.nii.gz"%(dicoms, niftiPath, subNum, subNum, versionNum))

def resting_conversion(dicoms, niftiPath, subNum, scanName):
    os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))

def dti_conversion(dicoms, niftiPath, subNum, scanName):
    os.system("convert_dcm2niix %s %s/sub-%s/dwi/Orientation_To_Fix/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))

def fieldmap_coversion(dicoms, niftiPath, subNum, fieldMapName):
    os.system("convert_dcm2niix %s %s/sub-%s/fmap/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, fieldMapName))

def asl_converstion(dicoms, niftiPath, subNum, scanName):
     os.system("convert_dcm2niix %s %s/sub-%s/asl/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))

def print_conversion_completion(scanName):
    print  ("----------" + scanName + " Conversion Complete----------")

# raw DICOMs in a set 
rawDir = glob.glob(rawData) # or just wildcard it
dicoms = set([int(raw.split('/')[4][0:]) for raw in rawDir]) # extracts INTEGERS w/o "0"
#dicoms.sort()
print (dicoms)

# NIFTIs
niftiDir = glob.glob(processedData)
niftis = set([int(nifti.split('/')[5][4:7]) for nifti in niftiDir]) # in python the set is called hash table
#niftis.sort()
print (niftis)

# Checking and Processing   

for dicom in dicoms:
    name = str(dicom) # string casting
    number = ["0" for _ in range(3-len(name))] + [name] # var = ["0"]*(3-len(name)) (do this b/c just printing name will give me numbers without 0)
    subNum = ''.join(number) # join the numbers without space!
    #print "Subject Number: " + subNum # This is for me to check

    niftiFolderName = "sub-" + subNum
    niftiSet = niftiPath + niftiFolderName
   
    if dicom in niftis: # if niftis already exists just prints so
        print ("----------NIfTIs for " + subNum + " exist, so NO conversion needed----------")

    elif dicom not in niftis: # but if niftis are not there, start the conversion
        print ("----------Initiating Conversion for " + subNum + "----------")
        
        unzippedDicoms = sorted(glob.glob("/study/midus3/raw-data/" + subNum + "/dicoms/*/*.tgz"))
        for dicoms in unzippedDicoms:
            scanName = dicoms.split('/')[6][6:] # Extract scanname
            
            #if "LOCALIZER" not in scanName: # Skip Localizers
            if "T1w" == scanName: # Had to do this becuase there is additional raw-data folder named T1w since 027
                os.makedirs(niftiSet)
                os.makedirs(niftiSet + "/anat")
                #os.system("convert_dcm2niix %s %s/sub-%s/anat/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))
                structural_conversion(dicoms, niftiPath, subNum, scanName)
                print_conversion_completion(scanName)
            
            if "task-ER_run-1_bold" in scanName:
                #scanName = scanName.replace('1', '01')
                os.makedirs(niftiSet + "/func")
                os.makedirs(niftiSet + "/func/Orientation_To_Fix")
                #os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-emotion-regulation_run-01.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                functional_conversion(dicoms, niftiPath, subNum, "01")
                print_conversion_completion(scanName)

            if "task-ER_run-2_bold" in scanName:
                #scanName = scanName.replace('2', '02')
                #os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-emotion-regulation_run-02.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                functional_conversion(dicoms, niftiPath, subNum, "02")
                print_conversion_completion(scanName)

            if "task-ER_run-3_bold" in scanName:
                #scanName = scanName.replace('3', '03')
                #os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-emotion-regulation_run-03.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                functional_conversion(dicoms, niftiPath, subNum, "03")
                print_conversion_completion(scanName)

            if "task-rest_bold" in scanName:
                #os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))
                resting_conversion(dicoms, niftiPath, subNum, scanName)
                print_conversion_completion(scanName)

            if "dwi" in scanName:
                #os.chdir(niftiSet)
                os.makedirs(niftiSet + "/dwi")
                #os.chdir("dwi")
                os.makedirs(niftiSet + "/dwi/Orientation_To_Fix")
                #os.system("convert_dcm2niix %s %s/sub-%s/dwi/Orientation_To_Fix/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))
                dti_conversion(dicoms, niftiPath, subNum, scanName)
                print_conversion_completion(scanName)

            if "WATER__fmap" in scanName:
                if os.path.isdir("%s/fmap/"%(niftiSet)) == False:
                    os.makedirs("%s/fmap"%(niftiSet))
                #os.system("convert_dcm2niix %s %s/sub-%s/fmap/sub-%s_magnitude.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                fieldmap_coversion(dicoms, niftiPath, subNum, "magnitude")
                print_conversion_completion(scanName)
                                
            if "FieldMap__fmap" in scanName:
                if os.path.isdir("%s/fmap/"%(niftiSet)) == False:
                    os.makedirs("%s/fmap"%(niftiSet))
                #os.system("convert_dcm2niix %s %s/sub-%s/fmap/sub-%s_fieldmap.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                fieldmap_coversion(dicoms, niftiPath, subNum, "fieldmap")
                print_conversion_completion(scanName)
                                
            if "asl" in scanName:
                #os.chdir(niftiSet)
                os.makedirs(niftiSet + "/asl")
                #os.system("convert_dcm2niix %s %s/sub-%s/asl/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))
                asl_converstion(dicoms, niftiPath, subNum, scanName)
                print_conversion_completion(scanName)
            
        print ("----------" + subNum + " Coversion Complete----------")





