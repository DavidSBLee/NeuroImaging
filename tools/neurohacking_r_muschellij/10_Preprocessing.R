> library(oro.nifti)

# Definitions
# From raw-data to pre-specified analytic format

#1. inhomegeneity correction
	# FSL has its own
	# slowly changing underlying noice from scanner due 
	# to magnetic field used to obtain image is inhomegenous
	# Simple checks: run an aggressive smoother over the image
#2. spatial interpolation
#3. skull stripping
	# crucial when one wants the size of the brain?
	# cruciail when registering to a template..works better
#4. spatial registration

# Pipeline should be scriptable and reproducible

# Basic Pipeline
# DICOM -> NIFTI -> N3 Correction -> Skull-Strip -> Coregistration

# oro.dicom (DICOM to NIFTI)