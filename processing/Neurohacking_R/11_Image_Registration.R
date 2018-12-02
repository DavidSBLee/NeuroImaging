# Registration
# is a spatial transformation of one or multiple images
# with the goal of making locations (voxels, ROIs) have the 
# same or similar interpretation

# AKA, Shift images in a way that locations match with the template
# Not perfect, but good step

# Co-registration
# means same subject
# fewer degrees of freedom, no need for huge registration
# 


# Linear Registration : RIGID
# 6 degrees of freedom (3 angles to rotate & 3 translation vectors)
# consists of a translation and a rotation
# take the image, rotate it, and trasnlate it

# Linear Registration : AFFINE
# 12 degrees of freedom
# matrix A has 9 entries (3x3 matrix) and translation vector has
# 3 entries: 

# Non-linear Registration
# 