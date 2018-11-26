#!/bin/python3

import os
import glob
import csv
import pandas as pd

class ScanEprimeDivider:

	def __init__(self, subject_number, scan_eprime_dir="/study/midus3/processed_data/Temporary/Big/", 
		scan_eprime_by_run_output_dir="/study/midus3/processed_data/Temporary/Small/", study_name="MIDUS3"):
		self.scan_eprime_dir = scan_eprime_raw_dir
		self.scan_eprime_by_run_output_dir = scan_eprime_output_dir
		self.study_name = study_name
		self.subject_number = subject_number

	def set_column_headers(self):
		column_header_list = ['onset',
		'duration',
        'database',
        'Response_Time_Face',
        'stimulus',
        'correct',
        'valence',
        'valenceFollowing',
        'gender',
        'response',
        'face_correct_response',
        'sociality',
        'groups',
        'onset_trimmed',
        'Blocks']

    	return column_header_list


    	#Define column header names
    def create_csv_writer(self):
    	column_header_list = self.set_column_headers()
    	row_writer = csv.DictWriter(newTsv, fieldnames=column_header_list, delimiter='\t', lineterminator='\n') 
    	return row_writer

    def create_csv_reader(self):
    	row_reader= csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names
    	return row_reader

    def write_header(self):
    	row_writer = create_csv_writer()
    	row_writer.writeheader()

    def compute_and_write_values(self):
    	row_reader = create_csv_reader()
    	row_writer = create_csv_writer()

    	# Compute the values (onset, duration, response time etc.)
        for rows in row_reader:
            blockNum = rows['Blocks']
            # Cast float to maintain the decimal points
            IAPSOnsetTime = float(rows['IAPSPicture.OnsetTime'])/float(1000)
            IAPSOffsetTime = float(rows['IAPSPicture.OffsetTime'])/float(1000)
            IAPSTTL = float(rows['WaitForTTL.RTTime'])/float(1000)
            IAPSOnsetTTLAdjusted = IAPSOnsetTime - IAPSTTL
            IAPSDuration = float(IAPSOffsetTime - IAPSOnsetTime)
            IAPSOnsetTimeTrimmed = IAPSOnsetTTLAdjusted - 8#(float(rows['IAPSPicture.OnsetTime'])-8000)/float(1000)
            IAPSNumber = rows['PictureFile'][:4]
            IAPSValence = rows['valencecategory']
            IAPSSocilaity = rows['Sociality']
            ones = rows['Group']

            taskNum = str(taskNum)
            if taskNum in blockNum:

                row_writer.writerow({'onset': IAPSOnsetTTLAdjusted,
                'duration':IAPSDuration,
                'Response_Time_Face': "n/a",
                'database': "IAPS",
                'stimulus': IAPSNumber,
                'correct': "n/a",
                'valence': IAPSValence,
                'valenceFollowing': "n/a",
                'gender': "n/a",
                'response': "n/a",
                'face_correct_response': "n/a",
                'sociality': IAPSSocilaity,
                'groups': ones,
                'onset_trimmed': IAPSOnsetTimeTrimmed,
                'Blocks':rows['Blocks']})





    def calc_write_values_IAPS(newTsv,tsvFile, taskNum):
        row_writer = csv.DictWriter(newTsv, fieldnames=column_header_list, delimiter='\t', lineterminator='\n') # \t skips column!
        row_reader= csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

        # Write column headers manually
        row_writer.writeheader()

        # Compute the values (onset, duration, response time etc.)
        for rows in row_reader:
            blockNum = rows['Blocks']
            # Cast float to maintain the decimal points
            IAPSOnsetTime = float(rows['IAPSPicture.OnsetTime'])/float(1000)
            IAPSOffsetTime = float(rows['IAPSPicture.OffsetTime'])/float(1000)
            IAPSTTL = float(rows['WaitForTTL.RTTime'])/float(1000)
            IAPSOnsetTTLAdjusted = IAPSOnsetTime - IAPSTTL
            IAPSDuration = float(IAPSOffsetTime - IAPSOnsetTime)
            IAPSOnsetTimeTrimmed = IAPSOnsetTTLAdjusted - 8#(float(rows['IAPSPicture.OnsetTime'])-8000)/float(1000)
            IAPSNumber = rows['PictureFile'][:4]
            IAPSValence = rows['valencecategory']
            IAPSSocilaity = rows['Sociality']
            ones = rows['Group']

            taskNum = str(taskNum)
            if taskNum in blockNum:

                row_writer.writerow({'onset': IAPSOnsetTTLAdjusted,
                'duration':IAPSDuration,
                'Response_Time_Face': "n/a",
                'database': "IAPS",
                'stimulus': IAPSNumber,
                'correct': "n/a",
                'valence': IAPSValence,
                'valenceFollowing': "n/a",
                'gender': "n/a",
                'response': "n/a",
                'face_correct_response': "n/a",
                'sociality': IAPSSocilaity,
                'groups': ones,
                'onset_trimmed': IAPSOnsetTimeTrimmed,
                'Blocks':rows['Blocks']})

    def calc_write_values_faces(newTsv,tsvFile, taskNum):
        row_writer = csv.DictWriter(newTsv, fieldnames=column_header_list, delimiter='\t', lineterminator='\n') # \t skips column!
        row_reader= csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

        # Write column headers manually
        row_writer.writeheader()

        # Compute the values (onset, duration, response time etc.)
        for rows in row_reader:
            blockNum = rows['Blocks']
            # Cast float to maintain the decimal points
            faceOnsetTime = float(rows['Face.OnsetTime'])/float(1000) #CG
            faceOffsetTime = float(rows['Face.OffsetTime'])/float(1000)
            faceTTL = float(rows['WaitForTTL.RTTime'])/float(1000)
            faceOnsetTTLAdjusted = faceOnsetTime - faceTTL
            faceOnsetTimeTrimmed = faceOnsetTTLAdjusted - 8 #(float(rows['Face.OnsetTime'])-8000)/float(1000)
            faceResponseTime = float(rows['Face.RT'])/float(1000) #CB
            faceDuration = float(faceOffsetTime - faceOnsetTime)
            faceNumber = rows['FaceFile'][:2]
            faceGender = rows['Gender']
            faceResponse = rows['Face.RESP']
            faceCorrectResponse = rows['Face.CRESP']
            faceCorrect = rows['Face.ACC']
            ones = rows['Group']
            IAPSValence = rows['valencecategory']

            taskNum = str(taskNum)
            if taskNum in blockNum:
                if faceCorrect == '1':
                    variable = 'Y'
                elif faceCorrect == '0':
                    variable = 'N'
                row_writer.writerow({'onset': faceOnsetTTLAdjusted,
                'duration': faceDuration,
                'Response_Time_Face': faceResponseTime,
                'database': "faces",
                'stimulus': faceNumber,
                'correct': variable,
                'valence': "n/a",
                'valenceFollowing': IAPSValence,
                'gender': faceGender,
                'response': faceResponse,
                'face_correct_response': faceCorrectResponse,
                'sociality': "n/a",
                'groups': ones,
                'onset_trimmed': faceOnsetTimeTrimmed,
                'Blocks':rows['Blocks']})

    #lineterminator is paramter in csv.writer. it is default set to '\r\n' causing double spacing
    def reader_and_writer(newTsv, tsvFile):
        writer = csv.writer(newTsv, delimiter='\t', lineterminator='\n')
        reader = csv.reader(tsvFile, delimiter='\t')

        for row in reader:
            writer.writerow(row)

    def block_one_data_manipulation(temporarySmallPath, subNum, niftiPath):
        # Read in csv
        df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_IAPS-01.tsv', sep='\t')
        df2 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_faces-01.tsv', sep='\t')
        # join the two data frames along rows
        df3 = pd.concat([df1, df2])
        # Sort everything by onset column
        df3 = df3.sort_values('onset')
        # Remove unnecessary blocks column
        del df3['Blocks']
        # Use loc and isnull to replace no responses to "n/a"
        df3.loc[(df3['Response_Time_Face'] == 0), 'Response_Time_Face'] = "n/a"
        df3.loc[(df3['response'].isnull()), 'response'] = "n/a"
        # Write the datafram into tsv format
        df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-EmotionRegulation_run-01_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
        print ('----------Onset file(s) for ' + subNum + '-01 created----------')

    def block_two_data_manipulation(temporarySmallPath, subNum, niftiPath):
        # Read in csv to Pandas
        df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_IAPS-02.tsv', sep='\t')
        df2 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_faces-02.tsv', sep='\t')
        # join the two data frames along rows
        df3 = pd.concat([df1, df2])
        # Sort everything by onset column
        df3 = df3.sort_values('onset')
        # Remove unnecessary blocks column
        del df3['Blocks']
        # Use loc and isnull to replace no responses to "n/a"
        df3.loc[(df3['Response_Time_Face'] == 0), 'Response_Time_Face'] = "n/a"
        df3.loc[(df3['response'].isnull()), 'response'] = "n/a"
        # Write the datafram into tsv format
        df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-EmotionRegulation_run-02_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
        print ('----------Onset file(s) for ' + subNum + '-02 created----------')

    def block_three_data_manipulation(temporarySmallPath, subNum, niftiPath):
        # Read in csv to Pandas
        df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_IAPS-03.tsv', sep='\t')
        df2 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_faces-03.tsv', sep='\t')
        # join the two data frames along rows
        df3 = pd.concat([df1, df2])
        # Sort everything by onset column
        df3 = df3.sort_values('onset')
        # Remove unnecessary blocks column
        del df3['Blocks']
        # Use loc and isnull to replace no responses to "n/a"
        df3.loc[(df3['Response_Time_Face'] == 0), 'Response_Time_Face'] = "n/a"
        df3.loc[(df3['response'].isnull()), 'response'] = "n/a"
        # Write the datafram into tsv format
        df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-EmotionRegulation_run-03_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
        print ('----------Onset file(s) for ' + subNum + '-03 created----------')
class ScanEprimeConverter:

	def __init__(self, subject_number, scan_eprime_raw_dir="/study/midus3/raw-data/scan_eprime/data/", 
		scan_eprime_output_dir="/study/midus3/processed_data/Temporary/Big/", study_name="MIDUS3"):
		self.scan_eprime_raw_dir = scan_eprime_raw_dir
		self.scan_eprime_output_dir = scan_eprime_output_dir
		self.study_name = study_name
		self.subject_number = subject_number

	# def inspect_scan_eprime(self):
	# 	raw_scan_eprime_files = sorted(glob.glob(self.scan_eprime_raw_dir + "/midus3_order[1-2]_eyetracking_v[0-9][0-9]-[0-9][0-9][0-9]-[0-9]*.txt"))
	# 	for file in raw_scan_eprime_files:
	# if os.path.isfile(f'{self.scan_eprime_output_dir} sub-{self.subject_number}_task-ER_events.tsv'):
	# 		pass
	# 	elif not os.path.isfile(f'{self.scan_eprime_output_dir} sub-{self.subject_number}_task-ER_events.tsv'):


	def identify_target_raw_eprime(self):
		infile = glob.glob(f'{scan_eprime_raw_dir} midus3_order[1-2]_eyetracking_v{self.subject_number}-{self.subject_number}.txt')
		return infile

	def set_outfile_name(self):
		outfile = f'{self.scan_eprime_output_dir} sub-{self.subject_number}_task-ER_events.tsv'

		return oufile

	def process(self):
		infile = self.identify_target_raw_eprime()
		outfile = self.set_outfile_name()
		os.system(f'eprime2tabfile {infile} > {outfile}')

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

	def inspect_dicoms(self):
		# raw DICOMs in a set
		raw_dicoms = glob.glob(self.raw_dir + "[0-9][0-9][0-9]")
		dicom_set = set([int(raw.split('/')[4][0:]) for raw in raw_dicoms]) # extracts INTEGERS w/o "0"
		#dicoms.sort()
		return dicom_set

	def inspect_niftis(self):
		# scan subjects that already have niftis
		niftis = glob.glob(self.nifti_dir + self.study_name + "_Imaging/sub-[0-9][0-9][0-9]")
		nifti_set = set([int(nifti.split('/')[5][4:7]) for nifti in niftis]) # in python the set is called hash table
		#niftis.sort()
		return nifti_set

	def identify_target_subject(self):
		dicom_set = self.inspect_dicoms()
		nifti_set = self.inspect_niftis()

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

nifti_converter = NiftiConverter()
nifti_converter.process()
rotator = NiftiRotator("001")
rotator.process()
eprime_converter = ScanEprimeConverter()
eprime_converter.process()


