library(fslr)

# Setting Path for FSL
Sys.getenv("FSLDIR")
options(fsl.path= "/Users/SB/Applications/fsl")
have.fsl()

setwd("/Users/SB/Desktop/Neurohacking_data/kirby21/visit_1/113")
# T1 weighted image
img = readnii("113-01-MPRAGE.nii.gz")

# View images interactively, so investigate more fluidily than just plotting statically
img
ortho2(img)
fslview(img)

# different viewers
# Mango Viewer
# ITK-SNAP


hist(c(img[img > 10000]), breaks = 200)
quants = quantile(c(img), probs = 0.1)

# Papaya (written in javascript - wrap an R package around it)
library(papayar)
#install.packages("papayar")
#devtools::install_github("muschellij2/papayar")
mask = img > 5e5
ortho2(img, img > 5e5) # 500,000

papaya(list(img, mask))

# another package
#devtools::install_github("muschellij2/itksnapr")
library(itksnapr)
itksnap(grayscale = img)
image(img)
