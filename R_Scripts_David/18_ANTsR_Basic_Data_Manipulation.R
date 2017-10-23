# Data Manipulation

library(ANTsR)

setwd("/Users/SB/Desktop/Neurohacking_data/kirby21/visit_1/113")

# Little differnt that readnifti function from oro.nifti package
# Dimensions specified as 3D
aimg = antsImageRead("113-01-MPRAGE.nii.gz", dimension = 3)

# aimg information
class(aimg)

# basic statistics
# Mean of image
mean(aimg)

# Mean over only voxel not equal to 0
mean(aimg[aimg!=0])

# Get image part out of an ANTsR object instead of antsImage
class(as.array(aimg))

# Extransfer function to jump from antsImage to nifti
library(devtools)
devtools::install_github("muschellij2/extrantsr")
libray(extrantsr)
class(nim <- ants2oro(aimg))
