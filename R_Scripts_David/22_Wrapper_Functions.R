# Wrapper
# extrantsr function preprocess_mri_within will do:
# Inhomegeneity correction
# Registration of the files to the first filename

library(extrantsr)
library(ANTsR)
library(scales)
library(fslr)

Sys.getenv("FSLDIR")
options(fsl.path= "/Users/SB/Applications/fsl")
have.fsl()

kirbydir <- "/Users/SB/Desktop/Neurohacking_data/kirby21"
mridir = file.path(kirbydir, "visit_1", "113")

files = c("113-01-MPRAGE.nii.gz",
          "113-01-T2w.nii.gz",
          "113-01-FLAIR.nii.gz")
files = file.path(mridir, files)

outfiles = c("113-01-MPRAGE_processed.nii.gz",
             "113-01-T2w_processed.nii.gz",
             "113-01-FLAIR_processed.nii.gz")

outfiles = file.path(mridir, outfiles)

# Inhomogeniety Correction(N4), register and skull strip the first image, apply the mask to the rest of the images
# SO that..I end up with Bias-Field correted Images and only-brain tissue(skull-stripped brain)
preprocess_mri_within(files=files, retimg = FALSE, outfiles = outfiles, correction = "N4", skull_strip = FALSE)

# Apply Brain Mask to all registerd to images
# Create Mask (fslbet_robust function from ANTsR package)
brain = fslbet_robust(img = outfiles[1], correct = FALSE, verbose = FALSE)
mask = brain > 0

# list of nifti obejcts contained in masekd_imgs
masked_imgs = lapply(outfiles, fslmask, mask = mask, verbose = FALSE)

# Present in orthographic (2nd image(T2w image)has been masked)
# Inhomogeniety corrected, skull stripped image
orthographic(masked_imgs[[2]])

### Do the same thing on the follow-up data 
mridir2 = file.path(kirbydir, "visit_2", "113")

files2 = c("113-02-MPRAGE.nii.gz",
          "113-02-T2w.nii.gz",
          "113-02-FLAIR.nii.gz")
files2 = file.path(mridir, files2)
outfiles2 = c("113-02-MPRAGE_processed.nii.gz",
             "113-02-T2w_processed.nii.gz",
             "113-02-FLAIR_processed.nii.gz")

outfiles2 = file.path(mridir2, outfiles2)

preprocess_mri_within(files=files2, retimg = FALSE, outfiles = outfiles2, correction = "N4", skull_strip = FALSE)

brain2 = fslbet_robust(img = outfiles2[1], correct = FALSE, verbose = FALSE)

mask2 = brain2 > 0
# list of nifti contaning mask
masked_imgs2 = lapply(outfiles2, fslmask, mask = mask2, verbose = FALSE)
orthographic(masked_imgs2[[3]])

# Now, All baseline data and follow up data is co-registered to SINGLE space
