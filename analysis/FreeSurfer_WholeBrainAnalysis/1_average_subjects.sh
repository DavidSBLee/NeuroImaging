#!/bin/sh

# average subjects' brains and create a customized common space

# Make sure you are in sci6
#ssh freesurfer-sci6.keck.waisman.wisc.edu

# Make sure you are using Freesurfer Version 5.7
#source /study/midusref/public/environments/default

# Set environment variables
export SUBJECTS_DIR=/study4/midusref/DATA/mri/processed/freesurfer
echo $SUBJECTS_DIR

# Create an array of subjects from data structure
subjectlist=`ls /study/midusref/DATA/mri/processed/freesurfer/???/ | awk -F/ {'print $8'} | sort | uniq -u`
ls /study/midusref/DATA/mri/processed/freesurfer/???/ | awk -F/ {'print $8'} | wc 
echo $subjectlist

# Enter subject directory
cd $SUBJECTS_DIR

# Average subjects to create common space
make_average_subject --out fsaverage_david --subjects $subjectlist 