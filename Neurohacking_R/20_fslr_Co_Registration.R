# Within Subject Registration

# ROI localization

# Segmentation

# Linear Registration: Rigid
# 6 df, 3df in rotation(R)(3 angles) and 3df in translation(t)
# Rotations: Pitch , Roll, and Yaw ==Yes, No, and I don't know

library(oro.nifti)
library(extrantsr)
library(fslr)

kirbydir <- "/Users/SB/Desktop/Neurohacking_data/kirby21"
mridir = file.path(kirbydir, "visit_1", "113")
T1_file = file.path(mridir, "113-01-MPRAGE.nii.gz")
# T1 image at baseline
T1 = readNIfTI(T1_file, reorient=FALSE)

# Registration of T2w to T1 with SKULL ON
# FLIRT from FSL is an automatd and robust tool for linear(affine) registration
# fslrl function flirt (calling FSL function flirt)

T2_file = file.path(mridir, "113-01-T2w.nii.gz")
T2w = readNIfTI(T2_file)
# Calls FSL, does Rigid Transformation, 
flirt_reg_t2_img = flirt(infile = T2_file, reffile = T1, dof = 6, verbose = FALSE)

# Pulls images side by side
double_ortho(T1, flirt_reg_t2_img)

