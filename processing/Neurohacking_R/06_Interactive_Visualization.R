library(oro.nifti)

setwd("/home/slee/Desktop")

fname="Output_3D_File"

print({nii_T1= readNIfTI(fname=fname)})

# Visulaize distribution of intensities of entire image

# Two plots, two columns, one row 
par(mfrow=c(1,2))

# Set margins of the plots to 0
o<-par(mar=c(4,4,0,0))

# create histogram on the nifti object (all the intensities of the nifti image), color the histogram, and change x & y labels
# distribution of the intensities

# large spike at 0, outside of brain is 0
hist(nii_T1, breaks = 75,prob=T, xlab="T1 intensities", col=rgb(0,0,1,1/2), main="");

# intensities greater than 20
# 20 is rather small to just lop of the bottom area of the histogram, so we visualize the *majority*
hist(nii_T1[nii_T1 > 20], breaks = 75, prob=T, xlab="T1 intensities > 20", col=rgb(0,0,1,1/2), main="")

#highintensity coud either mean hyperinstensity or artifact

# Back mapping : derive statistic from the image, and plot an overlay on the image

# Create logical operator (True or False)
# Whether specific voxel is from 300 to 400 inclusive (so 399)
is_btw_300_400<- ((nii_T1>300) & (nii_T1<400))

#Copy nifti and call it nii_T1_mask
nii_T1_mask <- nii_T1

nii_T1_mask[!is_btw_300_400] = nii_T1_mask
overlay(nii_T1, nii_T1_mask, z=11, plot.type="single")

overlay(nii_T1, nii_T1_mask

orthogrpahic(nii_T1, nii_T1_mask, xyz=c(200,220,11), text="Image overlaid with mask", text.cex = 1.5)