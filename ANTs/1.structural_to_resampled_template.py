 #!/usr/bin/env python3
import subprocess
import glob
import sys
import os

print(sys.argv)
subNum = sys.argv[1]

path = "/study4/midusref/DATA/mri/processed/david/%s"%(subNum)
#brain = glob.glob("%s/%s_T1w_fslanat_brain.nii.gz"%(path, subNum))

#os.mkdir("/study4/midusref/DATA/mri/processed/david/%s"%(subNum))
subprocess.call(["antsRegistrationSyN.sh", "-d", "3", "-f", "/home/slee/Desktop/xMAYO_T/template_brain_MIDUS3_resampled.nii.gz", "-m", "%s/%s_T1w_fslanat_brain.nii.gz"%(path, subNum), "-o", "/study4/midusref/DATA/mri/processed/david/%s/%s_structural_to_resampled_template_"%(subNum,subNum), "-t", "s"])