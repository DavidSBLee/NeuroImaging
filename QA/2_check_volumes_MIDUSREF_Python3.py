import glob
import os
import sys
import subprocess

f = open('/study4/midusref/midusref_imaging_public/QA/check_volumes1.txt', 'w')
sys.stdout = f

path = '/study4/midusref/midusref_imaging_public/'
analysis_path = '/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis/'
boldfiles = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-emotion-regulation_run-[0-9]_bold.nii.gz'%(path))
#Note that the 'trimmedBoldFiles' & trimmedRestFiles filepaths were incorrect in original script (resulting in 'trimmedBoldFiles' & 'trimmedRestFiles' being empty); specifically the final "MRID" was misspelled MRDI
trimmedBoldFiles = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-emotion-regulation_run-[0-9]_mod.nii.gz'%(analysis_path))
#Also note that the trimmed task files are missing _bold (filepaths in script were changed to reflect that, although it may be best to correct these filenames and change the script to reflect the corrected names)
#trimmedBoldFiles = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-emotion-regulation_run-[0-9]_bold_mod.nii.gz'%(analysis_path))
restfiles = glob.glob('%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-rest_bold.nii.gz'%(path))
trimmedRestFiles = glob.glob("%s/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/sub-MRID-[0-9][0-9][0-9][0-9][0-9]_task-rest_bold_mod.nii.gz"%(analysis_path))
#subNum = boldfiles[70:75]
#runNum = boldfiles[100:105]
"""
for bold in boldfiles:
    subNum = bold[70:75]
    runNum = bold[100:105]


for bold in boldfiles:
    split = bold.split('/')
    subNum = split[4][9:14]
    runNum = split[6][39:44]
"""
def run(command, volumes):
    cmd_args_lst = command.split()
    #print("Executing : ", cmd_args_lst)
    ex = subprocess.Popen(cmd_args_lst, stdout=subprocess.PIPE)
    out, err = ex.communicate()
    decodedOut = int(out[0:3].decode('utf-8'))
    if int(out[0:3].decode('utf-8')) != int(volumes):
        print(subNum + " " + runNum)
        print("Bad:Irregular Number of Volumes")
        print("Volumes: " + str(decodedOut) + "\n")
    elif int(out[0:3].decode('utf-8')) == int(volumes):
        print (subNum + " " + runNum)
        print("Volumes: " + str(decodedOut) + "\n")
"""
    if decodedOut != int(volumes):
        print (subNum + " " + runNum)
        print("Bad:Irregular Number of Volumes")
        print("Volumes: " + str(decodedOut) + "\n") #+ "Errors: " + str(err))
        print("")

    elif decodedOut == int(volumes):
        print (subNum + " " + runNum)
        print("Volumes: " + str(decodedOut) + "\n") #+ "Errors: " + str(err))
"""
countBold = 0
print ("----------Volumes of Bold Files----------")
for file in boldfiles:
    subNum = file[70:75]
    runNum = file[100:105]
    run("fslnvols %s"%(file), 231)
    countBold += 1
    #print (subNum + " " + runNum + "\n"),
print ("How Many Bold Files: " + str(countBold))
print ("How Many Subjects: " + str(countBold/3))
print ("")

countTrimmedBold = 0
print ("----------Volumes of Trimmed Bold Files----------")
for trimmed in trimmedBoldFiles:
    subNum = trimmed[96:101]
    runNum = trimmed[126:131] + "_Trimmed"
    run("fslnvols %s"%(trimmed), 227)
    countTrimmedBold += 1
print ("How Many Trimmed Bold Files: " + str(countTrimmedBold))
print ("How Many Subjects: " + str(countTrimmedBold/3))
print ("")

countRest = 0
print ("----------Volumes of Resting State Files----------")
for restfile in restfiles:
    subNum = restfile.split('-')[2][0:5]
    runNum = "Resting"
    run("fslnvols %s"%(restfile), 240)
    countRest += 1
print ("How Many Resting State Files: " + str(countRest))
print ("How Many Subjects: " + str(countRest))
print ("")

countTrimmedRest = 0
print ("----------Volumes of Trimmed Resting State Files----------")
for trimmedrest in trimmedRestFiles:
    subNum = trimmedrest.split('-')[2][0:5]
    runNum = "Resting_Trimmed"
    run("fslnvols %s"%(trimmedrest), 236)
    countTrimmedRest += 1
print ("How Many Trimmed Resting State Files: " + str(countTrimmedRest))
print ("How Many Subjects: " + str(countTrimmedRest))
print ("")

"""for trimmed in trimmedBoldFiles:
    subNum = trimmed[96:101]
	runNum = trimmed[126:131]
	run("fslnvols %s"%(trimmed), 227)
	countTrimmedBold += 1
"""
f.close()
