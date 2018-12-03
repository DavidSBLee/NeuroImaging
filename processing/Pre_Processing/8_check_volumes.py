#!/bin/python3
# First Compiled: 8/23/2017
# Last Updated: 10/20/2017
# Updated Content: (10/20/2017) Organization and Output
# Purpose: check volumes for bold, modified bold, and resting.
import glob
import os
import sys
import subprocess

infile = '/study/midus3/processed_data/QA/check_volumes.txt'
f = open(infile, 'w')
sys.stdout = f

def run(command):
    cmd_args_lst = command.split()
    #print("Executing : ", cmd_args_lst)
    ex = subprocess.Popen(cmd_args_lst, stdout=subprocess.PIPE)
    out, err = ex.communicate()
    print("Slices: " + str(out[0:3].decode('utf-8'))) #+ "\n" + "Errors: " + str(err))

path = '/study/midus3/processed_data/MIDUS3_Imaging/'
analysis_path = '/study/midus3/processed_data/MIDUS3_Imaging_Analysis/'
boldfiles = glob.glob('%s/sub-[0-9][0-9][0-9]/func/sub-[0-9][0-9][0-9]_task-EmotionRegulation_run-[0-9][0-9]_bold.nii.gz'%(path))
trimmedBoldFiles = glob.glob('%s/sub-[0-9][0-9][0-9]/func/sub-[0-9][0-9][0-9]_task-EmotionRegulation_run-0[0-9]_bold_mod.nii.gz'%(analysis_path))
restfiles = glob.glob('%s/sub-[0-9][0-9][0-9]/func/sub-[0-9][0-9][0-9]_task-rest_bold.nii.gz'%(path))
trimmedRestFiles = glob.glob('%s/sub-[0-9][0-9][0-9]/func/sub-[0-9][0-9][0-9]_task-rest_bold_mod.nii.gz'%(analysis_path))



print ("--------------------Volumes of Bold Files--------------------")
for file in boldfiles:
	split = file.split('/')
	subNum = split[5]
	runNum = split[7][31:37]
	print (subNum + " " + runNum),
	run("fslnvols %s"%(file))
	print ("")
print ("")


print ("--------------------Volumes of Trimmed Bold Files--------------------")
for trimmed in trimmedBoldFiles:
	subNum = trimmed.split('/')[5]
	runNum = trimmed.split('/')[7][31:37]
	print (subNum + " " + runNum),
	run("fslnvols %s"%(trimmed))
	print ("")
print ("")


print ("--------------------Volumes of Resting State Files--------------------")
for restfile in restfiles:
	subNum = restfile.split('/')[5]
	print (subNum),
	run("fslnvols %s"%(restfile))
	print ("")
print ("")


print ("--------------------Volumes of Trimmed Resting State Files--------------------")
for trimmedRest in trimmedRestFiles:
	subNum = trimmedRest.split('/')[5]
	print (subNum),
	run("fslnvols %s"%(trimmedRest))
	print ("")
print ("")

#os.system("chmod 775 %s"%(infile))

f.close()

