#!/usr/bin/env python

# MASTER SCRIPT FOR PROCESSING ALL IMAGING DATA for MIDUS3
# Run it on either condor or local machine
# First Compiled: 6/19/17
# Last Updated: 10/04/17 (David Lee)
# Updated Content: (08/22/17) NIfTI files need suffixes of "01, 02, 03 # NOT "1,2,3" according to BIDS and openfMRI example
# Updated Content: (08/29/17) Added "create_onset" and "separate_onset"
# Updated Content: (09/22/17) Fixed T1w portion as raw-data now has two(2) folders with T1w
# Updated Content: (10/04/17) Attempt to add T1w skull stripping, but was unsuccesful
# Future Updates: Add "0_prep_files.py" and "1_run_bet_anatomical.py"

# Purpose: 1. Convert DICOMs to NIfTIs
#          2. Fix Orientations for fMRI and Resting state
#          3. Create Onset Files of task data
#          4. Separate Onset Files by each run

# Note: There are separate scripts for each steps here:
#       /study3/midus3/processed_data/scripts/03_create_onset.py

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

### 2. Fix Orientations and Delete the old ones ###

"""
subDir = glob.glob("/study/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]")
subPath = set([int(sub[48:51]) for sub in subDir])
print subPath
"""
subPath = glob.glob('/study/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]')
#subPath = glob.glob('%s/sub-[0-9][0-9][0-9]'%(masterPath))

for sub in subPath:
    subNum = sub[48:51]
    if os.path.isdir("%s/func/Orientation_To_Fix/"%(sub)) == True:
        print "----------Fixing functional scan orientations for " + subNum + "----------"
        os.chdir("%s/func/Orientation_To_Fix/"%(sub))
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-01_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-ER_run-01_bold.nii.gz")
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-02_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-ER_run-02_bold.nii.gz")
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-03_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-ER_run-03_bold.nii.gz")
        os.system("fslreorient2std %s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-rest_bold.nii.gz %s/func/sub-"%(sub) + subNum + "_task-rest_bold.nii.gz")
        if os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-ER_run-01_bold.nii.gz") == True: #and os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-ER_run-2_bold.nii.gz") == True and os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-ER_run-3_bold.nii.gz" == True) and os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-rest_bold.nii.gz" == True):
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-01_bold.json", "/%s/func/"%(sub))
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-02_bold.json", "/%s/func/"%(sub))
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-ER_run-03_bold.json", "/%s/func/"%(sub))
            shutil.copy2("/%s/func/Orientation_To_Fix/sub-"%(sub) + subNum + "_task-rest_bold.json", "/%s/func/"%(sub))
            shutil.rmtree("%s/func/Orientation_To_Fix/"%(sub))
            print "----------Removing Orienation_To_Fix Directory for " + subNum + "----------"

#MK-Edits to include dwi/dti. Currently placing files in 'Orientation_Fixed' folder (as with func scans), but may want to just replace old files or place 'fixed' files in same directory w/ new name.

    if os.path.isdir("%s/dwi/Orientation_To_Fix"%(sub)) == True: #and os.path.isfile("%s/dwi/Orientation_Fixed/sub-"%(sub) + subNum + "_dwi.nii.gz") == False:
        print "----------Fixing dwi orienatation for " +  sub + ".----------"
        os.chdir("%s/dwi/Orientation_To_Fix/"%(sub))
        #os.makedirs("Orientation_Fixed")
        os.system("fslreorient2std %s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.nii.gz %s/dwi/sub-"%(sub) + subNum + "_dwi.nii.gz")
        if os.path.isfile("%s/dwi/sub-"%(sub) + subNum + "_dwi.nii.gz") == True:
            shutil.copy2("/%s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.json", "/%s/dwi/"%(sub))
            shutil.rmtree("%s/dwi/Orientation_To_Fix/"%(sub))

### 3. Convert eprime .txt files from MRI Scans to .tsv files (which will be used to create onset files for fmri processing) ###

# Set paths to .txt files and .tsv files
versionNumber = 1
raw_path = '/study3/midus3/raw-data/scan_eprime/data/'
txt_files = glob.glob(r"%s/midus3_order[1-2]_eyetracking_v[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9]*.txt"%(raw_path))

# Check that .tsv files have not already been created. If no .tsv file, script will create .tsv file in 'func' directory (using the .txt file from raw-data). If .tsv file already exists, no action will be taken. As a check for user, script will print names of those subjects for which directories are being created.
for file in txt_files:
    name = file.split('_')[4]
    name = name.split('-')
    name = name[1]
    #version = file[79] # extracts version numbers for each of multiple task data
    tsv_path = "/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/"%(name) # name extracts first ###

    if os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Big/sub-%s_task-ER_events.tsv"%(name)) == True:
        print "----------Onset files (.tsv) for " + name + " exist, so NO E-prime Conversion Needed----------"

    elif os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Big/sub-%s_task-ER_events.tsv"%(name)) == False:
        print "----------Converting----------"
        # Don't do anything when .tsv is already there
        if os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_events.tsv"%(name, name)) == True:
            print ".tsv file(s) already exists for " + name

        # Don't do anything when .tsv with any version number is already there
        elif os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_events_1.tsv"%(name, name)) == True and os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_events_2.tsv"%(name, name)) == True:
            print ".tsv file(s) already exists for " + name

        # Convert when .tsv is not there
        elif os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_events.tsv"%(name, name)) == False:
            if "009" in name: # Currently hardcoded for 009 --> more global approach needed using file counter
                print "----------Creating .tsv file for " + name + "----------"
                os.chdir(tsv_path)
                tsv = "/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Big/sub-%s_task-ER_events_%s.tsv"%(name, versionNumber)
                os.system("eprime2tabfile " + file + " > " + tsv)
                versionNumber += 1
            else:
                print "----------Creating .tsv file for " + name + "----------"
                os.chdir(tsv_path)
                tsv = "/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Big/sub-%s_task-ER_events.tsv"%(name)
                os.system("eprime2tabfile " + file + " > " + tsv)


### 4. Separate Onset files into three separate files ###
masterPath = "/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Big"
tsvPath = glob.glob("%s/*-ER_events.tsv"%(masterPath))
outfile = '/study3/midus3/processed_data/MIDUS3_Imaging/'

for tsv in tsvPath:
    subNum = tsv.split('-')
    subNum = subNum[1]
    subNum = subNum[0:3]

    ### Checking for the third Onset file ###
    # Do Nothing when the third Onset file exists
    if os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_run-03_events.tsv"%(subNum, subNum)) == True:
        print "----------Onsets-by-run for " + subNum + " exist, so NO separation needed----------"

    # Only Convert when the third Onset file does *NOT* exist
    elif os.path.isfile("/study3/midus3/processed_data/MIDUS3_Imaging/sub-%s/func/sub-%s_task-ER_run-03_events.tsv"%(subNum, subNum)) == False:

    ### Creating Onset for block 1 ###

        # Compute various computations and write a .tsv
        with open(tsv, 'rU') as tsvFile, open('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/sub-' + subNum + '_computed-01.tsv', 'wb') as newTsv:

            # Define column header names here
            fields = ('onset_iaps_trimmed',
            'Duration_IAPS',
            'onset_face_trimmed',
            'Duration_Face',
            'Response_Time_Face',
            'Blocks')

            # Create reader and writer variables
            rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
            rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

            #reader.next() # skip header

            # Write column headers manually
            rowWriter.writeheader()

            # Compute the values (onset, duration, response time etc.)
            for rows in rowReader:

                blockNum = rows['Blocks']
                # Cast float to maintain the decimal points
                IAPSOnsetTime = float(rows['IAPSPicture.OnsetTime'])
                IAPSOffsetTime = float(rows['IAPSPicture.OffsetTime'])
                IAPSDuration = float((IAPSOffsetTime - IAPSOnsetTime)/1000)

                faceOnsettime = float(rows['Face.OnsetTime']) #CG
                faceOffsetTime = float(rows['Face.OffsetTime'])
                faceResponsetime = float(rows['Face.RTTime']) #CB
                faceDuration = float((faceOffsetTime - faceOnsettime)/1000)
                responseTime = float((faceResponsetime - faceOnsettime)/1000)

                #Extract only the first block
                if "1" in blockNum:
                    rowWriter.writerow({'onset_iaps_trimmed': ((IAPSOnsetTime-8000)/1000),
                        'Duration_IAPS':IAPSDuration,
                        'onset_face_trimmed': ((faceOnsettime-8000)/1000),
                        'Duration_Face': faceDuration,
                        'Response_Time_Face': responseTime,
                        'Blocks':rows['Blocks']})


        with open(tsv, 'rU') as tsvFile, open('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/' + subNum + '-temporary-01.tsv', 'wb') as newTsv:
            writer = csv.writer(newTsv, delimiter='\t', lineterminator='\n') #lineterminator is paramter in csv.writer. it is default set to '\r\n' causing double spacing
            reader = csv.reader(tsvFile, delimiter='\t')

            for row in reader:
                writer.writerow(row)

        df1 = pd.read_csv('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/sub-' + subNum + '_computed-01.tsv', sep='\t')
        # Use loc and isnull to replace negative responset times to "NaN"
        df1.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "NaN"
        # Remove unnecessary blocks column
        del df1['Blocks']
        df2 = pd.read_csv('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/' + subNum + '-temporary-01.tsv', sep='\t',) # usecols = ['columnname'] could be useful here
        # cut the index
        df3 = df2.ix[:29]
        # Put two csvs together
        df4 = pd.concat([df1, df3], axis=1)
        # Put the combined csvs into pandas data frame
        df4 = pd.DataFrame(df4)
        # Write the datafram into tsv format
        df4.to_csv(outfile + "/sub-" + subNum + "/func/sub-" + subNum + "_task-ER_run-01_events.tsv", sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe

        print "----------Onset file(s) for " + subNum + "-01 created----------"

        ### Creating Onset for block 2 ###

        with open(tsv, 'rU') as tsvFile, open('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/sub-' + subNum + '_computed-02.tsv', 'wb') as newTsv:
            fields = ('onset_iaps_trimmed',
            'Duration_IAPS',
            'onset_face_trimmed',
            'Duration_Face',
            'Response_Time_Face',
            'Blocks')

            rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
            rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

            #reader.next() # skip header

            rowWriter.writeheader() # Write headers manually

            for rows in rowReader:
                blockNum = rows['Blocks']

                IAPSOnsetTime = float(rows['IAPSPicture.OnsetTime'])
                IAPSOffsetTime = float(rows['IAPSPicture.OffsetTime'])
                IAPSDuration = float((IAPSOffsetTime - IAPSOnsetTime)/1000)

                faceOnsettime = float(rows['Face.OnsetTime']) #CG
                faceOffsetTime = float(rows['Face.OffsetTime'])
                faceResponsetime = float(rows['Face.RTTime']) #CB
                faceDuration = float((faceOffsetTime - faceOnsettime)/1000)
                responseTime = float((faceResponsetime - faceOnsettime)/1000)

                if "2" in blockNum:
                    rowWriter.writerow({'onset_iaps_trimmed': ((IAPSOnsetTime-8000)/1000),
                        'Duration_IAPS':IAPSDuration,
                        'onset_face_trimmed': ((faceOnsettime-8000)/1000),
                        'Duration_Face': faceDuration,
                        'Response_Time_Face': responseTime,
                        'Blocks':rows['Blocks']})

        ### Creating Onset for block 3 ###

        with open(tsv, 'rU') as tsvFile, open('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/' + subNum + '-temporary-02.tsv', 'wb') as newTsv:
            writer = csv.writer(newTsv, delimiter='\t', lineterminator='\n') #lineterminator is paramter in csv.writer. it is set to '\r\n' causing double spacing
            reader = csv.reader(tsvFile, delimiter='\t')

            for row in reader:
                writer.writerow(row)

        df1 = pd.read_csv('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/sub-' + subNum + '_computed-02.tsv', sep='\t')

        # Use loc and isnull to replace negative responset times to "NaN"
        df1.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "NaN"
        # Remove unnecessary blocks column
        del df1['Blocks']
        df2 = pd.read_csv('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/' + subNum + '-temporary-02.tsv', sep='\t')
        #df3 = df2.drop(df2.index[[0,1,2,3,4]])
        #df4 = df3.drop(df3[:-3])
        #df2 = df2[df2.Blocks != 1]
        df3 = df2.ix[30:59]
        df3 = df3.reset_index(drop=True)
        #df5 = pd.merge(df1, df3, left_index=True, right_index=True)
        df5 = pd.concat([df1, df3], axis=1)
        # Put into pandas data frame
        df5 = pd.DataFrame(df5)
        # Write the datafram into tsv format
        df5.to_csv(outfile + "/sub-" + subNum + "/func/sub-" +  subNum + "_task-ER_run-02_events.tsv", sep='\t', index=None)

        print "----------Onset file(s) for " + subNum + "-02 created----------"

        with open(tsv, 'rU') as tsvFile, open('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/sub-' + subNum + '_computed-03.tsv', 'wb') as newTsv:
            fields = ('onset_iaps_trimmed',
            'Duration_IAPS',
            'onset_face_trimmed',
            'Duration_Face',
            'Response_Time_Face',
            'Blocks')

            rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
            rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

            #reader.next() # skip header

            rowWriter.writeheader()

            for rows in rowReader:
                blockNum = rows['Blocks']
                IAPSOnsetTime = float(rows['IAPSPicture.OnsetTime'])
                IAPSOffsetTime = float(rows['IAPSPicture.OffsetTime'])
                IAPSDuration = float((IAPSOffsetTime - IAPSOnsetTime)/1000)

                faceOnsettime = float(rows['Face.OnsetTime']) #CG
                faceOffsetTime = float(rows['Face.OffsetTime'])
                faceResponsetime = float(rows['Face.RTTime']) #CB
                faceDuration = float((faceOffsetTime - faceOnsettime)/1000)
                responseTime = float((faceResponsetime - faceOnsettime)/1000)

                if "3" in blockNum:
                    rowWriter.writerow({'onset_iaps_trimmed': ((IAPSOnsetTime-8000)/1000),
                        'Duration_IAPS':IAPSDuration,
                        'onset_face_trimmed': ((faceOnsettime-8000/1000)),
                        'Duration_Face': faceDuration,
                        'Response_Time_Face': responseTime,
                        'Blocks':rows['Blocks']})


        with open(tsv, 'rU') as tsvFile, open('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/' + subNum + '-temporary-03.tsv', 'wb') as newTsv:
            writer = csv.writer(newTsv, delimiter='\t', lineterminator='\n') #lineterminator is paramter in csv.writer. it is default set to '\r\n' causing double spacing
            reader = csv.reader(tsvFile, delimiter='\t')

            for row in reader:
                writer.writerow(row)


        df1 = pd.read_csv('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/sub-' + subNum + '_computed-03.tsv', sep='\t')
        # Use loc and isnull to replace negative responset times to "NaN"
        df1.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "NaN"
        # Remove unnecessary blocks column
        del df1['Blocks']
        df2 = pd.read_csv('/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/' + subNum + '-temporary-03.tsv', sep='\t')
        df3 = df2.ix[60:89]
        df3 = df3.reset_index(drop=True)
        df5 = pd.concat([df1, df3], axis=1)
        # Put into pandas data frame
        df5 = pd.DataFrame(df5)
        # Write the datafram into tsv format
        df5.to_csv(outfile + "/sub-" + subNum + "/func/sub-" + subNum + "_task-ER_run-03_events.tsv", sep='\t', index=None)


        print "----------Onset file(s) for " + subNum + "-03 created----------"

smallPath = glob.glob("/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/*.tsv")
for small in smallPath:
    os.remove(small)
    print "----------Deleting temporary and computed files----------"

### Things to Fix ###
        # 1. CHMOD the whole thing afterwards
        # (Fixed) 2. One problem: the script breaks when there already is "###_unprocessed_dicoms"
        # (Fixed) 3. Delete DICOM folders? b/c they take up space. I can put it in at the end of each loop
        # 4. What's better than if loop? I might use the switch or do-while loop
        # (Fixed) 5. Create task onset files
        # (Fixed) 6. Fix orientations of 5 scans (3 task + 1 resting + dwi scans)

        # Some Extra Codes that might* be useful down the road
        # var.append(scanName)
        # if not os.path.exists(scanName) --> I need this checking method in case it overwrites

        # How to use dcm commands
        #dcm2niix -f "filename" -o /home/mkelly/Desktop/DICOM_conversion_test/p04/func/ -z y ~/Desktop/p04_dicoms/00008.RESTING_STATE_FMRI/00008.RESTING_STATE_FMRI/
        #(-f --> filename; -o -->output directory; -z y -->tells it to zip files)
