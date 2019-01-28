> library(oro.nifti)

#Fluid-attenuated inversion recovery (FLAIR)
# It's clear that brain cancer area is obvious to visual inspection
# Set working directory
mridir <- "~/Neurohacking_data/BRAINIX/NIfTI"
sequence <- "FLAIR"
# Imaging single slice 12 on z scale (axial)
volume.f <- readNIfTI(file.path(mridir, paste0(sequence,'.nii.gz')),reorient=FALSE)
volume.f <- cal_img(volume.f)
image(volume.f, z = 12, plot.type = "single")

# T1 Weighted Image (hypointensive = darker)
sequence <- 'T1'
volume.t1 <- readNIfTI(file.path(mridir,sequence),reorient=FALSE)
volume.t1 <- cal_img(volume.t1)
image(volume.t1, z =12, plot.type = 'single')

# T2 Weighted Image (hyperintensive = lighter)
sequence <- 'T2'
volume.t2 <- readNIfTI(file.path(mridir,sequence),reorient=FALSE)
volume.t2 <- cal_img(volume.t2)
image(volume.t2, z =12, plot.type = 'single')
