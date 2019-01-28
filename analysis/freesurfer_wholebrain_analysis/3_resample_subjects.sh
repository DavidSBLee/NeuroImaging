#!/bin/sh

# resample each subjects' brain into common space and concatenate to single file (unsmooted output)

# Make sure you are in sci6
#ssh freesurfer-sci6.keck.waisman.wisc.edu

# Make sure you are using Freesurfer Version 5.7
#source /study/midusref/public/environments/default

# Set environment variables
export SUBJECTS_DIR=/study4/midusref/DATA/mri/processed/freesurfer
echo $SUBJECTS_DIR

# Enter subject directory
cd $SUBJECTS_DIR


# Set global varaibles
hemis='lh rh'

# Resample
for hemi in $hemis; do	
	echo "----------Resampling ${hemi}----------"	
	mris_preproc --fsgd david/age_pwb_david.fsgd \
	  --target fsaverage_david \
	  --hemi ${hemi} \
	  --meas thickness \
	  --out david/${hemi}.age_pwb_david.fsgd.00.mgh
done