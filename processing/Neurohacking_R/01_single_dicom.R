#install.packages("oro.dicom")
library(oro.dicom)

# Set working directory for single image
setwd("/home/slee/Desktop/dicomdir/001_unprocessed_dicoms/T1w")

# Assgign 71th dicom image to variable "slice"
slice = readDICOM("00003.T1w.000071.dcm")

### Basics ###
# Datatype of a dicom image (dicoms are stored as list)
class(slice)
# Two elements within a dicom image (dicoms have header and image)
names(slice)
# Datatype of header (list)
class(slice$hdr)
# Data type of first element of the header (data.frame)
class(slice$hdr[[1]])
# Datatype of image (list)
class(slice$img)
# Datatype of first element of the image (matrix)
class(slice$img[[1]])
# Dimension of first element of the image
dim(slice$img[[1]])

### Playing with the image ###

# Transpose data using t()
# Save the image in d
d = dim(t(slice$img[[1]]))
# Plot using dimensions in the X direction and Y direction
image(1:d[1], 1:d[2], t(slice$img[[1]]), col=gray(0:64/64))

# Look at 101th to 105th voxel in X direction and 121th to 125th voxel in Y direction
slice$img[[1]][101:105, 121:125]

# Histogram of entire slice of the image
	# prob = T makes it density instead of count histrogram
	# [,] means no subsets
hist(slice$img[[1]][,],breaks=50, xlab="FLAIR", prob=T, col=rgb(0,0,1,1/4), main="")

### Playing with the header ###
hdr = slice$hdr[[1]]
# Names in header
names(hdr)
# Items in this particular header (352)
hdr$name
# Resolution of image Subset the header over two items (1,1) == each pixel in the slice has dimension of 1mm by 1mm)
hdr[hdr$name == "PixelSpacing", "value"]
# Image acquistion parameter
hdr[hdr$name == "FlipAngle", ]