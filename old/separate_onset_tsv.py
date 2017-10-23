#!/bin/python
import glob
import csv
#import sys
#oneTsv = "/study/midus3/test/sub-001/func/sub-001_task-ER_events.tsv"
#f = open('/home/slee/Desktop/output.tsv', 'w')
#sys.stdout = f

masterPath = "/study/midus3/test/"
tsvPath = glob.glob("%s/sub-[0-9][0-9][0-9]/func/*.tsv"%(masterPath))

for tsv in tsvPath:
	subNum = tsv.split('-')
	subNum = subNum[2]
	subNum = subNum[0:3]
# Read infile & outfile, and manually write column header information 
	with open(tsv, 'rb') as tsvFile, open('/home/slee/Desktop/Test/sub-' + subNum + '_task-ER_run-01_events.tsv', 'wb') as newTsv:
		
		writer = csv.writer(newTsv, delimiter='\t')
		reader = csv.reader(tsvFile, delimiter='\t')
		#reader.next() # skip header

		for row in reader:
			row[0] = ""
			row[1] = ""
			row[2] = ""
			row[3] = ""
			writer.writerow(row)

		print "1st Step Complete for " + subNum

	with open(tsv, 'rb') as tsvFile, open('/home/slee/Desktop/Test/sub-' + subNum + '_task-ER_run-01_events.tsv', 'wb') as newTsv:

		fields = ('Onset', 
		'Duration',
		'Response_Time',
		'Blocks')
		#'IAPSPicture.StartTime',
		#'IAPSPicture.OffsetTime',
		#'valencecategory', 
		#'FullPicturePath', 
		#'FullFacePath') # This part will print headers
		
		rowWriter = csv.DictWriter(newTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') # \t skips column!
		rowReader = csv.DictReader(tsvFile, delimiter='\t') # Dict Reader uses the header column names
		
		rowWriter.writeheader() # Write headers manually

		for rows in rowReader:
			#print "working"
			blockNum = rows['Blocks']
			#blockNum = int(blockNum)
			onsetTime = float(rows['IAPSPicture.OnsetTime'])
			#startTime = float(row['IAPSPicture.StartTime'])
			offsetTime = float(rows['IAPSPicture.OffsetTime'])
			duration = float((offsetTime - onsetTime)/1000)
			#if duration < 0:
				#print "no button box!!"
			
			faceOnsettime = float(rows['Face.OnsetTime']) #CG
			faceRTtime = float(rows['Face.RTTime']) #CB
			responseTime = float((faceRTtime - faceOnsettime)/1000)

			if "1" in blockNum:
				#print "working"
				rowWriter.writerow({'Onset': onsetTime/1000,
					'Duration':duration, 
					'Response_Time': responseTime,
					'Blocks':rows['Blocks']})

					#'IAPSPicture.StartTime':row['IAPSPicture.StartTime'], 
					#'IAPSPicture.OffsetTime': row['IAPSPicture.OffsetTime'],
					#'valencecategory':row['valencecategory'], 
					#'FullPicturePath':row['FullPicturePath'],
					#'FullFacePath':row['FullFacePath']})
			
print "----------Onset file(s) for " + subNum + " created----------"

"""
	with open(tsv, 'rb') as tsvFile, open ('/home/slee/Desktop/Test/sub-' + subNum + '_task-ER_run-02_events.tsv', 'wb') as secondTsv:
		fields = ('Blocks', 'IAPSPicture.OnsetTime', 'IAPSPicture.StartTime','IAPSPicture.OffsetTime',
		'valencecategory', 'FullPicturePath', 'FullFacePath')
		reader = csv.DictReader(tsvFile, delimiter='\t')
		writer = csv.DictWriter(secondTsv, fieldnames=fields, delimiter='\t', lineterminator='\n') 
		writer.writeheader()

		for row in reader:
			blockNum = row['Blocks']
			startTime = float(row['IAPSPicture.StartTime'])
			offsetTime = float(row['IAPSPicture.OffsetTime'])
			duration = float((offsetTime - startTime)/1000)
			if "2" in blockNum:
				writer.writerow({'Blocks':row['Blocks'], 'IAPSPicture.OnsetTime': row['IAPSPicture.OnsetTime'], 
					'IAPSPicture.StartTime':row['IAPSPicture.StartTime'], 'IAPSPicture.OffsetTime': row['IAPSPicture.OffsetTime'],
					'valencecategory':row['valencecategory'], 'FullPicturePath':row['FullPicturePath'],
					'FullFacePath':row['FullFacePath']})

	with open(tsv, 'rb') as tsvFile, open ('/home/slee/Desktop/Test/sub-' + subNum + '_task-ER_run-03_events.tsv', 'wb') as secondTsv:
		fields = ('Blocks', 'IAPSPicture.OnsetTime', 'IAPSPicture.StartTime','IAPSPicture.OffsetTime',
		'valencecategory', 'FullPicturePath', 'FullFacePath')
		reader = csv.DictReader(tsvFile, delimiter='\t')
		writer = csv.DictWriter(secondTsv, fieldnames=fields, delimiter='\t', lineterminator='\n')
		writer.writeheader()

		for row in reader:
			blockNum = row['Blocks']
			startTime = float(row['IAPSPicture.StartTime'])
			offsetTime = float(row['IAPSPicture.OffsetTime'])
			duration = float((offsetTime - startTime)/1000)
			if "3" in blockNum:
				writer.writerow({'Blocks':row['Blocks'], 'IAPSPicture.OnsetTime': row['IAPSPicture.OnsetTime'], 
					'IAPSPicture.StartTime':row['IAPSPicture.StartTime'], 'IAPSPicture.OffsetTime': row['IAPSPicture.OffsetTime'],
					'valencecategory':row['valencecategory'], 'FullPicturePath':row['FullPicturePath'],
					'FullFacePath':row['FullFacePath']})
"""
		# Things to Fix	
		# (Fiexd But...) more efficient loop is needed) Break and create newfile each time it hits 30 (why can't I figure out the loop?)
		# (Fixed) All timing values should be in SECONDS, so devide all time values by 1000
		# 3. Change column names to "onset", 'duration', 'response_time'
		# (Fixed) Make it loop through all our subjects
		# 5. Remove single .tsv onsetfile after all conversions
