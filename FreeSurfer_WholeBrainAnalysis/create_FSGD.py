import pandas as pd
import numpy as np

# DEMEAN AGE
# DEMEAN COVARIATES


infile = "/Volumes/study4/midusref/DATA/mri/processed/freesurfer/david/freesurfer_with_pwb.csv"
outfile = "/Users/SB/Desktop/gender_age_pwb_david.fsgd"

def create_variables():
	df1 = pd.read_csv(infile, sep=',')
	df2 = df1.iloc[:, [0, 42, 605, 606, 609]]
	df3 = df2.sort_values(["subID"])

	# Rename Columns
	#df3.columns = ['subID', 'R5PGENDER', 'R5PAGE']

	#df3.loc[:,'Variables'] = df3.loc[:,'Variables'].astype(int)
	# Replace R5PGENDER coding
	df3.loc[df3['R5PGENDER'] == 1, 'R5PGENDER'] = 'Class1'
	df3.loc[df3['R5PGENDER'] == 2, 'R5PGENDER'] = 'Class2'

	# Round Up to 1 Decimal Points
	df3.loc[:,'scaled_age'] = df3.loc[:,'scaled_age'].round(1)
	df3.loc[:,'scaled_PWB_Composite'] = df3.loc[:,'scaled_PWB_Composite'].round(1)
	df3.loc[:,'PWB_avgXAGE'] = df3.loc[:,'PWB_avgXAGE'].round(1)

	# Add a + sign to age to justify alignment
	df3.loc[df3['scaled_age'] > 0, 'scaled_age'] = '+' + df3['scaled_age'].astype(str)
	df3.loc[df3['scaled_PWB_Composite'] > 0, 'scaled_PWB_Composite'] = '+' + df3['scaled_PWB_Composite'].astype(str)
	df3.loc[df3['PWB_avgXAGE'] > 0, 'PWB_avgXAGE'] = '+' + df3['PWB_avgXAGE'].astype(str)

	# Convert column subID's datatype as strings
	df3.loc[:,'subID'] = df3.loc[:,'subID'].astype(str)

	# Zero pad subID
	df3['subID'] = df3['subID'].apply(lambda x: x.zfill(3))

	# Insert column of "Input"s 
	df3.insert(loc=0, column='Variables', value='Input')
	
	# Make fsdg file 
	df3.to_csv(outfile, index=False, sep=' ', header=False) #float_format='%.2f')
	
	#df4 = pd.read_csv(outfile, sep='\t')
	
	#print (df4)
	#with open(outfile, 'w') as f:
		#f.write(df3.__repr__())

def add_headers():
	with open(outfile, 'r+') as f:
		lines = f.read()
		f.seek(0)
		f.write("GroupDescriptorFile 1\n")
		f.write("Title Cortical Thikness Relation with Age\n")
		f.write("Class Class1 plus blue\n")
		f.write("Class Class2 circle green\n")
		f.write("Variable          Age  PWB  AGExPWB\n" + lines)
		#f.close()

def add_suffix(variable1, variable2, variable3):
	with open(outfile, 'a') as f:
		f.write('DefaultVariable {} {} {}'.format(variable1, variable2, variable3))

create_variables()
add_headers()
add_suffix("Age", "PWB", "AGExPWB")