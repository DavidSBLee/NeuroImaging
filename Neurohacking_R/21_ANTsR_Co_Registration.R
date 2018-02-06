# Baseline FLAIR, T2, and T1
# We need to reigister FLAIR and T2 into T1

library(extrantsr)
library(ANTsR)
library(scales)

kirbydir <- "/Users/SB/Desktop/Neurohacking_data/kirby21"
mridir = file.path(kirbydir, "visit_1", "113")
T2_file = file.path(mridir, "113-01-T2w.nii.gz")

# T2(infile) that will be registerd to T1 (template)
reg_T2_img = ants_regwrite(filename = T2_file, template.file = T1, typeofTransform = "Rigid", verbose = FALSE)

# Fliar(infile) registred to T1 (template)
flair_file = file.path(mridir, "113-01-FLAIR.nii.gz")
reg_flair_img = ants_regwrite(filename = flair_file, template.file = T1, typeofTransform = "Rigid", verbose = FALSE)

# Way to check or tilts or shifts...
double_ortho(T1, reg_T2_img)
dobule_ortho(T1, reg_flair_img)

# Over-plotting (overlays)
ortho2(T1, reg_T2_img, col.y = alpha(hotmetal(), 0.25))
ortho2(T1, reg_flair_img, col.y = alpha(hotmetal(), 0.25))