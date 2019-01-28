import os
import numpy as np
from nibabel.testing import data_path
import nibabel as nib

file = os.path.join(data_path, '/Users/SB/Desktop/sub-012_T1w.nii.gz')

# set numpy to print only 2decimal digits for neatness
np.set_printoptions(precision=2, suppress=True)

# Load the nibabel image
# object img is an instance of nibabel image
img = nib.load(file)

### img objct inspection
# shape
img.shape
# pointing to the image array data (check if image has an array proxy)
img.dataobj
# affine: a 4x4 matrix mapping array in RAS+ world coordinate space
img.affine
# data type: should return "True" if data on disk are 16bit signed integers
img.get_data_dtype() == np.dtype(np.int16)
# affine transformation that determines the world-coordinates of the image elements
img.affine.shape

### img header inspection
# header: metadata for the image (NIfTI metadta)
img.header
print(img.header)

# header information via format-specific header object
hdr = img.header

# Access all NIfTI-specific inforamtion
hdr.get_xyzt_units()
# shap in array
hdr.get_data_shape()
# data type
hdr.get_data_type()
# voxel size in mm
hdr.get_zooms()

# Get set individual Fields in the header using dict (mapping-type) item accss
hdr['cal_max']

# Change header Fields
hdr['cal_max'] = 1200
hdr['cal_max']
# Access to the raw header information
raw = hdr.structarr
raw['xyzt-units']

### Creating and Saving
# Creating a new Image: at minimum, only need image data & image coordinate transformaion (affine)
data = np.ones((32, 32, 15, 100), dtype=np.int16)
img = nib.Nifti1Image(data, np.eye(4))
img.get_data_dtype() == np.dtype(np.int16)
img.header.get_xyzt_units()

# Save a image to a file
img.to_filename(os.path.join('/Users/SB/Desktop/test.nii.gz'))
nib.save(img, os.path.join('/Users/SB/Desktop/test.nii.gz'))


### Array vs. Array Proxy
# An Image can be stored in the image object as numpy array OR 
# OR on disk to access later "via an array proxy" (not the array itself, but something that represents the array)

### Array Proxies and proxy images
# Array proxy allows to create image object w/o immediately loading all the array from the disk 
# Called "proxy images", b/c image data is not yet an array, but the array proxy points to array data on disk

# Check iamge property (if the image has a "array proxy")
img.dataobj
nib.is_proxy(img.dataobj)

# Access to the proxy iamge (without loading any main image data into memory)
proxy_image_data = img.get_data()
proxy_image_data.shape
type(proxy_image_data)

### Array Images
# Create images from numpy arrays
array_data = np.arange(24, dtype=np.int16).reshape((2, 3, 4))
affine = np.diag([1, 2, 3, 1])
array_img = nib.Nifti1Image(array_data, affine)

# the image is stored as a numpy array, so no version of the array on disk
# check image property
array_img.dataobj
array_img.dataobj is array_data

# Access to the array image
array_image_data = array_img.get_data()
array_image_data.shape
array_image_data is array_data

# Save and Load
nib.save(array_img, '/Users/SB/Desktop/array_image.nii')
img_again = nib.load('/Users/SB/Desktop/array_image.nii')
img_again.shape

# or
img.to_filename('/Users/SB/Desktop/proxy_image.nii')
img_again = nib.load('/Users/SB/Desktop/proxy_image.nii')
img_again.shape

# get and set the filename
img_again.set_filename('/Users/SB/Desktop/another_image.nii')
img_again.get_filename()

### Details of files and images
# for an image saved on disk, has attribute called "file_map". 
# "img.file_map" is a dictionary; key (fileNames) and value (FileHolder obejct)
list(img_again.file_map)
img_again.file_map['image'].filename

# File that need more than one file to make up the image
pair_img = nib.Nifti1Pair(array_data, np.eye(4))
nib.save(pair_img, 'my_pair_image.img')
sorted(pair_img.file_map)
pair_img.file_map['header'].filename
pair_img.file_map['image'].filename

# Older Analyze format 
ana_img = nib.AnalyzeImage(array_data, np.eye(4))
sorted(ana_img.file_map)

# change contents of the file_map using set_filename
ana_img.set_filename('analyze_image.img')
ana_img.file_map['image'].filename
ana_img.file_map['header'].filename

### Data Scailing
# scl_slope and scl_inter

# Create images from numpy arrays
array_data = np.arange(24, dtype=np.int16).reshape((2, 3, 4))
affine = np.diag([1, 2, 3, 1])
array_img = nib.Nifti1Image(array_data, affine)
array_header = array_img.header

# Default scaling values are NaN(undefined)
array_header['scl_slope']
array_header['scl_inter']

# Get scailing values with get_slope_inter()
array_header.get_slope_inter()
# returns (None, None); "None" means "NaN"

# Set scailing values in the image header 
array_header.set_slope_inter(2, 10)
array_header.get_slope_inter()
array_header['scl_slope']
array_header['scl_inter']

# Setting sale factors has NO effect on image data before save/load
array_img.get_data()

# Save/Load/check that data array has the scaling applied
nib.save(array_img, 'scaled_image.nii')
scaled_img = nib.load('scaled_image.nii')
scaled_img.get_data()

# Header for loaded image has scailing reset to undefined
scaled_img.header.get_slope_inter()

# Access original slope and intercept in the array proxy
scaled_img.dataobj.slope
scaled_img.dataobj.inter



