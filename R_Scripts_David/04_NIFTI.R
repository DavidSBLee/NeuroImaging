#install.packages("oro.nifti")
library(oro.nifti)

setwd("/home/slee/Desktop")

# Filename
fname = "Output_3D_File"

# Pass in ojbect for nim
writeNIfTI(nim=nii_T1, filename=fname) #gzipped=FALSE == this argument will not zip it

# Pattern is like wildcard!
list.files(getwd(), pattern= "Output_3D_File")

# Find filenames that has "T" in this particular directory
list.files(getwd(), pattern = 'T')

# Reading a NIfTI file
# Do not reorient due to an error in the function reorient
nii_T1_read = readNIfTI("Output_3D_File", reorient=FALSE)

# Dimensions of the NIfTI file
dim(nii_T1_read)
