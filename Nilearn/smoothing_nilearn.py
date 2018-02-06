from nilearn import image

# Smoothing
smoothed_img = image.smooth_img("/Users/SB/Desktop/sample_data/sub-012_T1w.nii.gz",fwhm=1)
smoothed_img.to_filename("/Users/SB/Desktop/sub-012_smoothed.nii.gz")