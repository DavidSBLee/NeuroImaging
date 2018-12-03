#!/bin/sh

# Correct for number of tests we do
# Cluster Correction based on amount of smoothing and number of contiguous 
# (sharing border or nearby) significant vertices

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
	echo "----------Cluster Correction----------"
	mri_glmfit-sim \
	--glmdir david/${hemi}.gender_age_pwb_david.glmdir --cache 1.3 pos --cwp  0.05 --2spaces 
done

#specifies the clusterphormic thereshold (significance level for individual vertex) # directional or non-directional # negative log 10 notation (-log(0.05) == 1.3) (1.3 == 0.05 per vertex) (pos neg abs)
#clusterwise thershold (significance thereshold for clusters)
# both left and right hemisphere (omit it if one hemisphere)