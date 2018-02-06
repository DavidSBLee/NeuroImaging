#install.packages("fslr")
library(fslr)
library(oro.nifti)
# Always have to do this to use fsl functions in R studio
Sys.getenv("FSLDIR")
have.fsl()
# If have.fsl()=FALSE
# If on my Mac
options(fsl.path= "/Users/SB/Applications/fsl")
# If on Work Mac
#options(fsl.path= "/apps/fsl-latest")

# Should be True

setwd("/Users/SB/Desktop/Neurohacking_data/kirby21/visit_1/113")
#setwd("/home/slee/Desktop/Neurohacking_data/kirby21/visit_1/113")
nim=readNIfTI("113-01-MPRAGE.nii.gz", reorient = FALSE)



# In R
mean(nim)

# In FSL (After loading in FSLR package)
fslstats(nim, opts="-m")
fslstats("113-01-MPRAGE.nii.gz",opts="-m")


### Biasfield correction - to get the intenities on a comparable scale
fast_img = fsl_biascorrect(nim, retimg=TRUE)

# Create subtracted image
sub.bias <- niftiarr(nim, nim-fast_img)

# quantile the differene image using these as breaks
q=quantile(sub.bias[sub.bias !=0],probs = seq(0,1,by=0.1))

install.packages("scales")
library(scales)

# get a diverging gradient palette
fcol=div_gradient_pal(low="blue",mid="yellow",high="red")

ortho2(nim,sub.bias,col.y = alpha(fcol(seq(0,1, length=10)), 0.5), ybreaks = q, ycolorbar=TRUE, text = paste0("Original Image Minus N4", "\n Bias-Corrected Image"))


### look at histograms of corrected images vs original images
slices = c(2,6,10,14,18)
vals = lapply(slices, function(x){
	cbind(img=c(nim[,,x]),fast = c(fast_img[,,x]),
		slice = x)
})
vals = do.call("rbind", vals)
vals = data.frame(vals)
vals = vals[vals$img > 0 & vals$fast > 0,]
colnames(vals)[1:2] = c("Original Value", "Bias-Corrected Value")

#install.packages("reshape")
library(reshape)
v = melt(vals, id.vars = "slice")

#install.package("ggplot2")
library(ggplot2)
g = ggplot(aes(x = value,
		colour = factor(slice)),
	data = v) + geom_line(stat="density") + facet_wrap(~ variable)

g = g + scale_colour_discrete(name = "Slice #")