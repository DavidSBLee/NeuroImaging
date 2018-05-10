#!/bin/sh

# Smoothe each subject's resampled brain by 10mm FWHM

# Make sure you are in sci6
#ssh freesurfer-sci6.keck.waisman.wisc.edu

# Make sure you are using Freesurfer Version 5.7
#source /study/midusref/public/environments/default

export SUBJECTS_DIR=/study4/midusref/DATA/mri/processed/freesurfer
echo $SUBJECTS_DIR

# Enter subject directory
cd $SUBJECTS_DIR

# Set global varaibles
hemis='lh rh'

# Resample
for hemi in $hemis; do	
	echo "----------Smoothing ${hemi}----------"	
	mri_surf2surf --hemi ${hemi} \
	--s fsaverage_david \
	--sval david/${hemi}.age_pwb_david.fsgd.00.mgh \
	--fwhm 10 \
	--cortex \
	--tval david/${hemi}.age_pwb_david.10B.mgh
done