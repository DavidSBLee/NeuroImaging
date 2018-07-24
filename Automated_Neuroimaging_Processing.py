#!/bin/python3

# Autor: D.Lee
# First Compiled: 10/15/2017
# Last Updated: 12/08/2017
# Updated Content: (10/15/2017) Organization
# Updated Content: (10/30/2017) Compilation of individual scripts
# Updated Conetnt: (11/02/2017) Added "groups" column tu pull Parametric modulation as "1"
# Updated Conetnt: (11/13/2017) Python 3 Compatibility Partial Update
# Updated Conetnt: (11/20/2017) Onset_Separation TTL adjustment
# Updated Conetnt: (12/08/2017) Python 3 Compatibility Final Update
# Updated Conetnt: (01/10/2018) Bug Fix in onset creation (lines 200, 201, 217, 218)
# Updated Content: (01/30/2018) Updated loop for subject 035: two e-prime files
# Updated Content: (04/25/2018) Updated dicom conversion loop for subject 050: different raw-scan name
# Updated Content: (05/10/2018) Updated fMRI file structure to fit BIDS specification
# Updated Content: (06/08/2018) Added "umask 002" to grant output file permissions
# Updated Content: (06/20/2018) Deleted "umask 002" becasue this does not work on condor environment

# Purpose: 1. Convert DICOMs to NIfTIs
#          2. Fix Orientations for fMRI and Resting state
#          3. Create Onset Files of task data
#          4. Separate Onset Files by each run

# Things to change when runing on different data set
#   1. Global Variables
#   2. Splits
#   3. Arguments passed into functions

# Import necessary Modules
import os
import glob
import shutil
import os.path
import csv
import pandas as pd


# Set Global Variables (All are paths...)
rawData = "/study/midus3/raw-data/[0-9][0-9][0-9]" # path to raw data
processedData= "/study/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]" # path to processed data
niftiPath = "/study/midus3/processed_data/MIDUS3_Imaging/" # path to nifti directories

onsetPath = "/study/midus3/raw-data/scan_eprime/data/" # path to onset .txt files
temporaryBigPath = "/study/midus3/processed_data/Temporary/Big/"
temporarySmallPath = "/study/midus3/processed_data/Temporary/Small/"

# Set Functions in order of Usage
def structural_conversion(dicoms, niftiPath, suNum, scanName):
    os.system("convert_dcm2niix %s %s/sub-%s/anat/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))

def functional_conversion(dicoms, niftiPath, subNum, versionNum):
    os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-EmotionRegulation_run-%s_bold.nii.gz"%(dicoms, niftiPath, subNum, subNum, versionNum))

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

def fix_orientation(sub, subNumFull, versionNum):
    os.system("fslreorient2std %s/func/Orientation_To_Fix/%s_task-EmotionRegulation_run-%s_bold.nii.gz"%(sub, subNumFull, versionNum) + " %s/func/%s_task-EmotionRegulation_run-%s_bold.nii.gz"%(sub, subNumFull, versionNum))

def copy_bold_files(sub, subNum, versionNum):
    shutil.copy2("/%s/func/Orientation_To_Fix/%s_task-EmotionRegulation_run-%s_bold.json"%(sub, subNumFull, versionNum), "/%s/func/"%(sub))

def fix_resting_orientation(sub, subNum):
    os.system("fslreorient2std %s/func/Orientation_To_Fix/%s_task-rest_bold.nii.gz"%(sub, subNumFull) + " %s/func/%s_task-rest_bold.nii.gz"%(sub, subNumFull))

def copy_resting_files(sub, subNum):
    shutil.copy2("/%s/func/Orientation_To_Fix/%s_task-rest_bold.json"%(sub, subNumFull), "/%s/func/"%(sub))

def fix_dti_orientation(sub, subNum):
    os.system("fslreorient2std %s/dwi/Orientation_To_Fix/%s_dwi.nii.gz"%(sub, subNumFull) + " %s/dwi/%s_dwi.nii.gz"%(sub, subNumFull))

def copy_dti_files(sub, subNum):
    shutil.copy2("/%s/dwi/Orientation_To_Fix/%s_dwi.json"%(sub, subNumFull), "/%s/dwi/"%(sub))

#Define column header names
def calc_write_values_IAPS(newTsv,tsvFile, taskNum):
    rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
    rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

    # Write column headers manually
    rowWriter.writeheader()

    # Compute the values (onset, duration, response time etc.)
    for rows in rowReader:
        blockNum = rows['Blocks']
        # Cast float to maintain the decimal points
        IAPSOnsetTime = float(rows['IAPSPicture.OnsetTime'])/float(1000)
        IAPSOffsetTime = float(rows['IAPSPicture.OffsetTime'])/float(1000)
        IAPSTTL = float(rows['WaitForTTL.RTTime'])/float(1000)
        IAPSOnsetTTLAdjusted = IAPSOnsetTime - IAPSTTL
        IAPSDuration = float(IAPSOffsetTime - IAPSOnsetTime)
        IAPSOnsetTimeTrimmed = IAPSOnsetTTLAdjusted - 8#(float(rows['IAPSPicture.OnsetTime'])-8000)/float(1000)
        IAPSNumber = rows['PictureFile'][:4]
        IAPSValence = rows['valencecategory']
        IAPSSocilaity = rows['Sociality']
        ones = rows['Group']

        taskNum = str(taskNum)
        if taskNum in blockNum:

            rowWriter.writerow({'onset': IAPSOnsetTTLAdjusted,
            'duration':IAPSDuration,
            'Response_Time_Face': "n/a",
            'database': "IAPS",
            'stimulus': IAPSNumber,
            'correct': "n/a",
            'valence': IAPSValence,
            'valenceFollowing': "n/a",
            'gender': "n/a",
            'response': "n/a",
            'face_correct_response': "n/a",
            'sociality': IAPSSocilaity,
            'groups': ones,
            'onset_trimmed': IAPSOnsetTimeTrimmed,
            'Blocks':rows['Blocks']})

def calc_write_values_faces(newTsv,tsvFile, taskNum):
    rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
    rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

    # Write column headers manually
    rowWriter.writeheader()

    # Compute the values (onset, duration, response time etc.)
    for rows in rowReader:
        blockNum = rows['Blocks']
        # Cast float to maintain the decimal points
        faceOnsetTime = float(rows['Face.OnsetTime'])/float(1000) #CG
        faceOffsetTime = float(rows['Face.OffsetTime'])/float(1000)
        faceTTL = float(rows['WaitForTTL.RTTime'])/float(1000)
        faceOnsetTTLAdjusted = faceOnsetTime - faceTTL
        faceOnsetTimeTrimmed = faceOnsetTTLAdjusted - 8 #(float(rows['Face.OnsetTime'])-8000)/float(1000)
        faceResponseTime = float(rows['Face.RT'])/float(1000) #CB
        faceDuration = float(faceOffsetTime - faceOnsetTime)
        faceNumber = rows['FaceFile'][:2]
        faceGender = rows['Gender']
        faceResponse = rows['Face.RESP']
        faceCorrectResponse = rows['Face.CRESP']
        faceCorrect = rows['Face.ACC']
        ones = rows['Group']
        IAPSValence = rows['valencecategory']

        taskNum = str(taskNum)
        if taskNum in blockNum:
            if faceCorrect == '1':
                variable = 'Y'
            elif faceCorrect == '0':
                variable = 'N'
            rowWriter.writerow({'onset': faceOnsetTTLAdjusted,
            'duration': faceDuration,
            'Response_Time_Face': faceResponseTime,
            'database': "faces",
            'stimulus': faceNumber,
            'correct': variable,
            'valence': "n/a",
            'valenceFollowing': IAPSValence,
            'gender': faceGender,
            'response': faceResponse,
            'face_correct_response': faceCorrectResponse,
            'sociality': "n/a",
            'groups': ones,
            'onset_trimmed': faceOnsetTimeTrimmed,
            'Blocks':rows['Blocks']})

#lineterminator is paramter in csv.writer. it is default set to '\r\n' causing double spacing
def reader_and_writer(newTsv, tsvFile):
    writer = csv.writer(newTsv, delimiter='\t', lineterminator='\n')
    reader = csv.reader(tsvFile, delimiter='\t')

    for row in reader:
        writer.writerow(row)

def block_one_data_manipulation(temporarySmallPath, subNum, niftiPath):
    # Read in csv
    df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_IAPS-01.tsv', sep='\t')
    df2 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_faces-01.tsv', sep='\t')
    # join the two data frames along rows
    df3 = pd.concat([df1, df2])
    # Sort everything by onset column
    df3 = df3.sort_values('onset')
    # Remove unnecessary blocks column
    del df3['Blocks']
    # Use loc and isnull to replace no responses to "n/a"
    df3.loc[(df3['Response_Time_Face'] == 0), 'Response_Time_Face'] = "n/a"
    df3.loc[(df3['response'].isnull()), 'response'] = "n/a"
    # Write the datafram into tsv format
    df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-EmotionRegulation_run-01_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
    print ('----------Onset file(s) for ' + subNum + '-01 created----------')

def block_two_data_manipulation(temporarySmallPath, subNum, niftiPath):
    # Read in csv to Pandas
    df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_IAPS-02.tsv', sep='\t')
    df2 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_faces-02.tsv', sep='\t')
    # join the two data frames along rows
    df3 = pd.concat([df1, df2])
    # Sort everything by onset column
    df3 = df3.sort_values('onset')
    # Remove unnecessary blocks column
    del df3['Blocks']
    # Use loc and isnull to replace no responses to "n/a"
    df3.loc[(df3['Response_Time_Face'] == 0), 'Response_Time_Face'] = "n/a"
    df3.loc[(df3['response'].isnull()), 'response'] = "n/a"
    # Write the datafram into tsv format
    df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-EmotionRegulation_run-02_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
    print ('----------Onset file(s) for ' + subNum + '-02 created----------')

def block_three_data_manipulation(temporarySmallPath, subNum, niftiPath):
    # Read in csv to Pandas
    df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_IAPS-03.tsv', sep='\t')
    df2 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_faces-03.tsv', sep='\t')
    # join the two data frames along rows
    df3 = pd.concat([df1, df2])
    # Sort everything by onset column
    df3 = df3.sort_values('onset')
    # Remove unnecessary blocks column
    del df3['Blocks']
    # Use loc and isnull to replace no responses to "n/a"
    df3.loc[(df3['Response_Time_Face'] == 0), 'Response_Time_Face'] = "n/a"
    df3.loc[(df3['response'].isnull()), 'response'] = "n/a"
    # Write the datafram into tsv format
    df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-EmotionRegulation_run-03_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
    print ('----------Onset file(s) for ' + subNum + '-03 created----------')

if __name__ == "__main__":
    ### 1. Convert DICOMs to NIFTIs ###

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

        niftiFolderName = "sub-" + subNum
        niftiSet = niftiPath + niftiFolderName

        if dicom in niftis: # if niftis already exists just prints so
            #print ("----------NIfTIs for " + subNum + " exist, so NO conversion needed----------")
            pass

        elif dicom not in niftis: # but if niftis are not there, start the conversion
            print ("----------Initiating Conversion for " + subNum + "----------")

            unzippedDicoms = sorted(glob.glob("/study/midus3/raw-data/" + subNum + "/dicoms/*/*.tgz"))
            for dicoms in unzippedDicoms:
                fullScanName = dicoms.split('/')[6]
                scanName = fullScanName[6:] # Extract scanname
                #print (scanName)
                #if "LOCALIZER" not in scanName: # Skip Localizers
                if "T1w" == scanName: # Had to do this becuase there is additional raw-data folder named T1w since 027
                    os.makedirs(niftiSet)
                    os.makedirs(niftiSet + "/anat")
                    #os.system("convert_dcm2niix %s %s/sub-%s/anat/sub-%s_%s.nii.gz"%(dicoms, niftiPath, subNum, subNum, scanName))
                    structural_conversion(dicoms, niftiPath, subNum, scanName)
                    print_conversion_completion(scanName)

                if "00005.task-ER_run-1_bold" in fullScanName:
                    #scanName = scanName.replace('1', '01')
                    os.makedirs(niftiSet + "/func")
                    os.makedirs(niftiSet + "/func/Orientation_To_Fix")
                    #os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-emotionRegulation_run-01.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                    functional_conversion(dicoms, niftiPath, subNum, "01")
                    print_conversion_completion(scanName)

                if "00006.task-ER_run-2_bold" in fullScanName:
                    #if "task-ER_run-2_bold" in fullScanName:
                        #scanName = scanName.replace('2', '02')
                        #os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-emotionRegulation_run-02.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                    functional_conversion(dicoms, niftiPath, subNum, "02")
                    print_conversion_completion(scanName)

                    #elif "task-ER_run-1_bold" in fullScanName:
                        #functional_conversion(dicoms, niftiPath, subNum, "02")
                        #print_conversion_completion("task-ER_run-2_bold")

                if "00007." in fullScanName:
                    #if "task-ER_run-3_bold" in fullScanName:
                    functional_conversion(dicoms, niftiPath, subNum, "03")
                    print_conversion_completion(scanName)
                """
                if "00007." in fullScanName:
                    if "task-ER_run-3_bold" in fullScanName:
                        #scanName = scanName.replace('3', '03')
                        #os.system("convert_dcm2niix %s %s/sub-%s/func/Orientation_To_Fix/sub-%s_task-emotionRegulation_run-03.nii.gz"%(dicoms, niftiPath, subNum, subNum))
                        functional_conversion(dicoms, niftiPath, subNum, "03")
                        print_conversion_completion(scanName)

                    elif "task-ER_run-2_bold" in scanName:
                        functional_conversion(dicoms, niftiPath, subNum, "03")
                        print_conversion_completion("task-ER-run-3_bold")
				"""
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

    ### 2. Fix Orientations and Delete the old ones ###

    subPath = glob.glob(processedData)

    for sub in subPath:
        subNumFull = sub.split('/')[5]
        subNum = subNumFull[4:7]

        if os.path.isdir("%s/func/Orientation_To_Fix/"%(sub)) == True:
            print ("----------Fixing functional scan orientations for " + subNum + "----------")
            fix_orientation(sub, subNumFull, "01")
            fix_orientation(sub, subNumFull, "02")
            fix_orientation(sub, subNumFull, "03")
            fix_resting_orientation(sub, subNum)

            if os.path.isfile("%s/func/sub-"%(sub) + subNum + "_task-EmotionRegulation_run-01_bold.nii.gz") == True:
                copy_bold_files(sub, subNum, "01")
                copy_bold_files(sub, subNum, "02")
                copy_bold_files(sub, subNum, "03")
                copy_resting_files(sub, subNum)
                shutil.rmtree("%s/func/Orientation_To_Fix/"%(sub))


        if os.path.isdir("%s/dwi/Orientation_To_Fix"%(sub)) == True:
            print ("----------Fixing dwi orienatation for " +  subNum + ".----------")
            fix_dti_orientation(sub, subNum)

            if os.path.isfile("%s/dwi/sub-"%(sub) + subNum + "_dwi.nii.gz") == True:
                copy_dti_files(sub, subNum)
                # BVECs and BVALSs created here are not usable
                #shutil.copy2("/%s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.bval", "/%s/dwi/"%(sub))
                #shutil.copy2("/%s/dwi/Orientation_To_Fix/sub-"%(sub) + subNum + "_dwi.bvec", "/%s/dwi/"%(sub))
                shutil.rmtree("%s/dwi/Orientation_To_Fix/"%(sub))


    ### 3. Convert eprime .txt files from to .tsv files ###
    versionNumber = 1

    txt_files = sorted(glob.glob("%s/midus3_order[0-9]_eyetracking_v[0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9]*.txt"%(onsetPath)))

    # Check that .tsv files have not already been created. If no .tsv file, script will create .tsv file in 'func' directory (using the .txt file from raw-data). If .tsv file already exists, no action will be taken. As a check for user, script will print names of those subjects for which directories are being created.
    for file in txt_files:
        name = file.split('_')[4]
        name = name.split('-')
        name = name[1]
        #version = file[79] # extracts version numbers for each of multiple task data
        tsv_path = niftiPath + "/sub-%s/func/"%(name) # name extracts first ###

        if os.path.isfile(temporaryBigPath + "/sub-%s_task-ER_events.tsv"%(name)) == True:
            #print ("----------No E-prime Conversion for", name, "Needed----------")
            pass

        elif os.path.isfile(temporaryBigPath + "/sub-%s_task-ER_events.tsv"%(name)) == False:
            print ("----------Converting----------")
            # Don't do anything when .tsv is already there
            if os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events.tsv"%(name, name)) == True:
                print (".tsv file(s) already exists for " + name)

            # Don't do anything when .tsv with any version number is already there
            elif os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events_1.tsv"%(name, name)) == True and os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events_2.tsv"%(name, name)) == True:
                print (".tsv file(s) already exists for " + name)

            # Convert when .tsv is not there
            elif os.path.isfile(niftiPath + "/sub-%s/func/sub-%s_task-ER_events.tsv"%(name, name)) == False:
                if "009" in name: # Currently hardcoded for 009 --> more global approach needed using file counter
                    print ("----------Creating .tsv file for " + name + "----------")
                    os.chdir(tsv_path)
                    tsv = temporaryBigPath + "/sub-%s_task-ER_events_%s.tsv"%(name, versionNumber)
                    os.system("eprime2tabfile " + file + " > " + tsv)
                    versionNumber += 1

                elif "038" in name:
                    print ("----------Creating .tsv file for " + name + "----------")
                    os.chdir(tsv_path)
                    tsv = temporaryBigPath + "/sub-%s_task-ER_events_%s.tsv"%(name, versionNumber)
                    os.system("eprime2tabfile " + file + " > " + tsv)
                    versionNumber += 1

                else:
                    print ("----------Creating .tsv file for " + name + "----------")
                    os.chdir(tsv_path)
                    tsv = temporaryBigPath + "/sub-%s_task-ER_events.tsv"%(name)
                    os.system("eprime2tabfile " + file + " > " + tsv)

    ### 4. Separate Onset files into three separate files ###

    tsvPath = sorted(glob.glob('%s/*-ER_events.tsv'%(temporaryBigPath)))

    # Define column header names & # Create reader and writer variables
    # reader.next() # skip header
    fields = ['onset',
        'duration',
        'database',
        'Response_Time_Face',
        'stimulus',
        'correct',
        'valence',
        'valenceFollowing',
        'gender',
        'response',
        'face_correct_response',
        'sociality',
        'groups',
        'onset_trimmed',
        'Blocks']

    for tsv in tsvPath:
        subNum = tsv.split('-')
        subNum = subNum[1]
        subNum = subNum[0:3]

        ### Checking for the third Onset file ###
        # Do Nothing when the third Onset file exists
        if os.path.isfile(niftiPath + '/sub-%s/func/sub-%s_task-EmotionRegulation_run-03_events.tsv'%(subNum, subNum)) == True:
            #print ('----------Onsets by run for ' + subNum + ' exist already---------')
            pass

        # Only Convert when the third Onset file does *NOT* exist
        elif os.path.isfile(niftiPath + '/sub-%s/func/sub-%s_task-EmotionRegulation_run-03_events.tsv'%(subNum, subNum)) == False:

            ### Creating Onset for block 1 ###

            # Compute various computations and write a .tsv
            with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_IAPS-01.tsv', 'w', newline="") as newTsv:
                calc_write_values_IAPS(newTsv, tsvFile, 1)

            with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_faces-01.tsv', 'w', newline="") as newTsv:
                calc_write_values_faces(newTsv, tsvFile, 1)

            block_one_data_manipulation(temporarySmallPath, subNum, niftiPath)

            ### Creating Onset for block 2 ###

            with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_IAPS-02.tsv', 'w', newline="") as newTsv:
                calc_write_values_IAPS(newTsv, tsvFile, 2)

            with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_faces-02.tsv', 'w', newline="") as newTsv:
                calc_write_values_faces(newTsv, tsvFile, 2)

            block_two_data_manipulation(temporarySmallPath, subNum, niftiPath)

            ### Creating Onset for block 3 ###

            with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_IAPS-03.tsv', 'w', newline="") as newTsv:
                calc_write_values_IAPS(newTsv, tsvFile, 3)

            with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_faces-03.tsv', 'w', newline="") as newTsv:
                calc_write_values_faces(newTsv, tsvFile, 3)

            block_three_data_manipulation(temporarySmallPath, subNum, niftiPath)

            print ('----------Onset Data Manipulation for', subNum, 'Complete----------')
