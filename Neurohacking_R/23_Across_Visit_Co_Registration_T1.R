

# Wrapper 
# "preprocess_mri_within" function from Extrantsr package will do:
# 1. Inhomegeneity correction
# 2. Registration of the series of images

library(extrantsr)
library(ANTsR)
library(scales)
library(fslr)
library(oro.nifti)

# Setting Path for FSL
Sys.getenv("FSLDIR")
options(fsl.path= "/Users/SB/Applications/fsl")
have.fsl()

# Master Directory
kirbydir <- "/Users/SB/Desktop/Neurohacking_data/kirby21"

### Registarion of Flair & T2 in T1 Original image
mridir = file.path(kirbydir, "visit_1", "113")

# Pass in a filename vector
files = c("113-01-MPRAGE.nii.gz",
          "113-01-T2w.nii.gz",
          "113-01-FLAIR.nii.gz")

# Making the filenames complete (hardpaths)
files = file.path(mridir, files)

# Create output files
outfiles = c("113-01-MPRAGE_processed.nii.gz",
             "113-01-T2w_processed.nii.gz",
             "113-01-FLAIR_processed.nii.gz")

outfiles = file.path(mridir, outfiles)

### Process MRI within a subject
# Inhomogeniety Correction(N4), Register to first image, apply the mask to the rest of the images
preprocess_mri_within(files=files, retimg = FALSE, outfiles = outfiles, correction = "N4", skull_strip = FALSE)

# Skull-Stripping
# Create NIfTI object "brain"(Mask) ("fslbet_robust" function from ANTsR package)
brain = fslbet_robust(img = outfiles[1], correct = FALSE, verbose = FALSE)
mask = brain > 0

# "fslmask" fucntion list of nifti obejcts contained in "masekd_imgs"
masked_imgs = lapply(outfiles, fslmask, mask = mask, verbose = FALSE)

# Present in orthographic (2nd image(T2w image)has been masked)
# Inhomogeniety corrected, skull stripped image
orthographic(masked_imgs[[2]])




### Registration of Flair & T2 in T1 follow up image
### Process MRI within-visit 
mridir2 = file.path(kirbydir, "visit_2", "113")

files2 = c("113-02-MPRAGE.nii.gz",
           "113-02-T2w.nii.gz",
           "113-02-FLAIR.nii.gz")
files2 = file.path(mridir2, files2)

outfiles2 = c("113-02-MPRAGE_processed.nii.gz",
              "113-02-T2w_processed.nii.gz",
              "113-02-FLAIR_processed.nii.gz")
outfiles2 = file.path(mridir2, outfiles2)

preprocess_mri_within(files=files2, retimg = FALSE, outfiles = outfiles2, correction = "N4", skull_strip = FALSE)

# Take follow-up T1w-image, skull strip it, apply the mask
brain2 = fslbet_robust(img = outfiles2[1], correct = FALSE, verbose = FALSE)

mask2 = brain2 > 0
# Create T1 image from the Follow-up visit
masked_imgs2 = lapply(outfiles2, fslmask, mask = mask2, verbose = FALSE)

#Plot flair image
orthographic(masked_imgs2[[3]])
# Now, All baseline data and follow up data is co-registered to SINGLE space




### Across visit co-registration skull-off images
# Create outfile names for output filenames
oufiles3 = sub('.nii.gz', "_reg.nii.gz", "outfiles2")

# Registartion within a subject
ants_regwrite(filename = masked_imgs2[[1]], 
              retimg = FALSE, outfile = outfiles2[1],
              template.file = masked_imgs[[1]],
              other.files = masked_imgs2[2:3],
              other.outfiles = outfiles2[2:3],
              typeofTransform = "Rigid", verbose = FALSE)

ss_t1 = masked_imgs[[1]]
visit_2_t1 = readNIfTI(outfiles2[1], reorient=FALSE)

# Visually check registration quality
double_ortho(ss_t1, visit_2_t1)
ortho2(ss_t1,visit_2_t1,col.y=alpha(hotmetal(), 0.25))




### Non-Linear Registration
# >12df , registration to a template is necessary 
# Steps

# 1. Move FLAIR into T1w image space (RIGID registration)
# 2. Move ROI into the SAME T1w image space
# 3. Apply Non-Linear transformation to move the T1w into TEMPLATE image

# Why not move FlAIR directly into TEMPLATE?
# B/C template images are created from T1w images, much easier to match T1w to the template as opposed to FLAIR

# AFFINE before non-linear transformation
neurodir <- "/Users/SB/Desktop/Neurohacking_data"

mridir = file.path(neurodir, "BRAINIX", "NIFTI")

t1 = file.path(mridir, "T1.nii.gz")
t1 = readNIfTI(t1, reorient = FALSE)


# read in the FLAIR AND roi NIfTI files
flair = file.path(mridir, "FLAIR.nii.gz")
roi = file.path(mridir, "ROI.nii.gz")


flair_file = readNIfTI(flair, reorient = FALSE)

roi_file = readNIfTI(roi, reorient = FALSE)
is_tumor <- (roi_file > 0)
roi_file[!is_tumor] = NA

orthographic(flair_file, roi_file, xyz=c(200,155,12),
             col.y = alpha("red", 0.2),
             text = "Image overlaid with mask", 
             text.cex = 1.5)

# Non-Linear registration into template
# Goal: have ROI on template space
reg_flair = file.path(mridir, "FLAIR_regToT1.nii.gz")
reg_roi = file.path(mridir, "ROI_regToT1.nii.gz")

reg_flair_img = ants_regwrite(filename = flair,
  template.file = t1,
  outfile = reg_flair,
  typeofTransform = "Rigid",
  other.files = roi,
  other.outfiles = reg_roi,
  verbose = FALSE)

reg_roi_img = readNIfTI(reg_roi, reorient = FALSE)

double_ortho(t1, reg_flair_img)

ortho2(reg_flair_img, reg_roi_img, col.y = alpha("red", 0.2))













