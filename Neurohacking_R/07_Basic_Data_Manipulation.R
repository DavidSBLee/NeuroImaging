### Masking

library(oro.nifti)

#Set the MRI directory for the nifti data
mridir <- "/home/slee/Desktop"

#Read in the first image
T1 <- readNIfTI(file.path(mridir, "/Output_3D_File.nii.gz"), reorient=FALSE)

#All Field Views of T1 
orthographic(T1)

### Operations (Addtion, Subtraction, Multiplication)

# Mask (Binary 0-1 image)
mask <- readNIfTI(file.path(mridir, '/SUBJ0001_mask.nii.gz'), reorient=FALSE)

# All Field Views of Mask
orthographic(mask)

### Maksing Operation (Multiplying)
# 0's ones we don't want
# 1's ones we want 
masked.T1 <- T1*mask 
# WILL GET AN ERROR if not in the SAME DIMENSIONS: Error in e1@.Data * e2@.Data : non-conformable arrays

# Second MP range (Subtracting)
# Same person, same modality, both MPRAGEs
# Base line & Second Visit

# Load follow-up T1 image
T1.follow <- readNIfTI(file.path(mridir, '/SUBJ0001-020MPRAGE.nii.gz'), reorient=FALSE)

# Subtract baseline T1-w from follow up T1-w scan
subtract.T1 <- T1.follow - T1

# Basic Statistics
min(subtract.T1)
max(subtract.T1)

# Voxel by Voxel oeprations

# Addition
add.T1 <- T1.follow + T1

# Multiplication
multiply.T1 <- T1.follow * T1