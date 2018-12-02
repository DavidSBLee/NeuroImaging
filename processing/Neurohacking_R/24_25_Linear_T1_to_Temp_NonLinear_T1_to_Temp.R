# Linear Registartion of T1 to the template
# Affine before Non-Linear

library(extrantsr)
library(ANTsR)
library(scales)
library(fslr)
library(oro.nifti)
library(plyr)

# Setting Path for FSL
Sys.getenv("FSLDIR")
options(fsl.path= "/Users/SB/Applications/fsl")
have.fsl()

# Pre-processing steps on T1 image
neurodir <- "/Users/SB/Desktop/Neurohacking_data"
mridir = file.path(neurodir, "BRAINIX", "NIFTI")
t1 = file.path(mridir, "T1.nii.gz")
t1 = readNIfTI(t1, reorient = FALSE)

# Bias Correction 
n4_t1 = bias_correct(t1, correction = "N4")

# Skull strip
brain = fslbet_robust(img = n4_t1, correct = FALSE, verbose = FALSE)

# Affine registation on EVE template (no skull template)
template.file = file.path(neurodir, "Template", "JHU_MNI_SS_T1_brain.nii.gz")

# Affinely registered T1
aff_t1_outfile = file.path(mridir, "T1_AffinetoEVE.nii.gz")

# Affinely registerd ROI
aff_roi_outfile = file.path(mridir, "ROI_regToT1_AffinetoEVE.nii.gz")
reg_roi = file.path(mridir, "ROI_regToT1.nii.gz")

# Do affine registration with "ants_regwrite" function from Extrantsr package
aff_brain = ants_regwrite(filename = brain,
                          outfile = aff_t1_outfile,
                          other.files = reg_roi, # Already in the T1 space
                          other.outfiles = aff_roi_outfile,
                          template.file = template.file,
                          typeofTransform = "Affine",
                          verbose = FALSE)

aff_roi = readNIfTI(aff_roi_outfile, reorient = FALSE)

template = readNIfTI(template.file, reorient = FALSE)
# T1 imaged registered + EVE template
double_ortho(aff_brain, template)

# Continue Assessing (plotting registred_T1 overlayed by template)
ortho2(aff_brain, template, col.y = alpha(hotmetal(),0.35))

# Affine brain on the bottom, overlayed the template over
ortho2(aff_brain, template, z=ceiling(dim(template)[3]/2), plot.type="single",col.y=alpha(hotmetal(),0.35))

# Make sure ROI is sitting in the T1W image, plot affinely registred T1 image on top of aff_roi
ortho2(aff_brain, aff_roi, col.y = alpha(hotmetal(),0.35), xyz=xyz(aff_roi))


### Non-Linear Registration of T1 to Template 
# Flair to T1 (Rigid)
# SyN (Diffeomorphic Symmetric Normalization):
# Flexible and local matching of tissues to the template
# EVE template (skull-stripped) so we have to skull strip our images to match

syn_t1_outfile = file.path(mridir, "T1_SyntoEve.nii.gz")
syn_roi_outfile = file.path(mridir, "ROI_regToT1_SyntoEve.nii.gz")

syn_brain = ants_regwrite(filename = brain,
                          outfile = syn_t1_outfile,
                          other.files = reg_roi,
                          other.outfiles = syn_roi_outfile,
                          template.file = template.file,
                          typeofTransform = "SyN",
                          verbose = FALSE)

syn_roi = readNIfTI(aff_roi_outfile, reorient = FALSE)

double_ortho(syn_brain, template)
ortho2(syn_brain, template, col.y = alpha(hotmetal(), 0.35))
# Visualizing one specific slice
ortho2(syn_brain, template, z=ceiling(dim(template)[3]/2), plot.type="single", col.y = alpha(hotmetal(), 0.35))



### Getting ROI info from Non-Linear Registration
# Where is ROI placed in the template? 
# extracting JHU Eve atlas type I and labels
atlas = "JHU_MNI_SS_WMPM_TYPE-I"
txtfile = file.path(neurodir, "Template", paste0(atlas, "_SlicerLUT.txt"))

### read look up table (LUT)
jhut1.df = read.table(txtfile, stringsAsFactors = FALSE)
jhut1.df = jhut1.df[, 1:2]
# Create 2-columned dataframe (index = numeric lable for voxel, label = label name  )
colnames(jhut1.df) = c("index", "label")
jhut1.df$index = as.numeric(jhut1.df$index)

# Print data frame
jhut1.df[1:4,]

# Read in the template image
jhut1.img = readNIfTI(file.path(neurodir, "TEMPLATE", paste0(atlas, ".nii.gz")))

# Obtain the numeric lables from the atlas
uimg = sort (unique(c(jhut1.img)))

# Obtain the numeric labels from the LUT
all.ind = jhut1.df$index

# Chekc that all numeric lables from the atlas are in LUT
stopifnot(all(uimg %in% all.ind))

hist(c(syn_roi[syn_roi > 0]))

# Treshold the ROI to binary
# Use a weighted sum over the ROI

# Make a data frame with the index of the atlas and the value of the ROI at that voxel
# Data frame with 
roi.df = data.frame(index = jhut1.img[syn_roi > 0],
                    roi = syn_roi[ syn_roi > 0])

# Obtain the number (sum) of voxels that have an roi
# value > 0.5 in the roi by the index of labels
# go through each index (voxel), add voxels that are greater than 0.5 
label_sums = ddply(roi.df, .(index), summarize,
                   sum_roi = sum(roi), sum_roi_thresh = sum(roi > 0.5))
# merge with the LUT that has acutal labels so we can match index with labels
label_sums = merge(label_sums, jhut1.df, by="index")

sums = label_sums

# Assign labels to the row names
rownames(label_sums) = label_sums$label

# Reorder labels from the most to the least engaged
label_sums$label = label_sums$index = NULL

lable_sums = label_sums[order(label_sums$sum_roi, decreasing = TRUE), ]

# calculate the percent of the tumor engaging the region
label_pct = t(t(label_sums)/colSums(label_sums)) * 100 
head(round(label_pct, 1), 10)

