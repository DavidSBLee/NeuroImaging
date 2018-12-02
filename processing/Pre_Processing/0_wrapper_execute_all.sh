#!/usr/bin/env bash

subj=$1

if [[ ! $subj =~ ^-?[0-9]+$ ]]; then
	echo "----------Pass in the Subject-ID as an Argument, TRY AGAIN----------"
else
	echo "----------Begin Processing----------"

	# Permission Masking
	umask 002
	echo "----------Granting Owner and Group RW Permission----------"

	# Pre-Processing
	echo "----------Calling Master Script----------"
	python3 /study/midus3/processed_data/scripts/1_Master_Script_MIDUS3_Python3.py

	# Skull Stripping
	echo "----------Calling Brain Extraction (Bet) Script----------"
	python3 /study/midus3/processed_data/scripts/2_brain_extraction_MIDUS3_Python3.py
	
	# Set environment for Brain Suite
	LD_LIBRARY_PATH=/apps/MCR-R2015b/x86_64_sci7/v90/runtime/glnxa64:/apps/MCR-R2015b/x86_64_sci7/v90/bin/glnxa64:/apps/MCR-R2015b/x86_64_sci7/v90/sys/os/glnxa64
	PATH=/apps/BrainSuite-18a/x86_64_sci7/bin:$PATH

	echo "----------Calling Brain Extraction (BSE) Script----------"
	python3 /study/midus3/processed_data/scripts/2.1_MIDUS3_N4BiasFieldCorrection_5Iter_v2.py

	# Unset Brain Suite Environment (just the matlab, because this particular version collidees with FSL)
	LD_LIBRARY_PATH=

	# Trimming and Motion Assessing
	echo "----------Calling Trim and Motion Assess Script----------"
	python3 /study/midus3/processed_data/scripts/3_trim_and_motion_assess_MIDUS3_Python3_Argument.py $subj

	# Output Volume Check
	echo "----------Calling Volume Check Script----------"
	python3 /study3/midus3/processed_data/scripts/4_check_volumes_MIDUS3_Python3.py

	echo "----------Processing Complete----------"
fi
