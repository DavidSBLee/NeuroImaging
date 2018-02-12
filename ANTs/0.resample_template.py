 #!/usr/bin/env python3

import os
 # Resample a template image with 1x1x1 voxel dimension
 # Change the voxel dimension of your choice
 # The change in the voxel dimension will change the number of total dimensions
os.system("ResampleImage 3 /path/to/template /path/to/resampled/template 1x1x1")