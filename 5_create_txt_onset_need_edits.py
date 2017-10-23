#!/bin/python

# Author: David SB Lee
# First Compiled: 10/16/2017
# Last Updated: 10/20/2017
# Updated Content: (10/20/2017) Added Authorship
# Purpose: Create Three-column .txt onsets for FSL use

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

print(sys.argv)
subID = sys.argv[1]

def data_manipulation(blockNum, threeDigit):

	onset = "%s/sub-%s/func/sub-%s_task-ER_run-"%(path, subID, subID) + blockNum + "_events.tsv"
	output = "%s/sub-%s/model/%s_cond"%(path, subID, subID) + threeDigit + ".txt"
	
	with open (output, 'wb') as newOnset:
		df1 = pd.read_csv(onset, sep='\t')
		# Print Onset_Face, Druation, and Group (1's)
		df2 = df1.iloc[:,[2,3,14]]
		df2.to_csv(output, sep='\t', index=None, header=False)
	
path = "/home/slee/Desktop" 

if os.path.isdir("%s/sub-%s/model"%(path, subID)) == False:
	os.makedirs("%s/sub-%s/model"%(path, subID))
	print "----------Creating MODEL Directory----------"

data_manipulation("01", "001")
data_manipulation("02", "002")
data_manipulation("03", "003")
