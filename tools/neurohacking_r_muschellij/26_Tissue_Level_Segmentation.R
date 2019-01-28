# Using "fast" function from fslr
# Segment CSF, GM, and WM (divide image into different tissue types, and creating masks accordingly)
# Calculate Volume of CSF, GM, and WM

library(oro.nifti)
library(fslr)

mridir = file.path("/Users/SB/Desktop/Neurohacking_data/kirby21/visit_1/113")
t1_path = file.path(mridir, "113-01-MPRAGE.nii.gz")

### Preprocessing

# Read the T1 image
nim = readNIfTI(t1_path, reorient = FALSE)

# Conduct bias field correction
fast_img = fsl_biascorrect(nim, retimg=TRUE)

# Perform brain extraction
bet = fslbet(infile=fast_img, retimg=TRUE)


### Brain Segmentation

# Perform segmentation
fast = fast(file = bet_fast, outfile = file.path(paste0(mridir,"/113-01-MPRAGE_biascorrected_BET_FAST.nii.gz")))

# Displays CSF segmenation
ortho2(bet, fast==1, col.y = alpha("red", 0.5), text = "SUBJ113_CSF_1")

# Displays GM segmenation
ortho2(bet, fast==2, col.y = alpha("red", 0.5), text= "SUBJ113_GM_1")

# Displays WM segmenation
ortho2(bet, fast==3, col.y = alpha("red", 0.5), text = "SUB113_WM_1")


### Loading in the pve Files to investiage

# Read in the pve file for CSF
pve_CSF = readNIfTI(paste0(mridir, "/113-01-MPRAGE_N4_BET_FAST_pve_0.nii.gz"))

# Read in the pve file for GM
pve_GM = readNIfTI(paste0(mridir, "/113-01-MPRAGE_N4_BET_FAST_pve_1.nii.gz"))

# Read in the pve file for WM
pve_WM = readNIfTI(paste0(mridir, "/113-01-MPRAGE_N4_BET_FAST_pve_2.nii.gz"))

# Read in the pve file for CSF
threshold = 0.33

# Calculate the product of voxel dimensions (Volume)
vdim_CSF=prod(voxdim(pve_CSF))

# Reads in the pve file for WM
nvoxels_CSF=sum(pve_CSF>threshold)

# Calculate the volume of CSF in mL
vol_pveCSF=vdim_CSF*nvoxels_CSF/1000

# CSF volume in mL
vol_pveCSF

# GM volume in mL
vol_pveGM

# WM volume in mL
vol_pveWM
