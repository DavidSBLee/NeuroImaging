#!/bin/python3
import os
import glob

class NiftiRotator:

	def __init__(self, subject_number, nifti_dir="/study/midus3/processed_data/", study_name="MIDUS3"):
		self.nifti_dir = nifti_dir
		self.study_name = study_name
		self.subject_number = subject_number
		self.subject_dir = "sub-" + subject_number

	# def identify_target_subject(self):
	# 	niftis = glob.glob(self.nifti_dir + self.study_name + "_Imaging/sub-[0-9][0-9][0-9]")

	# 	for nifti in niftis:
	# 		subject_dir = nifti.split('/')[5]
	# 		subject_number = subject_dir[4:]

	def fix_task_fMRI_orientation(self, run_number, old_scan_name, new_scan_name):
		target_nifti = f'{self.nifti_dir}{self.subject_dir}/func/{self.subject_dir}_{old_scan_name}_{run_number}_bold.nii.gz'
		if os.path.isfile(target_nifti):
			os.system(f'fslreorient2std {target_nifti} {self.nifti_dir}{self.subject_dir}/func/{self.subject_dir}_{new_scan_name}_{run_number}_bold.nii.gz')
			os.remove(target_nifti)

	def rename_task_fMRI_json(self, run_number, old_scan_name, new_scan_name):
		target_json = f'{self.nifti_dir}{self.subject_dir}/func/{self.subject_dir}_{old_scan_name}_{run_number}_bold.json'
		if os.path.isfile(target_json):
			os.rename(target_json, f'{self.nifti_dir}{self.subject_dir}/func/{self.subject_dir}_{new_scan_name}_{run_number}_bold.json')

	def fix_resting_fMRI_orientation(self):
		target_nifti = f'{self.nifti_dir}{self.subject_dir}/func/{self.subject_dir}_task-rest_bold.nii.gz'
		if os.path.isfile(target_nifti):
			os.system(f'fslreorient2std {target_nifti} {target_nifti}')

	def fix_dwi_orientation(self):
		target_nifti = f'{self.nifti_dir}{self.subject_dir}/dwi/{self.subject_dir}_dwi.nii.gz'
		if os.path.isfile(target_nifti):
			os.system(f'fslreorient2std {target_nifti} {target_nifti}')

	def process(self):
		self.fix_task_fMRI_orientation("run-1", "task-ER", "task-EmotionRegulation")
		self.rename_task_fMRI_json("run-1", "task-ER", "task-EmotionRegulation")
		self.fix_task_fMRI_orientation("run-2", "task-ER", "task-EmotionRegulation")
		self.rename_task_fMRI_json("run-2", "task-ER", "task-EmotionRegulation")
		self.fix_task_fMRI_orientation("run-3", "task-ER", "task-EmotionRegulation")
		self.rename_task_fMRI_json("run-3", "task-ER", "task-EmotionRegulation")
		self.fix_resting_fMRI_orientation()
		self.fix_dwi_orientation()



class NiftiConverter:

	def __init__(self, nifti_dir="/study/midus3/processed_data/", raw_dir="/study/midus3/raw-data/", study_name="MIDUS3"):
		
		self.nifti_dir = nifti_dir
		self.raw_dir = raw_dir
		self.study_name = study_name

	def scan_dicoms(self):
		# raw DICOMs in a set
		raw_dicoms = glob.glob(self.raw_dir + "[0-9][0-9][0-9]")
		dicom_set = set([int(raw.split('/')[4][0:]) for raw in raw_dicoms]) # extracts INTEGERS w/o "0"
		#dicoms.sort()
		return dicom_set

	def scan_niftis(self):
		# scan subjects that already have niftis
		niftis = glob.glob(self.nifti_dir + self.study_name + "_Imaging/sub-[0-9][0-9][0-9]")
		nifti_set = set([int(nifti.split('/')[5][4:7]) for nifti in niftis]) # in python the set is called hash table
		#niftis.sort()
		return nifti_set

	def identify_target_subject(self):
		dicom_set = self.scan_dicoms()
		nifti_set = self.scan_niftis()

		for dicom_number in dicom_set:
			# cast string and zero-pad the subject numbers
			dicom_number_string = str(dicom_number)
			dicom_number_zero_padded = ["0" for i in range(3-len(dicom_number_string))] + [dicom_number_string]
			subject_number = ''.join(dicom_number_zero_padded)
			subject_dir = "sub-" + subject_number
			subject_dicom_path = self.raw_dir + subject_number

			if dicom_number in nifti_set:
				pass

			elif dicom_number not in nifti_set:
				return subject_dir, subject_dicom_path, subject_number

	def extract_scan_info(self, scan_path):
		scan_name = scan_path.split('/')[6][6:]
		return scan_name

	def convert(self, scan_path, scan_type, subject_dir, scan_name):
		#print(self.out_path)
		#os.system("convert_dcm2niix %s %s/%s_%s.nii.gz"%(scan_path, self.nifti_dir, subject_number, scan_name))
		os.system(f'convert_dcm2niix {scan_path} {self.nifti_dir}{subject_dir}/{scan_type}/{subject_dir}_{scan_name}.nii.gz')

	def process(self):

		subject_dir, subject_dicom_path, subject_number = self.identify_target_subject()

		scans = sorted(glob.glob(subject_dicom_path + "/dicoms/*/*.tgz"))

		for scan in scans:
			scan_name = self.extract_scan_info(scan)

			if scan_name == "T1w": # should be 'ORIG_T1w' for scans with pure-filtered T1w's
				scan_type = "anat"
				os.makedirs(self.nifti_dir + subject_dir + "/anat/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, scan_name)

			if scan_name == "task-ER_run-1_bold":
				scan_type = "func"
				os.makedirs(self.nifti_dir + subject_dir + "/func/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, scan_name)

			if scan_name == "task-ER_run-2_bold":
				scan_type = "func"
				os.makedirs(self.nifti_dir + subject_dir + "/func/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, scan_name)

			if scan_name == "task-ER_run-3_bold":
				scan_type = "func"
				os.makedirs(self.nifti_dir + subject_dir + "/func/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, scan_name)

			if scan_name == "task-rest_bold":
				scan_type = "func"
				os.makedirs(self.nifti_dir + subject_dir + "/func/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, scan_name)

			if scan_name == "dwi":
				scan_type = "dwi"
				os.makedirs(self.nifti_dir + subject_dir + "/dwi/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, scan_name)

			if scan_name == "WATER__fmap":
				scan_type = "fmap"
				os.makedirs(self.nifti_dir + subject_dir + "/fmap/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, "magnitude")

			if scan_name == "FieldMap__fmap":
				scan_type = "fmap"
				os.makedirs(self.nifti_dir + subject_dir + "/fmap/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, "fieldmap")

			if scan_name == "asl":
				scan_type = "asl"
				os.makedirs(self.nifti_dir + subject_dir + "/asl/", exist_ok=True)
				self.convert(scan, scan_type, subject_dir, scan_name)

converter = NiftiConverter()
converter.process()
rotator = NiftiRotator("001")
rotator.process()

