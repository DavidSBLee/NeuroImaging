#install.packages("oro.dicom")
library(oro.dicom)

# Set working directory for all images
setwd("/home/slee/Desktop/dicomdir/001_unprocessed_dicoms")

# Read all dicoms 
all_slices_T1 = readDICOM("T1w/") # Error when there is .json, make it only get .dcm

# Dimension of first element of images
dim(all_slices_T1$img[[1]])

# Resolution of the images
hdr[hdr$name == "PixelSpacing", "value"]



 