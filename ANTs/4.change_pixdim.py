

nifti_tool -mod_hdr -prefix test_epi_edited.nii -infiles test_epi.nii -mod_field pixdim '1.0 4.0 1.7188 1.7188 DESIREDTR 0.0 0.0 0.0'
nifti_tool -mod_hdr -prefix test_epi_edited.nii -infiles sub-001_normalized.nii.gz -mod_field pixdim '1.0 4.0 1.7188 1.7188 1.0 0.0 0.0 0.0'