import glob
import os
import sys
import subprocess
import codecs

print(sys.argv)
subId = sys.argv[1]
analysis_path = "/study/midus3/processed_data/MIDUS3_Imaging_Analysis"
path = "/study/midus3/processed_data/MIDUS3_Imaging"

def open_structural():
	os.system("fslview_deprecated %s/sub-%s/anat/sub-%s_T1w*"%(analysis_path, subId, subId))
	#os.system("view %s/sub-%s/anat/sub-%s_T1w_anat.nii.gz"%(analysis_path, subId, subId))
	#os.system("view %s/sub-%s/anat/sub-MRID-%s_T1w_2.nii.gz"%(analysis_path, subId, subId))
	#os.system("view %s/sub-%s/anat/sub-MRID-%s_T1w_2_anat.nii.gz"%(analysis_path, subId, subId))

def fslinfo_func(runNum):
	print ("-----------Header Information for {}, run{}-----------".format(subId, runNum))
	os.system("fslinfo %s/sub-%s/func/sub-%s_task-EmotionRegulation_run-%s_bold_mod.nii.gz"%(analysis_path, subId, subId, runNum))

def fslinfo_resting():
	print ("-----------Header Information for {}, resting-----------".format(subId))
	os.system("fslinfo %s/sub-%s/func/sub-%s_task-rest_bold_mod.nii.gz"%(analysis_path, subId, subId))

def open_functional(runNum):
	os.system("fslview_deprecated %s/sub-%s/func/sub-%s_task-EmotionRegulation_run-%s_bold_mod.nii.gz"%(analysis_path, subId, subId, runNum))

def open_resting():
	os.system("fslview_deprecated %s/sub-%s/func/sub-%s_task-rest_bold_mod.nii.gz"%(analysis_path, subId, subId))

#def print_html():
	#f = codecs.open("%s/sub-%s/func/QA/motion.html"%(analysis_path, subId))
	#g = codecs.open("%s/sub-%s/func/QA/motion_resting.html"%(analysis_path, subId))
	#print (g.read())
	#print (f.read())

def open_html():
	#os.system("firefox %s/sub-MRID-%s/func/QA/motion_rest.html"%(analysis_path, subId))
	os.system("open %s/sub-%s/func/QA/motion.html"%(analysis_path, subId))

def open_csv(runNum):
	os.system("open %s/sub-%s/func/sub-%s_task-EmotionRegulation_run-%s_events.tsv"%(path, subId, subId, runNum))

def open_dti():
	os.system("fslview_deprecated %s/sub-%s/dwi/sub-%s_dwi.nii.gz"%(path, subId, subId))

# Structural QA
# Open Structurals
open_structural()

# Functional QA
# fslinfo functionals
fslinfo_func('01')
fslinfo_func('02')
fslinfo_func('03')
fslinfo_resting()

# Open Fucntionals
open_functional('01')
open_functional('02')
open_functional('03')
open_resting()

# Open Motion HTMLs
open_html()
raw_input("----------Press ENTER to Continue----------")

# Open each onset file
open_csv('01')
raw_input("----------Press ENTER to Continue----------")

open_csv('02')
raw_input("----------Press ENTER to Continue----------")

open_csv('03')
raw_input("----------Press ENTER to Continue----------")

# Open DTI scan
open_dti()

print ("----------QA complete for {}----------".format(subId))
