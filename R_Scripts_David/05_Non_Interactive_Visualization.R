library(oro.nifti)

setwd("/home/slee/Desktop")

fname="Output_3D_File"

print({nii_T1= readNIfTI(fname=fname)})

# Plot 11th slice of nifti

# Defulat R function
# d = dimensions of the image (so in this case = 256)
d = dim(nii_T1)
# By default, image function uses heat.colors(12) from graphics package (graphics:image)
# Colors can be reset: (col=gray(0:64/64))
# Plot from 1 to d[1] (rows) , 1 to d[2] (columns), pass nifti object subset to 11th slice (taking 11th slice of the brain and visualizing it)
image(1:d[1],1:d[2],nii_T1[,,11],xlab="",ylab="")



### Oro.Nifti fucntions ###
### Defaulted to gray view ###

# Plot 11th slice of nifti (Alternative)
image(nii_T1, z=11, plot.type="single")

# By default, images will go axially
image(nii_T1)

# Another way: orthographic view from oro.nifti package
# Visulaize at one specfici point of the brain, in all three slices (axial, sagital, coronal)
orthographic(nii_T1, xyz=c(200,220,11))


# These are non-interactive visualization