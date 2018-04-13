import pandas as pd
import numpy as np


infile = "/Volumes/study4/midusref/DATA/mri/processed/freesurfer/david/freesurfer_ref_original.csv"
outfile = "/Users/SB/Desktop/output.txt"

def create_variables():
	df1 = pd.read_csv(infile, sep=',')
	df2 = df1.iloc[:, [0, 68, 69]]
	df3 = df2.sort_values(["ID"])

	# Rename Columns
	df3.columns = ['subID', 'Gender', 'Age']

	#df3.loc[:,'Variables'] = df3.loc[:,'Variables'].astype(int)
	# Replace gender coding
	df3.loc[df3['Gender'] == 1, 'Gender'] = 'Class1'
	df3.loc[df3['Gender'] == 2, 'Gender'] = 'Class2'

	# Convert column subID's datatype as strings
	df3.loc[:,'subID'] = df3.loc[:,'subID'].astype(str)
	# Zero pad subID
	df3['subID'] = df3['subID'].apply(lambda x: x.zfill(3))

	# insert column of "Input"s 
	df3.insert(loc=0, column='Variables', value='Input')
	df3.to_csv(outfile, index=False, sep='\t', header=False)

def add_headers():
	with open(outfile, 'r+') as f:
		lines = f.read()
		f.seek(0)
		f.write("GroupDescriptorFile 1\n")
		f.write("Title Cortical Thikness Relation with Age\n")
		f.write("Class class1 plus blue\n")
		f.write("Class class2 circle green\n")
		f.write("Variable           Age\n" + lines)
		#f.close()

def add_suffix(variable):
	with open(outfile, 'a') as f:
		f.write('DefaultVariable {}'.format(variable))

create_variables()
add_headers()
add_suffix("Age")