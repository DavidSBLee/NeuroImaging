#!/bin/sh

# Make sure you are in sci6
#ssh freesurfer-sci6.keck.waisman.wisc.edu

# Make sure you are using Freesurfer Version 5.7
#source /study/midusref/public/environments/default

subj=$1

export SUBJECTS_DIR=/study4/midusref/DATA/mri/processed/freesurfer
echo $SUBJECTS_DIR

cd SUBJECTS_DIR

# Regenerate based on edits to the white matter mask


recon-all -autorecon-pial -autorecon2-wm -autorecon3 -subjid ${subj} -qcache -no-isrunning