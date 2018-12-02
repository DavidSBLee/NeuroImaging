#!/bin/python3

# Author: David SB Lee
# First Compiled: 10/16/2017

# Things to change when runing on different data set
	# 1. all paths
	# 2. all splits
	# 3. parameters for the fucntion data_manipulation
	# 4. This takes an argument of subject Number "###"
	
import os
import glob
import os.path
import csv
import pandas as pd 
import sys
import math

# Set global variables (paths)
path = "/study3/midus3/processed_data/Temporary/Small"
niftiPath = "/study3/midus3/processed_data/MIDUS3_Imaging"
analysisPath = "/study3/midus3/processed_data/MIDUS3_Imaging_Analysis" 

# The script takes an argument 
(sys.argv)
subID = sys.argv[1]

def data_manipulation_No_Response(blockNum):
	onset = "%s/sub-%s_faces-%s.tsv"%(path, subID, blockNum)
	output = "%s/sub-%s/model/%s_No_Response_%s.txt"%(analysisPath, subID, subID, blockNum)

	with open (output, 'wb') as newOnset:
		df1 = pd.read_csv(onset, sep='\t')
		# Select Rows where Response Time is 0, meaning NO button box press
		df2 = df1.loc[df1['Response_Time_Face'] == 0]
		# Fetch Onset, Druation, and Group (1's)
		df3 = df2.iloc[:,[13,1,3]]
		df3.to_csv(output, sep='\t', index=None, header=False)

def data_manipulation_IAPS_by_Valence(blockNum, valence):
	#try:
	onset = "%s/sub-%s_IAPS-%s.tsv"%(path, subID, blockNum)
	output = "%s/sub-%s/model/%s_IAPS_%s_%s.txt"%(analysisPath, subID, subID, valence, blockNum)

	with open (output, 'wb') as newOnset:
		df1 = pd.read_csv(onset, sep='\t')
		# Selct Rows whose Valence Column Values are postive
		df2 = df1.loc[df1['valence'] == valence]
		# Fetch Onset, Druation, and Group (1's)
		df3 = df2.iloc[:,[13,1,12]]
		df3.to_csv(output, sep='\t', index=None, header=False)
		#df2.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "n/a"
	#except IOError:
		#print("Error" + )
def data_manipulation_FACES_by_Valence(blockNum, valence):

	onset = "%s/sub-%s_faces-%s.tsv"%(path, subID, blockNum)
	output = "%s/sub-%s/model/%s_FACES_%s_%s.txt"%(analysisPath, subID, subID, valence, blockNum)

	with open (output, 'wb') as newOnset:
		df1 = pd.read_csv(onset, sep='\t')
		# Selct Rows whose Valence Column Values are what you input (i.e. pos)
		df2 = df1.loc[df1['valenceFollowing'] == valence]
		# Fetch Onset, Druation, and Group (1's)
		df3 = df2.iloc[:,[13,1,12]]
		df3.to_csv(output, sep='\t', index=None, header=False)
		#df2.loc[(df1['Response_Time_Face'] < 0 ) | (df1['Response_Time_Face'].isnull()), 'Response_Time_Face'] = "n/a"

def data_maipulation_RT_Adjustment(blockNum):
	onset = "%s/sub-%s_faces-%s.tsv"%(path, subID, blockNum)
	output = "%s/sub-%s/model/%s_RT_Adjusted_%s.txt"%(analysisPath, subID, subID, blockNum)

	with open (output, 'wb') as newOnset:
		df1 = pd.read_csv(onset, sep='\t')
		# Calculate mean RT for all 30 responses
		meanRT = df1["Response_Time_Face"].mean()
		# Limit float to rounded up 2 decimal points 
		meanRT_RoundedUp = round(meanRT, 2)
		print ("meanRT for",subID, blockNum + ":", meanRT_RoundedUp)
		# Compute RT - meanRt 
		adjustedRT = df1['Response_Time_Face'] - meanRT
		# Replace all rows with mean RT subtracted from RT
		df1.loc[(df1['Response_Time_Face'] > 0), 'Response_Time_Face'] = adjustedRT
		# Round up the adjustRT to three decimal points
		df1['Response_Time_Face'] = df1['Response_Time_Face'].round(3)
		# Fetch Onset, Druation, and Group (1's)
		df2 = df1.iloc[:,[13,1,3]]
		df2.to_csv(output, sep='\t', index=None, header=False)

def data_manipulation_RT_adjustment_by_Valence(blockNum, valence):
	onset = "%s/sub-%s_faces-%s.tsv"%(path, subID, blockNum)
	output = "%s/sub-%s/model/%s_RT_adjusted_%s_%s.txt"%(analysisPath, subID, subID, valence, blockNum)

	with open (output, 'wb') as newOnset:
		df1 = pd.read_csv(onset, sep='\t')
		# Calculate mean RT for all 30 responses
		meanRT = df1["Response_Time_Face"].mean()
		# Limit float to rounded up 2 decimal points 
		meanRT_RoundedUp = round(meanRT, 2)
		print ("meanRT for",subID, blockNum + ":", meanRT_RoundedUp)
		# Compute RT - meanRt 
		adjustedRT = df1['Response_Time_Face'] - meanRT
		# Replace all rows with mean RT subtracted from RT
		df1.loc[(df1['Response_Time_Face'] > 0), 'Response_Time_Face'] = adjustedRT
		# Round up the adjustRT to three decimal points
		df1['Response_Time_Face'] = df1['Response_Time_Face'].round(3)
		# Selct Rows whose Valence Column Values are what you input (i.e. pos)
		df1 = df1.loc[df1['valenceFollowing'] == valence]
		# Fetch Onset, Druation, and Group (1's)
		df2 = df1.iloc[:,[13,1,3]]
		df2.to_csv(output, sep='\t', index=None, header=False)
if __name__ == "__main__":
	# If model in anaylsis does NOT exist AND subject has func data...
	if os.path.isdir("%s/sub-%s/model"%(analysisPath, subID)) == True:
		print ("----------Model Directory Already Exists----------")

	elif os.path.isdir("%s/sub-%s/model"%(analysisPath, subID)) == False and os.path.isdir("%s/sub-%s/func"%(niftiPath, subID)) == True: 
		os.makedirs("%s/sub-%s/model"%(analysisPath, subID))
		print ("----------Creating MODEL Directory----------")

	if os.path.isfile("%s/sub-%s/model/%s_IAPS_pos_01.txt"%(analysisPath, subID, subID)) == False:
		try:
			data_manipulation_IAPS_by_Valence("01", "pos")
			print ("----------Creating Onset Files----------")
			data_manipulation_IAPS_by_Valence("02", "pos")
			data_manipulation_IAPS_by_Valence("03", "pos")

			data_manipulation_IAPS_by_Valence("01", "neg")
			data_manipulation_IAPS_by_Valence("02", "neg")
			data_manipulation_IAPS_by_Valence("03", "neg")

			data_manipulation_IAPS_by_Valence("01", "neu")
			data_manipulation_IAPS_by_Valence("02", "neu")
			data_manipulation_IAPS_by_Valence("03", "neu")

			data_manipulation_FACES_by_Valence("01", "pos")
			data_manipulation_FACES_by_Valence("02", "pos")
			data_manipulation_FACES_by_Valence("03", "pos")

			data_manipulation_FACES_by_Valence("01", "neg")
			data_manipulation_FACES_by_Valence("02", "neg")
			data_manipulation_FACES_by_Valence("03", "neg")

			data_manipulation_FACES_by_Valence("01", "neu")
			data_manipulation_FACES_by_Valence("02", "neu")
			data_manipulation_FACES_by_Valence("03", "neu")

			data_manipulation_RT_adjustment_by_Valence("01", "pos")
			data_manipulation_RT_adjustment_by_Valence("02", "pos")
			data_manipulation_RT_adjustment_by_Valence("03", "pos")

			data_manipulation_RT_adjustment_by_Valence("01", "neg")
			data_manipulation_RT_adjustment_by_Valence("02", "neg")
			data_manipulation_RT_adjustment_by_Valence("03", "neg")

			data_manipulation_RT_adjustment_by_Valence("01", "neu")
			data_manipulation_RT_adjustment_by_Valence("02", "neu")
			data_manipulation_RT_adjustment_by_Valence("03", "neu")

			data_maipulation_RT_Adjustment("01")
			data_maipulation_RT_Adjustment("02")
			data_maipulation_RT_Adjustment("03")

			data_manipulation_No_Response("01")
			data_manipulation_No_Response("02")
			data_manipulation_No_Response("03")
		except IOError:
			# Print which subject has error
			print("Error: " + subID + " does not have func data" )
	else:
			print ("----------Onset Files Already Exists----------")

