#!/usr/bin/env python
# making edits
# MAKING MORE EDITS
import os
import glob
import shutil
import os.path
import csv
import pandas as pd

### 1. Convert DICOMs to NIFTIs ###

# raw DICOMs in an array 
rawDir = glob.glob("/study/midus3/raw-data/[0-9][0-9][0-9]") # or just wildcard it
dicoms = set([int(raw.split('/')[4][0:]) for raw in rawDir]) # extracts INTEGERS w/o "0"
#dicoms.sort()
print dicoms

# NIFTIs
niftiDir = glob.glob("/study/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]")
niftis = set([int(nifti.split('/')[5][4:7]) for nifti in niftiDir]) # in python the set is called hash table
#niftis.sort()
print niftis

# Checking and Processing	

for dicom in dicoms:
    name = str(dicom) # string casting
    number = ["0" for _ in range(3-len(name))] + [name] # var = ["0"]*(3-len(name)) (do this b/c just printing f will give me numbers without 0)
    subNum = ''.join(number) # join the numbers without space!
    #print "Subject Number: " + subNum # This is for me to check
    
    dicomFolderName = subNum + "_unprocessed_dicoms"
    dicomPath = "/study/midus3/processed_data/dicomdir/"
    dicomSet = dicomPath + dicomFolderName
    
    niftiFolderName = "sub-" + subNum
    niftiPath = "/study/midus3/processed_data/MIDUS3_Imaging/"
    
    # Delete Unzziped Dicoms 
   
    if dicom in niftis: # if niftis already exists just prints so
        print "----------Niftis for " + subNum + " exist, so NO conversion needed----------"

    elif dicom not in niftis:
        print "----------Initiating Conversion for " + subNum + "----------"
        
        os.chdir(dicomPath)
        if os.path.exists(dicomFolderName): # Prevents script from breaking when there is a dicom folder already
            print "----------Removing unzipped dicoms for " + subNum + "----------"
            shutil.rmtree(dicomFolderName)

        os.makedirs(dicomFolderName) # Create ###_unprocessed_dicoms folders
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
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/anat/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
                print "----------" + scanName + " Conversion Complete----------"

            if "task-ER_run-1_bold" in scanName:
                scanName = scanName.replace('1', '01')
                os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
                os.makedirs(scanName)
                os.chdir(scanName)
                os.system("tar -xvzf " + files) # unzip .tgz's
                os.chdir(niftiPath)
                #os.makedirs("beh")
                os.chdir(niftiFolderName)
                os.makedirs("func")
                os.chdir("func")
                os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/func/Orientation_To_Fix/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
                print  "----------" + scanName + " Conversion Complete----------"

            if "task-ER_run-2_bold" in scanName:
                scanName = scanName.replace('2', '02')
                os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
                os.makedirs(scanName)
                os.chdir(scanName)
                os.system("tar -xvzf " + files) # unzip .tgz's
                os.chdir(niftiPath)
                #os.makedirs("sub-" + subNum)
                os.chdir(niftiFolderName)
                #os.makedirs("func")
                os.chdir("func")
                #os.makedirs("Orientation_To_Fix")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/func/Orientation_To_Fix/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
                print  "----------" + scanName + " Conversion Complete----------"
                
            if "task-ER_run-3_bold" in scanName:
                scanName = scanName.replace('3', '03')
                os.chdir("/study/midus3/processed_data/dicomdir/" + dicomFolderName)
                os.makedirs(scanName)
                os.chdir(scanName)
                os.system("tar -xvzf " + files) # unzip .tgz's
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
                os.system("tar -xvzf " + files) # unzip .tgz's
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
                os.system("tar -xvzf " + files) # unzip .tgz's
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
                os.system("tar -xvzf " + files) # unzip .tgz's
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
                os.system("tar -xvzf " + files) # unzip .tgz's
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
                os.system("tar -xvzf " + files) # unzip .tgz's
                os.chdir(niftiPath)
                #os.makedirs("sub-" + subNum)
                os.chdir(niftiFolderName)
                os.makedirs("asl")
                os.system("dcm2niix -f " + niftiFolderName + "_" + scanName + " -o /study/midus3/processed_data/MIDUS3_Imaging/" + "sub-" + subNum + "/asl/" + " -z y /study/midus3/processed_data/dicomdir/" + dicomFolderName + "/" + scanName)
                print  "----------" + scanName + " Conversion Complete----------"
        print "----------" + subNum + " Coversion Complete----------"
    
    if os.path.exists(dicomSet):
        print "----------Removing unzipped dicoms for " + subNum + "----------"
        shutil.rmtree(dicomSet)
        print "----------DICOM Removal Complete----------"