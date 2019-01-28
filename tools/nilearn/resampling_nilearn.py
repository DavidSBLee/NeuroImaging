from nilearn.datasets import MNI152_FILE_PATH
print ('%r' %MNI152_FILE_PATH)

mayo = '/Users/SB/Desktop/Mayo_T1w_template.nii.gz'
anat = "/Users/SB/Desktop/CNN/midus2_nifti/10040/10040_T1w.nii.gz"
func = '/Users/SB/Desktop/sample_data/sub-012_task-emotion-regulation_run-01_bold.nii.gz'

from nilearn.image import load_img
anat_img = load_img(anat)
mni_img = load_img(mni)
func_img = load_img(func)

from nilearn.image import resample_to_img
resampled_anat = resample_to_img(anat_img, mni_img)
resampled_func = resample_to_img(func_img, mni_img)

resampled_anat.to_filename("/Users/SB/Desktop/resampled_anat.nii.gz")
resampled_func.to_filename("/Users/SB/Desktop/resampled_func.nii.gz")