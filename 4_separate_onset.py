#!/bin/python

# First Compiled: 8/30/17
# Last Updated: 10/14/2017
# Updated Content: (10/13/2017) Changed run-1 ----> run-01
# Updated Content: (10/14/2017) Created several functions to make the code more readable and efficient
# Purpose: Separate Onset File into three by-block

# Things to change when runing on different data set
	# 1. all paths
	# 2. all splits

import glob
import csv
import os
import pandas as pd

# Define column header names 
def calc_write_values(newTsv,tsvFile, taskNum):
	rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
	rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names

	# Write column headers manually
	rowWriter.writeheader()

	# Compute the values (onset, duration, response time etc.)
	for rows in rowReader:
		blockNum = rows['Blocks']
		# Cast float to maintain the decimal points
		IAPSOnsetTime = float(rows['IAPSPicture.OnsetTime'])
		IAPSOffsetTime = float(rows['IAPSPicture.OffsetTime'])
		IAPSDuration = float((IAPSOffsetTime - IAPSOnsetTime)/1000)

		faceOnsettime = float(rows['Face.OnsetTime']) #CG
		faceOffsetTime = float(rows['Face.OffsetTime'])
		faceResponsetime = float(rows['Face.RTTime']) #CB
		faceDuration = float((faceOffsetTime - faceOnsettime)/1000)
		responseTime = float((faceResponsetime - faceOnsettime)/1000)
		
		taskNum = str(taskNum)
		if taskNum in blockNum:
			rowWriter.writerow({'onset_iaps_trimmed': ((IAPSOnsetTime-8000)/1000),
			'Duration_IAPS':IAPSDuration,
			'onset_face_trimmed': ((faceOnsettime-8000)/1000),
			'Duration_Face': faceDuration,
			'Response_Time_Face': responseTime,
			'Blocks':rows['Blocks']})

#lineterminator is paramter in csv.writer. it is default set to '\r\n' causing double spacing
def reader_and_writer(newTsv, tsvFile):
	writer = csv.writer(newTsv, delimiter='\t', lineterminator='\n') 
	reader = csv.reader(tsvFile, delimiter='\t')

	for row in reader:
		writer.writerow(row)

def block_one_data_manipulation(temporarySmallPath, subNum, outfile):
	df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_computed-01.tsv', sep='\t')
	# Use loc and isnull to replace negative responset times to 'NaN'
	df1.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = 'NaN'
	# Remove unnecessary blocks column
	del df1['Blocks']
	df2 = pd.read_csv(temporarySmallPath + subNum + '-temporary-01.tsv', sep='\t',) # usecols = ['columnname'] could be useful here
	# cut the index
	df3 = df2.ix[:29]
	# Put two csvs together
	df4 = pd.concat([df1, df3], axis=1)
	# Put the combined csvs into pandas data frame
	df4 = pd.DataFrame(df4)
	# Write the datafram into tsv format
	df4.to_csv(outfile + '/sub-' + subNum + '/func/sub-' + subNum + '_task-ER_run-01_events.tsv', sep='\t', index=None) # index = None --> removes first column of the index which are created by to_csv Pandas dataframe

	print '----------Onset file(s) for ' + subNum + '-01 created----------'

def block_two_data_manipulation(temporarySmallPath, subNum, outfile):
	df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_computed-02.tsv', sep='\t')
	# Use loc and isnull to replace negative responset times to 'NaN'
	df1.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = 'NaN'
	# Remove unnecessary blocks column
	del df1['Blocks']
	df2 = pd.read_csv(temporarySmallPath + subNum + '-temporary-02.tsv', sep='\t')
	#df3 = df2.drop(df2.index[[0,1,2,3,4]])
	#df4 = df3.drop(df3[:-3])
	#df2 = df2[df2.Blocks != 1]
	df3 = df2.ix[30:59]
	df3 = df3.reset_index(drop=True)
	#df5 = pd.merge(df1, df3, left_index=True, right_index=True)
	df5 = pd.concat([df1, df3], axis=1)
	# Put into pandas data frame
	df5 = pd.DataFrame(df5)
	# Write the datafram into tsv format
	df5.to_csv(outfile + '/sub-' + subNum + '/func/sub-' +  subNum + '_task-ER_run-02_events.tsv', sep='\t', index=None)

	print '----------Onset file(s) for ' + subNum + '-02 created----------'

def block_three_data_manipulation(temporarySmallPath, subNum, outfile):
	df1 = pd.read_csv(temporarySmallPath + 'sub-' + subNum + '_computed-03.tsv', sep='\t')
	# Use loc and isnull to replace negative responset times to 'NaN'
	df1.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = 'NaN'
	# Remove unnecessary blocks column
	del df1['Blocks']
	df2 = pd.read_csv(temporarySmallPath + subNum + '-temporary-03.tsv', sep='\t')
	df3 = df2.ix[60:89]
	df3 = df3.reset_index(drop=True)
	df5 = pd.concat([df1, df3], axis=1)
	# Put into pandas data frame
	df5 = pd.DataFrame(df5)
	# Write the datafram into tsv format
	df5.to_csv(outfile + '/sub-' + subNum + '/func/sub-' + subNum + '_task-ER_run-03_events.tsv', sep='\t', index=None)

	print '----------Onset file(s) for ' + subNum + '-03 created----------'

# Make it a function so that we can put it subject number...
masterPath = '/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Big'
tsvPath = glob.glob('%s/*-ER_events.tsv'%(masterPath))
temporarySmallPath = '/study3/midus3/processed_data/MIDUS3_Imaging/Temporary/Small/'
smallPath = glob.glob(temporarySmallPath + '*.tsv')
outfile = '/study3/midus3/processed_data/MIDUS3_Imaging/'

# Define column header names & # Create reader and writer variables
# reader.next() # skip header
fields = ('onset_iaps_trimmed',
	'Duration_IAPS',
	'onset_face_trimmed',
	'Duration_Face',
	'Response_Time_Face',
	'Blocks')

for tsv in tsvPath:
	subNum = tsv.split('-')
	subNum = subNum[1]
	subNum = subNum[0:3]

	### Checking for the third Onset file ###
	# Do Nothing when the third Onset file exists
	if os.path.isfile(outfile + '/sub-%s/func/sub-%s_task-ER_run-03_events.tsv'%(subNum, subNum)) == True:
		print 'Onsets by run for ' + subNum + ' exist already...'

	# Only Convert when the third Onset file does *NOT* exist
	elif os.path.isfile(outfile + '/sub-%s/func/sub-%s_task-ER_run-03_events.tsv'%(subNum, subNum)) == False:

		### Creating Onset for block 1 ###

		# Compute various computations and write a .tsv
		with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_computed-01.tsv', 'wb') as newTsv:
			calc_write_values(newTsv, tsvFile, 1)

		with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + subNum + '-temporary-01.tsv', 'wb') as newTsv:
			reader_and_writer(newTsv, tsvFile)
		block_one_data_manipulation(temporarySmallPath, subNum, outfile)

		### Creating Onset for block 2 ###

		with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_computed-02.tsv', 'wb') as newTsv:
			calc_write_values(newTsv, tsvFile, 2)

		with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + subNum + '-temporary-02.tsv', 'wb') as newTsv:
			reader_and_writer(newTsv, tsvFile)
		block_two_data_manipulation(temporarySmallPath, subNum, outfile)

		### Creating Onset for block 3 ###

		with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + 'sub-' + subNum + '_computed-03.tsv', 'wb') as newTsv:
			calc_write_values(newTsv, tsvFile, 3)

		with open(tsv, 'rU') as tsvFile, open(temporarySmallPath + subNum + '-temporary-03.tsv', 'wb') as newTsv:
			reader_and_writer(newTsv, tsvFile)
		block_three_data_manipulation(temporarySmallPath, subNum, outfile)


print '----------Deleting temporary and computed files----------'
for small in smallPath:
	os.remove(small)

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
outfile = csv.DictWriter(open(outputfile, 'wb'), fieldnames=fruit_wanted)
fruit_wanted = set(fruit_wanted)

for row in csv.DictReader(open(inputfile, 'rb')):
	row = {k: row[k] for k in row if k in fruit_wanted}
	 	outfile.writerow(row)
 """

