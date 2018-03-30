import pandas as pd
import numpy as np
import math
import glob

# SSD Calculation
#SSD = sqrt( (dx(t)-dx(t-1))^2 + (dy(t)-dy(t-1))^2 + (dz(t)-dz(t-1))^2 + (da(t)-da(t-1))^2 + (db(t)-db(t-1))^2 + (dc(t)-dc(t-1))^2 )

# Function for calculating difference t1-t  (lag 1 difference)
def calculate_diff(t, tMINUS1, newColumnHeader):
	# Extract the column of interest
	df4 = df2[t]
	df5 = df3[tMINUS1]
	# Merge extracted columns
	df6 = pd.concat([df4,df5], axis=1)
	# Calculate t1-t
	df6[newColumnHeader] = df6.loc[:, t] - df6.loc[:, tMINUS1]
	# Add 0,0,0 to row 1 
	df6.loc[-1] = [0,0,0]
	df6.index = df6.index + 1
	df6 = df6.sort_index()
	# Extract the difference
	df7 = df6[newColumnHeader]
	return (df7)


#path = "/Volumes/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis/sub-MRID-[0-9][0-9][0-9][0-9][0-9]/func/*task-rest_bold_mod_mcf.par"
path = "/Volumes/study4/midusref/midusref_imaging_public/MIDUSREF_Imaging_Analysis/sub-MRID-30725/func/*task-rest_bold_mod_mcf.par"
files = sorted(glob.glob(path))
print (len(files))
for file in files:
	# Extract subject number
	subNum = file.split('/')[6][-5:]

	# Read in to pandas
	df1 = pd.read_csv(file, names = ["A", "B", "C", "D", "E", "F"], header=None, squeeze=True) # squeez is reading it as Series

	# Split based on two spaces, put them into one column
	df1 = pd.DataFrame(df1['A'].str.split('  ', 5).tolist(), columns = ['A', 'B', 'C', 'D', 'E', 'F'])

	# Put data into float
	df1 = df1.astype(float)

	# Covert Rotations(Radians) into degrees
	# Displacement on the surface of a sphere that was 57mm
	# A,B,C Rotations & D,E,F Translations
	df1['A'] = (df1['A']*180)/math.pi
	df1['B'] = (df1['B']*180)/math.pi
	df1['C'] = (df1['C']*180)/math.pi
	df1['D'] = df1['D']
	df1['E'] = df1['E']
	df1['F'] = df1['F']

	# Select all the rows excpet row 1
	# Create t
	df2 = df1[1:]
	df2 = pd.DataFrame(df2)
	df2.reset_index(drop=True, inplace=True)

	# Create t-1
	# Select all the rows except row 236 and rename columms
	df3 = df1[:-1]
	df3 = pd.DataFrame(df3)
	df3.reset_index(drop=True, inplace=True)
	df3.columns = ["a","b","c","d","e","f"]

	# Store return values into dataframe variable
	dfA = calculate_diff('A', 'a', 'diff_A')
	dfB = calculate_diff('B', 'b', 'diff_B')
	dfC = calculate_diff('C', 'c', 'diff_C')
	dfD = calculate_diff('D', 'd', 'diff_D')
	dfE = calculate_diff('E', 'e', 'diff_E')
	dfF = calculate_diff('F', 'f', 'diff_F')

	# Merge all the differences
	master_df = pd.concat([dfA, dfB, dfC, dfD, dfE, dfF], axis=1)

	# Square the values across the dataframe
	master_df['diff_A'] = master_df['diff_A']**2
	master_df['diff_B'] = master_df['diff_B']**2
	master_df['diff_C'] = master_df['diff_C']**2
	master_df['diff_D'] = master_df['diff_D']**2
	master_df['diff_E'] = master_df['diff_E']**2
	master_df['diff_F'] = master_df['diff_F']**2

	# Sum the values across the dataframe
	master_df['sum'] = master_df.sum(axis=1)

	# Square Root of the values across the dataframe
	master_df['sqrt'] = np.sqrt(master_df[['sum']])

	# Compare each TR's SSD to 0.2mm threshold
	counter = 0
	for index, row in master_df.iterrows():
		if row['sqrt'] > 0.2:
			#print("high motion!")
			counter += 1

	print ("total TR with high motion:", str(counter))

	output = "/Users/SB/Desktop/output.txt" 
	
	with open (output, 'a') as outfile:
		if counter == 0:
			outfile.write(subNum)
			outfile.write(": ")
			outfile.write(str(counter))
			outfile.write("\n")


#0 인거 삭제해야함 or delete row 120
"""
df4 = df2['A']
	df5 = df3['a']

	df6 = pd.concat([df4,df5], axis=1)
	df6['diff_A'] = df6.loc[:, "A"] - df6.loc[:, "a"]
	df6.loc[-1] = [0,0,0]
	df6.index = df6.index + 1
	df6 = df6.sort_index()
	dfA = df6['diff_A']
	return (dfA)
"""
# Compute calculation by row and put results in an extra column
#df1['sum'] = df1.sum(axis=1)
#df1['sqrt'] = np.sqrt(df1[['sum']])

# Put the average of column sqrt


# Write to csv
master_df.to_csv("/Users/SB/Desktop/junk.csv", sep=',', index=False, header=True)

