import glob
import os
import sys
import subprocess
import codecs

print(sys.argv)
subId = sys.argv[1]
analysis_path = "/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis"
path = "/study4/midusref/midusref_imaging_public"

def open_structural():
	os.system("fslview %s/sub-MRID-%s/anat/sub-MRID-%s_T1w.nii.gz"%(analysis_path, subId, subId))
	os.system("fslview %s/sub-MRID-%s/anat/sub-MRID-%s_T1w_2.nii.gz"%(analysis_path, subId, subId))
	os.system("fslview %s/sub-MRID-%s/anat/sub-MRID-%s_T1w_fslanat.nii.gz"%(analysis_path, subId, subId))
	os.system("fslview %s/sub-MRID-%s/anat/sub-MRID-%s_T1w_2_fslanat.nii.gz"%(analysis_path, subId, subId))

def fslinfo_func(runNum):
	os.system("fslinfo %s/sub-MRID-%s/func/sub-MRID-%s_task-emotion-regulation_run-%s_mod.nii.gz"%(analysis_path, subId, subId, runNum))

def fslinfo_resting():
	os.system("fslinfo %s/sub-MRID-%s/func/sub-MRID-%s_task-rest_bold_mod.nii.gz"%(analysis_path, subId, subId))

def open_functional(runNum):
	os.system("fslview %s/sub-MRID-%s/func/sub-MRID-%s_task-emotion-regulation_run-%s_mod.nii.gz"%(analysis_path, subId, subId, runNum))

def open_resting():
	os.system("fslview %s/sub-MRID-%s/func/sub-MRID-%s_task-rest_bold_mod.nii.gz"%(analysis_path, subId, subId))

def print_html():
	f = codecs.open("%s/sub-MRID-%s/func/QA/motion.html"%(analysis_path, subId))
	g = codecs.open("%s/sub-MRID-%s/func/QA/motion_resting.html"%(analysis_path, subId))
	print (f.read())
	print (g.read())

def open_html():
	os.system("firefox %s/sub-MRID-%s/func/QA/motion_task.html"%(analysis_path, subId))
	os.system("firefox %s/sub-MRID-%s/func/QA/motion_rest.html"%(analysis_path, subId))

def open_csv(runNum):
	os.system("xdg-open %s/sub-MRID-%s/func/sub-MRID-%s_task-emotion-regulation_run-%s_events.tsv"%(path, subId, subId, runNum))

# Structural QA
# Open Structurals
open_structural()

# Functional QA
# fslinfo functionals
fslinfo_func(1)
fslinfo_func(2)
fslinfo_func(3)
fslinfo_resting()

# Open Fucntionals
open_functional(1)
open_functional(2)
open_functional(3)
open_resting()

# Open Motion HTMLs
open_html()

# Open each onset file
open_csv(1)
open_csv(2)
open_csv(3)







