#install.packages("oro.dicom")
library(oro.dicom)

# Set working directory for all images
setwd("/home/slee/Desktop/dicomdir/001_unprocessed_dicoms")

# Read all dicoms 
all_slices_T1 = readDICOM("T1w/") # Error when there is .json, make it only get .dcm

# Put the list all_slices_T1 into nii_T1 (so nii_T1 is now collection of converted dicoms)
nii_T1 = dicom2nifti(all_slices_T1)

# Dimensions and datatype of nii_T1
d = dim(nii_T1); d; class(nii_T1)

# Plot 11th slice of the array
image(1:d[1], 1:d[2], nii_T1[,,11], col=gray(0:64/64), xlab="")
