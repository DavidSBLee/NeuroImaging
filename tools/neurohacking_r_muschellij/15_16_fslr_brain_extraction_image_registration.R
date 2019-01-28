library(fslr)

# Inhomogeneity correction - name it "Fast"
### Then to BRAIN EXTRACTION ###

# Check for FSL
Sys.getenv("FSLDIR")
options(fsl.path= "/Users/SB/Applications/fsl")
have.fsl()

setwd("/Users/SB/Desktop/Neurohacking_data/BRAINIX/NIfTI")
# inhomegeniety correted image (ideally)
nim=readNIfTI("T1.nii.gz", reorient = FALSE)

# fslr::fslbet  is used to call FSL commands
# return images true = retimg=TRUE

bet_fast = fslbet(infile=nim, retimg = TRUE)

# Create NIfTIarray , fill with "1"
bet_fast_mask <- niftiarr(bet_fast, 1)

# Determine what areas of skull-stripped image actulaly contain BRAIN TISSUE
# Binary Variable (True&False)
is_in_mask = bet_fast > 0

# Assign NA value to areas taht are non-brain
bet_fast_mask[!is_in_mask] <- NA

# Brain Extracted Image
orthographic(bet_fast)

# Original Image w/ overlay of mask
orthographic(nim,bet_fast_mask)


# When bet hasn't worked properly 
# re run using "cog" function from fslr
# find center of gravity of the image - for better segmentation
cog = cog(bet_fast, ceil=TRUE)

# create phrase that we can pass in to fsl gives us option to pass in center of gravity 
# pasting together -c (indication for center of gravity from bet) and coordinates of center of gravity 
cog = paste("-c", paste(cog, collapse= " "))

# option to put in center of gravity
bet_fast2 = fslbet(infile=nim, retimg=TRUE, opts=cog)

### IMAGE_Registration ###

######################### Rigid Registration

tempdir <- "/Users/SB/Desktop/Neurohacking_data/Template"

# Load in MNI Template (made with 152 subjects)
template <- readNIfTI (file.path(tempdir, "/MNI152_T1_1mm_brain.nii.gz"), reorient = FALSE)

# Take input to reference filename
registered_fast = flirt(infile=bet_fast2, reffile = template, dof = 6, retimg = TRUE)

orthographic(template)
orthographic(registered_fast)

# Template and Registered_Fast have same dimensions now, 
# proving that there is intrapolation going on to fit the images
dim(template)
dim(registered_fast)
dim(bet_fast2)

######################### Affine Image Registration allowing for global scaling 
reg_fast_affine = flirt(infile=bet_fast2, reffile = template, dof = 12, retimg = TRUE)

orthographic(reg_fast_affine)

########################## Non Linear Registration (FNIRT)
# Affine has to come before Non-Linear (R has a function for this)
fnirt_fast = fnirt_with_affine(infile=bet_fast2, reffile = template, outfile = "FNIRT_to_Template", retimg=TRUE)





