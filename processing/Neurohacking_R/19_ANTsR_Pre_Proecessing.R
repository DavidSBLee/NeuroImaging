# Image processing with ANTsR Package
# ANTsR functionalities to work on NIfTI obejcts

# Bias field correction (Using N4 Algorithm)
# Wraps n3BiasFieldCorrection and n4BiasFieldCorrection from ANTsR for bias field correction:
extrantsr::bias_correct 

library(fslr)
library(ANTsR)
library(extrantsr)

# Check for FSL
Sys.getenv("FSLDIR")
options(fsl.path= "/Users/SB/Applications/fsl")
have.fsl()

setwd("/Users/SB/Desktop/Neurohacking_data/BRAINIX/NIfTI")
nim=readNIfTI("T1.nii.gz", reorient = FALSE)


#n3img = bias_correct(nim, corrrection = "N3", retimg=TRUE)
#orthographic(n3img)

# n4 is recommended, improved on speed, convergence properties
# compared to origianl T1 image, you can see where the difference are (T1 - N4 correctd)
n4img = bias_correct(nim, correction = "N4", retimg=TRUE)

orthographic(n4img)

# Registration
tempdir <- "/Users/SB/Desktop/Neurohacking_data/Template"
template <- readNIfTI (file.path(tempdir, "/MNI152_T1_1mm_brain.nii.gz"), reorient = FALSE)

# In ANTsR
registered_n4 = antsRegistration(filename=n4img, template.file= template, remove.warp = TRUE, typeofTransform = "Rigid")

# In extrantsr
registered_n4 = ants_regwrite(filename=n4img, template.file= template, remove.warp = TRUE, typeofTransform = "Rigid")
# read in NIfTI object, do registartion on template, apply that trasformation using rigid transformation, and do intrapolation (local averaging : take all voxel and average them )
# different transfomration "Rigid", "Affine", "SyN"

orthographic(registered_n4)
