#!/bin/python3

# Author: David SB Lee
# First Compiled: 8/30/17
# Last Updated: 12/08/2017
# Updated Content: (10/13/2017) Changed run-1 ----> run-01
# Updated Content: (10/14/2017) Created several functions to make the code more readable and efficient
# Updated Conetnt: (10/24/2017) Changed small & big paths to fit BIDS validation
#								Changed NaN to n/a to fit BIDS validation
# Updated Conetnt: (10/27/2017) Organization of Onset files (include both IAPS/face in same column and sort!!)
# Updated Conetnt: (10/30/2017) Created more necessary columns and they look beautiful
# Updated Conetnt: (11/01/2017) Fixed bug in decmial points
# Updated Conetnt: (11/02/2017) Added "groups" column tu pull Parametric modulatio as "1"
# Updated Content: (11/20/2017) Fixed OnsetTime to reflect "TTL adjustment"
# Updated Content: (12/08/2017) Python3 Compatibility
# Updated Conetnt: (01/10/2018) Bug Fix in onset creation (lines 177, 178, 209, 210)

# Purpose: Separate Onset File into three by-block

# Things to change when runing on different data set
	# 1. all paths
	# 2. all splits

import glob
import csv
import os
import pandas as pd

# Define column header names 
def calc_write_values_IAPS(newTsv,tsvFile, taskNum):
	rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
	rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

	# Write column headers manually
	rowWriter.writeheader()
	
	# Compute the values (onset, duration, response time etc.)
	for rows in rowReader:
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
			
			rowWriter.writerow({'onset': IAPSOnsetTTLAdjusted,
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
	rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
	rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

	# Write column headers manually
	rowWriter.writeheader()

	# Compute the values (onset, duration, response time etc.)
	for rows in rowReader:
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
			rowWriter.writerow({'onset': faceOnsetTTLAdjusted,
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
	# Read in csv to Pandas
	df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_IAPS-01.tsv', sep='\t')
	df2 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_faces-01.tsv', sep='\t')
	# Use loc and isnull to replace negative responset times to "n/a"
	#df1.loc[(df1['Response_Time_Face']).astype(float) < 0 | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "n/a"
	#df2.loc[(df2['Response_Time_Face']).astype(float) < 0 | (df2['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "n/a"
	#df1['Response_Time_Face'] = pd.to_numeric(df1['Response_Time_Face'], errors='coerce')
	#df2['Response_Time_Face'] = pd.to_numeric(df2['Response_Time_Face'], errors='coerce')
	#df1.loc[df1['Response_Time_Face'] < 0] = 'n/a'
	#df2.loc[df2['Response_Time_Face'] < 0] = 'n/a'
	# Remove unnecessary blocks column
	#del df1['Blocks']
	#del df2['Blocks']
	# Put csv's into dataframe
	#df1 = pd.DataFrame(df1)
	#df2 = pd.DataFrame(df2)
	# join the two data frames along rows 
	df3 = pd.concat([df1, df2])
	# Sort everything by onset column
	df3 = df3.sort_values('onset')
	# Remove unnecessary blocks column
	del df3['Blocks']
	# Use loc and isnull to replace no responses to "n/a"
	df3.loc[(df3['Response_Time_Face'] == 0), 'Response_Time_Face'] = "n/a"
	df3.loc[(df3['response'].isnull()), 'response'] = "n/a"
	
	#df99['Response_Time_Face'] = pd.to_numeric(df99['Response_TimeFace'], errors='coerce')
	#df99.loc[(df99['Response_Time_Face'] < 0 ) | (df99['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "n/a"
	#df99.replace("0", "n/a")
	# Write the datafram into tsv format
	df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-emotion-regulation_run-01_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
	print ('----------Onset file(s) for ' + subNum + '-01 created----------')

	# Only perform this if you need original Onset File for some reason, you shouldn't really
	"""
	df3 = pd.read_csv(temporarySmallPath + subNum + '-temporary-01.tsv', sep='\t',) # usecols = ['columnname'] could be useful here
	# cut the index
	df4 = df3.ix[:29]
	# Put two csvs together
	df5 = pd.concat([df1, df4], axis=1)
	# Put the combined csvs into pandas data frame
	df5 = pd.DataFrame(df5)
	# Write the datafram into tsv format
	df5.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-ER_run-01_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
	"""

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
	df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-emotion-regulation_run-02_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe
	print ('----------Onset file(s) for ' + subNum + '-02 created----------')
	# Only perform this if you need original Onset File for some reason, you shouldn't really
	"""
	df3 = pd.read_csv(temporarySmallPath + subNum + '-temporary-02.tsv', sep='\t')
	#df3 = df2.drop(df2.index[[0,1,2,3,4]])
	#df4 = df3.drop(df3[:-3])
	#df2 = df2[df2.Blocks != 1]
	df4 = df3.ix[30:59]
	df4 = df4.reset_index(drop=True)
	#df5 = pd.merge(df1, df3, left_index=True, right_index=True)
	df5 = pd.concat([df1, df3], axis=1)
	# Put into pandas data frame
	df5 = pd.DataFrame(df5)
	# Write the datafram into tsv format
	df5.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' +  subNum + '_task-ER_run-02_events.tsv', sep='\t', index=None)
	"""

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
	df3.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-emotion-regulation_run-03_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe

	print ('----------Onset file(s) for ' + subNum + '-03 created----------')
	# Only perform this if you need original Onset File for some reason, you shouldn't really
	"""
	df3 = pd.read_csv(temporarySmallPath + subNum + '-temporary-03.tsv', sep='\t')
	df4 = df3.ix[60:89]
	df4 = df4.reset_index(drop=True)
	df5 = pd.concat([df1, df3], axis=1)
	# Put into pandas data frame
	df5 = pd.DataFrame(df5)
	# Write the datafram into tsv format
	df5.to_csv(niftiPath + '/sub-' + subNum + '/func/sub-' + subNum + '_task-ER_run-03_events.tsv', sep='\t', index=None)
	"""

# Make it a function so that we can put it subject number...
temporaryBigPath = '/study3/midus3/processed_data/Temporary/Big'
tsvPath = sorted(glob.glob('%s/*-ER_events.tsv'%(temporaryBigPath)))
temporarySmallPath = '/study3/midus3/processed_data/Temporary/Small/'
smallPath = sorted(glob.glob(temporarySmallPath + '*.tsv'))
niftiPath = '/study3/midus3/processed_data/MIDUS3_Imaging/'

# Define column header names & # Create reader and writer variables
# reader.next() # skip header


fields = ['onset',
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

for tsv in tsvPath:
    subNum = tsv.split('-')
    subNum = subNum[1]
    subNum = subNum[0:3]

    ### Checking for the third Onset file ###
    # Do Nothing when the third Onset file exists
    if os.path.isfile(niftiPath + '/sub-%s/func/sub-%s_task-emotion-regulation_run-03_events.tsv'%(subNum, subNum)) == True:
        print ('----------Onsets by run for ' + subNum + ' exist already---------')

    # Only Convert when the third Onset file does *NOT* exist
    elif os.path.isfile(niftiPath + '/sub-%s/func/sub-%s_task-emotion-regulation_run-03_events.tsv'%(subNum, subNum)) == False:

        ### Creating Onset for block 1 ###

        # Compute various computations and write a .tsv
        with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_IAPS-01.tsv', 'w', newline="") as newTsv:
            calc_write_values_IAPS(newTsv, tsvFile, 1)

        with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_faces-01.tsv', 'w', newline="") as newTsv:
            calc_write_values_faces(newTsv, tsvFile, 1)

        block_one_data_manipulation(temporarySmallPath, subNum, niftiPath)
        #with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + subNum + '-temporary-01.tsv', 'wb') as newTsv:
            #reader_and_writer(newTsv, tsvFile)

        ### Creating Onset for block 2 ###

        with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_IAPS-02.tsv', 'w', newline="") as newTsv:
            calc_write_values_IAPS(newTsv, tsvFile, 2)

        with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_faces-02.tsv', 'w', newline="") as newTsv:
            calc_write_values_faces(newTsv, tsvFile, 2)

        block_two_data_manipulation(temporarySmallPath, subNum, niftiPath)
        #with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + subNum + '-temporary-02.tsv', 'wb') as newTsv:
            #reader_and_writer(newTsv, tsvFile)

        ### Creating Onset for block 3 ###

        with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_IAPS-03.tsv', 'w', newline="") as newTsv:
            calc_write_values_IAPS(newTsv, tsvFile, 3)

        with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_faces-03.tsv', 'w', newline="") as newTsv:
            calc_write_values_faces(newTsv, tsvFile, 3)

        block_three_data_manipulation(temporarySmallPath, subNum, niftiPath)
        #with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + subNum + '-temporary-03.tsv', 'wb') as newTsv:
            #reader_and_writer(newTsv, tsvFile)

        print ('----------Onset Data Manipulation for', subNum, 'Complete----------')
"""
print '----------Deleting temporary and computed files----------'
for small in smallPath:
	os.remove(small)
"""
"""
Useful Examples

# pandas reddit page for columns
# https://www.reddit.com/r/learnpython/comments/44p1bi/how_do_you_remove_a_column_of_a_csv_file/


singleOnsetFile = set([int(tsvs.split('/')[5][4:7]) for tsvs in tsvPath])
print singleOnsetFile

path = glob.glob("/study3/midus3/processed_data/MIDUS3_Imaging/sub-[0-9][0-9][0-9]/func/*run-01_events.tsv")
multipleOnsetFiles = set([int(onset.split('/')[5][4:7]) for onset in path])
print multipleOnsetFiles


for onsets in singleOnsetFile:

	if onsets in multipleOnsetFiles:
		print "Onsets exist already"

	if onsets not in multipleOnsetFiles:


fruit_wanted = ['fruit'] + ["'%s'" % f for f in fruit_wanted.split(',')]
niftiPath = csv.DictWriter(open(outputfile, 'wb'), fieldnames=fruit_wanted)
fruit_wanted = set(fruit_wanted)

for row in csv.DictReader(open(inputfile, 'rb')):
	row = {k: row[k] for k in row if k in fruit_wanted}
	 	niftiPath.writerow(row)
 """

