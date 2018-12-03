import nibabel as nib

# smoothing structural
img = nib.load("/Users/SB/Desktop/sample_data/sub-012_T1w.nii.gz")

smoothed_img = image.smooth_img(img, fwhm = 1)

nib.save(smoothed_img, '/Users/SB/Desktop/test.nii.gz')



# smoothing functional

img = nib.load("/Users/SB/Desktop/sample_data/sub-012_task-emotion-regulation_run-01_bold.nii.gz")

smoothed_img = image.smooth_img(img, fwhm = 5)

nib.save(smoothed_img, '/Users/SB/Desktop/test_func.nii.gz')
