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

for hemi in $hemis; do	
	echo "----------GLM Analysis----------"
	mri_glmfit \
	--y david/${hemi}.age_pwb_david.10B.mgh \
	--fsgd david/age_pwb_david.fsgd dods\
	--C david/${hemi}-avg-thickness-age-pwb-cor.mtx \
	--surf fsaverage ${hemi} \
	--cortex \
	--glmdir david/${hemi}.age_pwb_david.glmdir
done