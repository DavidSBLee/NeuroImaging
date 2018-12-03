#!/usr/bin/env python3

import pandas as pd
import os
import sys
import re
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import glob

# Notes
# definately have to merge before applying any filters
# Q's
# How to correct for delay - no need I can just use RTTime (E-PRIME CLOCK)
# Why 6 timestamps, not 5? - don't use "timestamp", use "TETTime"
# Some missing AOIs 
# How to filter by validity? 
# Sampling rate varies by subject
# Re scale AOI to 800 x 600
# Intermediate files
# Filter out Blinks???
# CSV for each subject with total good trials, and good per each IAPS # AND stim in chronological order

subNum = sys.argv[1]

#--------------------Gaze Data--------------------
# Read in gaze data 
gaze_file = "/study/midusref/raw-data/EMG/eprime//MIDUSref_startle_order*_FINAL_VERSION-%s-%s.gazedata"%(subNum, subNum)
gaze_file = glob.glob(gaze_file)
gaze_file = gaze_file[0]
gaze = pd.read_csv(gaze_file, sep='\t')

#--------------------E-prime Data--------------------
# Convert Eprime file in to tsv
eprime_input = "/study/midusref/raw-data/EMG/eprime//MIDUSref_startle_order*_FINAL_VERSION-%s-%s.txt"%(subNum, subNum)
eprime_input = glob.glob(eprime_input)
eprime_input = eprime_input[0]

os.makedirs("/study/midusref/DATA/Eyetracking/david_analysis/data_processed/%s"%(subNum), exist_ok=True)
os.system("eprime2tabfile %s > /study/midusref/DATA/Eyetracking/david_analysis/data_processed/%s/MIDUSref_FINAL_VERSION-%s-%s.tsv"%(eprime_input, subNum, subNum, subNum))

# Read in Eprime data
e_prime = pd.read_csv("/study/midusref/DATA/Eyetracking/david_analysis/data_processed/%s/MIDUSref_FINAL_VERSION-%s-%s.tsv"%(subNum, subNum, subNum), sep='\t')

#--------------------Gaze and E-prime Data Merged--------------------
data_merged = pd.merge(gaze, e_prime, on='image')

#--------------------Denoising1:Applies Universally--------------------

##### Remove first 6 practice picture trials (subset df that is not practice trials)
data_merged = data_merged[(data_merged['Running']) != 'pracList']

##### Remove trials that are considered "pause"
data_merged = data_merged[(data_merged['Procedure']) != 'pause']

##### Potentially, blink filtering needs to happen here

##### Remove trials from fixation period (~1000ms)
# Create a new column "TimestampMilliseconds" using "TETTIME" (E-prime Clock in Microseconds)
data_merged['TimestampMilliseconds'] = data_merged['TETTime']

# Round to nearest whole number
#data_merged['TimestampMillisecondsRounded'] = data_merged['TimestampMilliseconds'].round()

# Group by IAPS image number and rank by time in milieseconds
data_merged['rank'] = data_merged.groupby('image')['TimestampMilliseconds'].rank(ascending=True, method='dense')
data_merged['rank'] = data_merged['rank'].astype(int)

# Extract start times based on rank 1 of all IAPS images
startTime = data_merged.loc[data_merged['rank'] == 1]
startTime = startTime['TimestampMilliseconds']
startTimeList = startTime.tolist()

# Remove first 1000ms of each trial
for time in startTimeList:
	fixationCrossTime = time + 1
	data_merged = data_merged.drop(data_merged[(data_merged.TimestampMilliseconds > time) & (data_merged.TimestampMilliseconds <= fixationCrossTime)].index)

# Total trials before Denoising #2
pre_denoise_gaze_count = len(data_merged.index)
print ("preDenoise_trials: " + str(pre_denoise_gaze_count))

# Total stim count before Denoising #2
preDenoise_imageList = data_merged['image'].unique()
preDenoise_stim_count = str(len(preDenoise_imageList))
print ("preDnoise_stim_count: " + preDenoise_stim_count)

#--------------------Denoising2:Applies Differently by Subject--------------------
##### Filter data by validity
# Keep only trials with AT LEAST one good (valid) eye gaze 
# Use anything from 0 , 1 , or 2 in at least one eye
data_merged = data_merged[(data_merged['ValidityLeftEye'] <= 2) | (data_merged['ValidityRightEye'] <= 2)] 
# For some reason, keep including "4" so manually drop trila that have 4 in BOTH left and right eye
data_merged = data_merged.drop(data_merged[(data_merged.ValidityLeftEye == 4) & (data_merged.ValidityRightEye ==4)].index) 

# Remove trials with invalid distance data 
# We might not have to do this depdning on whether we use this in later computations
data_merged = data_merged.drop(data_merged[(data_merged.DistanceLeftEye == -1)].index)
data_merged = data_merged.drop(data_merged[(data_merged.DistanceRightEye == -1)].index)

# Total trials after Denoising #2
post_denoise_gaze_count = len(data_merged.index)
print ("postDenoise_trials: " + str(post_denoise_gaze_count))

# Total stim count after Denoising #2
postDenoise_imageList = data_merged['image'].unique()
postDenoise_stim_count = str(len(postDenoise_imageList))
print ("postDnoise_stim_count: " + postDenoise_stim_count)


# Figure out which Stim has been removed due to Denoising #2
missingIAPSList = list(set(preDenoise_imageList) - set(postDenoise_imageList))
print (missingIAPSList)

# Compare missingIAPSList to the Original, figure out which nth element is missing
missing_stim_number_list = [] 
for index, stim in enumerate(preDenoise_imageList):
	for missingIAPS in missingIAPSList:
		if missingIAPS == stim:
			stim_number = "stim_" + str(index + 1)
			missing_stim_number_list.append(stim_number)
print (missing_stim_number_list)

# Total valid data after Denoising #2
percent_good_data_subject = round((post_denoise_gaze_count/pre_denoise_gaze_count) * 100, 2)
print ("percent good data subject: %s percent"%(percent_good_data_subject))

# Check for any lingering invalid data
#print (data_merged.groupby('image').ValidityRightEye.nunique())
#print (data_merged['ValidityRightEye'].unique())

##### Interpolate missing data by IAPS image
# Watch out for missing IAPS due to denoising in the previous step
stim_counter = 0

IAPSList = [] + missingIAPSList
StimList = [] + missing_stim_number_list
GoodPercentList = [0] * len(missing_stim_number_list)

#print (IAPSList)
for image in postDenoise_imageList:
	stim_counter += 1 
	stim_name = "stim_" + str(stim_counter)

	if stim_name in StimList:
		stim_counter += 1
		stim_name = "stim_" + str(stim_counter)

	single_image_df = data_merged.loc[data_merged['image'] == image]
	firstIndex = (min(single_image_df.index))
	finalIndex = (max(single_image_df.index))
	indexList = range(firstIndex, finalIndex-1)

	# Number of good raw trials (before interpolation)
	raw_trials = len(single_image_df)

	# Figure out missing values due to previous denoising and fill in with "NaN"
	single_image_df = single_image_df.reindex(indexList, fill_value=np.nan)

	# Re-set the index from 1 
	single_image_df = single_image_df.reset_index(drop=True)

	# Compute sampling rate for each trial
	single_image_df['sampling_rate'] = single_image_df['TimestampMilliseconds'].diff()
	#single_image_df.to_csv("/home/slee/Desktop/sample.csv")
	average_sampling_rate = single_image_df['sampling_rate'].mean()
	print ("average sampling rate for %s : %s"%(image, str(average_sampling_rate)))

	# Create a column for # data points
	single_image_df['trial_number'] = list(range(0, len(indexList)))

	# Number of total trials (after interpolation)
	with_interpolated_trials = len(single_image_df)

	single_image_df.to_csv("/study/midusref/DATA/Eyetracking/david_analysis/data_processed/{}/{}.csv".format(subNum, image))

	# Create Plotsplt.suptitle('subject%s %s'%(subNum, image))
	fig = plt.figure()
	plt.plot(single_image_df['CursorX'], 'b')
	plt.plot(single_image_df['CursorY'], 'g')
	fig.suptitle('subject%s %s'%(subNum, image))
	plt.ylabel("Coordinates")
	plt.xlabel("Trials")
	plt.legend(['X', 'Y'])
	#plt.show()
	fig.savefig('/study/midusref/DATA/Eyetracking/david_analysis/data_processed/{}/{}_{}.png'.format(subNum, subNum, image))
	# Create Plots
	
	# Percent raw data for single IAPS
	try:
		percent_good_data_IAPS = round((raw_trials/with_interpolated_trials) * 100, 2)
	#print ("percent good data %s: %s percent"%(image, percent_good_data_IAPS))
	#print ("percent good data %s: %s percent"%(stim_name, percent_good_data_IAPS))
	except ZeroDivisionError:
		percent_good_data_IAPS = 0

	IAPSList.append(image)
	StimList.append(stim_name)
	GoodPercentList.append(percent_good_data_IAPS)

	# Make a column to indicate interpolated or not (Before actual interpolation)
	single_image_df['data_type'] = single_image_df['TimestampMilliseconds']
	single_image_df['data_type'].fillna("interpolated", inplace=True)
	try:
		single_image_df.loc[single_image_df['data_type'] != "interpolated", 'data_type'] = "raw"
	except TypeError:
		continue

	# Interpolate missing timestamp and gaze point and distance
	single_image_df['TimestampMilliseconds'] = single_image_df['TimestampMilliseconds'].interpolate("linear")
	single_image_df['CursorX'] = single_image_df['CursorX'].interpolate("linear")
	single_image_df['CursorY'] = single_image_df['CursorY'].interpolate("linear")
	single_image_df['DistanceRightEye'] = single_image_df['DistanceRightEye'].interpolate("linear")
	single_image_df['DistanceLeftEye'] = single_image_df['DistanceLeftEye'].interpolate("linear")

	# Create numpy array to feed compute_saccade()
	coordinate_df = single_image_df[['CursorX', 'CursorY']]
	

	#arr = coordinate_df['CursorX', 'CursorY'].values
	#print (arr)

# Create Intermediate QA files
good_data_IAPS_number_df = pd.DataFrame({subNum:GoodPercentList}) # "Stim":StimList, {"IAPS":IAPSList}
good_data_IAPS_number_df_transposed = good_data_IAPS_number_df.T
good_data_IAPS_number_df_transposed.columns = IAPSList
good_data_IAPS_number_df_transposed.insert(loc=0, column='TotalValid', value=[percent_good_data_subject])
#print (good_data_IAPS_number_df_transposed)
good_data_IAPS_number_df_transposed.to_csv("/study/midusref/DATA/Eyetracking/david_analysis/data_processed/%s/%s_valid_IAPS.csv"%(subNum, subNum))

good_data_STIM_number_df = pd.DataFrame({subNum:GoodPercentList}) # "Stim":StimList, {"IAPS":IAPSList}
good_data_STIM_number_df_transposed = good_data_STIM_number_df.T
good_data_STIM_number_df_transposed.columns = StimList
good_data_STIM_number_df_transposed.insert(loc=0, column='TotalValid', value=[percent_good_data_subject])
#print (good_data_STIM_number_df_transposed)
good_data_STIM_number_df_transposed.to_csv("/study/midusref/DATA/Eyetracking/david_analysis/data_processed/%s/%s_valid_STIM.csv"%(subNum, subNum))

print ("processing for %s complete without error"%(subNum))
#single_image_df.to_csv("/home/slee/Desktop/eye_sample.csv")
#print (single_image_df)

"""
#--------------------Feature Engineering for angular velocity--------------------
# pixel size in mm
pixel = 0.264583333333

# Compute velocity (distance/time) for X and Y
single_image_df['X_movement'] = abs(single_image_df['CursorX'].diff())
single_image_df['X_movement_mm'] = single_image_df['X_movement'] * pixel
single_image_df['velocity_X'] = single_image_df['X_movement_mm'] / single_image_df['TimestampMilliseconds']

single_image_df['Y_movement'] = abs(single_image_df['CursorY'].diff())
single_image_df['Y_movement_mm'] = single_image_df['Y_movement'] * pixel
single_image_df['velocity_Y'] = single_image_df['Y_movement_mm'] / single_image_df['TimestampMilliseconds']

# Interpolate missing data)
#single_image_df['velocity_X'] = single_image_df['velocity_X'].interpolate("linear")
#ssingle_image_df['velocity_Y'] = single_image_df['velocity_Y'].interpolate("linear")

# Compute sampling rate for each trial
single_image_df['Time_diff'] = abs(single_image_df['TimestampMilliseconds'].diff())

# Compute gaze angle (just Right Eye for now)
single_image_df['RightEye_distance_B'] = single_image_df['DistanceRightEye']
single_image_df['RightEye_distance_C'] = single_image_df['DistanceRightEye']

# shift 
single_image_df.RightEye_distance_B = single_image_df.RightEye_distance_B.shift(+1)

# Missing distance from the eye to the monitor (only to the camera)
X_GazeAngle_list = []
for index, row in single_image_df.iterrows():
	a = row['X_movement']
	b = row['RightEye_distance_B']
	c = row['RightEye_distance_C']
	numerator = b**2 + c**2 - a**2
	denominator = 2 * b * c
	value = numerator/denominator
	#print (value)

	if value < 1.0:
		gaze_angle = math.acos(value)
		#print (gaze_angle)
		X_GazeAngle_list.append(gaze_angle)

print (len(X_GazeAngle_list))

single_image_df['RightEye_X_GazeAngle'] = X_GazeAngle_list
single_image_df.to_csv("/home/slee/Desktop/eye_sample.csv")
"""

"""
#--------------------AOI--------------------
imageList = data_merged['image'].unique()
IAPSlist = []
coordinateList = []
objectNumList = []
noAOIlist = []

for image in imageList:
	filePath = "/study/reference/public/IAPS/IAPS/IAPS_2008_1-20_800x600BMP/IAPS_2008_AOIs/%s.OBT"%(image)


	#parser = re.compile(r"[^=]+=(\d+), (\d+), (\d+), (\d+), (\d+)")

	#IAPSnumb = filePath[-8:-4]
	try:
		with open(filePath, 'rU') as f:
			for line in f:
				a = line.split('=')
				if len(a) > 1 and a[1] != "0\n":
					objectNum = a[0]
					objectCoordinate = a[1][:-10]
	
					IAPSlist.append(image)
					coordinateList.append(objectCoordinate)
					objectNumList.append(objectNum)

		df1 = pd.DataFrame(IAPSlist, columns=['image'])
		df2 = pd.DataFrame(coordinateList, columns=['coordinate'])
		df3 = pd.DataFrame(objectNumList, columns=['objectNumber'])
		df4 = pd.concat([df1, df2], axis=1)
		df5 = pd.concat([df4, df3], axis=1)

	except OSError as e:
		print ("no AOI for %s"%(image))
		noAOIlist.append(image)

# Drop coordinates that indicate grid (object01)
df5 = df5[df5.objectNumber.str.contains("Object01") == False].reset_index()


# Fetch AOI type information and recode 
df5['AOItype'] = df5.coordinate.str[:1]
df5['AOItype'] = df5['AOItype'].replace(['1'], 'Rectangle')
df5['AOItype'] = df5['AOItype'].replace(['2'], 'Ellipse')

# Refine coordinates
# Iterate throw rows in coordinate column and split by , and get everyhitng but 0 index!
#df5['coordinate'] = df5.coordinate.str[3:]
newCoordinateList = []
for index, row in df5.iterrows():
	a = (row['coordinate']).split(",")
	newCoordinate = a[1:]
	#df5.loc[index,'coordinate'] = newCoordinate
	newCoordinateList.append(newCoordinate)

df6 = pd.DataFrame(newCoordinateList, columns=['Xmin','Ymax','Xmax','Ymin'])
#df5["newCoordinate"] = pd.Series(newCoordinateList, index=df5.index)


# merge new coordinate information with AOI dataframe
df7 = pd.concat([df5, df6], axis=1)
#print (df7)
#print (list(df7))
"""








 






"""
data_merged_again= pd.merge(data_merged, df3, how='left', on='image')

#print (df3)
#a = df3['image'].tolist()
#import collections
#print ([item for item, count in collections.Counter(a).items() if count > 1])

#print (df3)



### Correct for eyetracker delay provided by difference between variables "TETTIME" and "GazeDataRTTime" and other timing issue, only use GOOD eyetracing data
# Create a new column "eyetrackerDelay" 
data_merged['eyetrackerDelay'] = data_merged['TETTime'] - data_merged['GazeDataRTTime']
#print (gaze['eyetrackerDelay'])

# How do I correct for eyetracker delay??? I think I want to subtract these millesecond delay values from timestampMilliseconds...???
data_merged['correctedTimestamp'] = data_merged['TimestampMilliseconds'] - data_merged['eyetrackerDelay']
#print (gaze['correctedTimestamp'])

# Subset dataframe with either right & left valid data
df2 = df1[(df1['ValidityLeftEye']==0) | (df1['ValidityRightEye']==0)] 

print (df2)
# Subset dataframe with both right & left, take average


e_prime = e_prime[e_prime.pracList != 1]
e_prime = e_prime[e_prime.pracList != 2]
e_prime = e_prime[e_prime.pracList != 3]
e_prime = e_prime[e_prime.pracList != 4]
e_prime = e_prime[e_prime.pracList != 5]
df1 = e_prime[e_prime.pracLißst != 6]

#or
df1 = e_prime[(e_prime['pracList'] >= 1) & (e_prime['pracList'] <= 6)]


### How to rank, groupby, and remove certain ranks
data_merged['rank'] = data_merged.groupby('image')['Timestamp'].rank(ascending=True, method='dense')
data_merged['rank'] = data_merged['rank'].astype(int)

# Create a new dataframe and a new column of how many unique ranks are there for each IAPS image
counts_gaze = data_merged.groupby('image')['rank'].nunique().reset_index()

# Rename the new column 
counts_gaze.rename(columns=dict(rank='rank_counts'), inplace=True)

print (counts_gaze)
# Remove any IAPS pictures with ranks other than 6
counts_gaze = counts_gaze[counts_gaze['rank_counts'] == 6]

print (counts_gaze)
# Merge the dataframe with the original by IAPS number
data_merged = pd.merge(data_merged, counts_gaze, how='inner', on='image')

#print(gaze.groupby('image').agg({'rank':'max'}))

# Extract rows that have max (6) ranks
max_vals_gaze = data_merged.groupby('image')['rank'].max().reset_index()

# Rename the rank column
max_vals_gaze.rename(columns=dict(rank='rank_max'), inplace=True)


# Merge the dataframe with original IAPS number
data_merged = pd.merge(data_merged, max_vals_gaze, how='left', on='image')

# Remove ranks 1 aka.first 1 second (Fixation) period of the paradigm
data_merged = data_merged[(data_merged['rank'] != 1)]

# Check column names
#print (list(gaze))


### Might be useuful for interpolation later on resetting index
numb_columns = len(data_merged.columns)
data_merged.loc[0,'RightEye_distance_C'] = 0 


vector_b = data_merged['RightEye_distance_B']
#vector_b.rename("RightEye_distance_B")
firstIndex = (min(vector_b.index))
vector_b.loc[firstIndex-1] = 0
vector_b.sort_index(inplace=True)
#vector_b.index = vector_b.index + 1

data_merged = pd.concat([data_merged, vector_b], axis=1)

#single_image = single_image.dropna()
#single_image = single_image.astype(float)
#for col in single_image:
	#single_image[col] = pd.to_numeric(single_image[col], errors='coerce')


#print (single_image.dtypes)
#single_image['TimestampMilliseconds'].fillna(method='ffill')
#single_image_time = pd.Series(single_image['TimestampMilliseconds'])
#single_image_time.fillna(0, inplace=True)
#single_image_time = single_image_time.astype(float)
#single_image_time = single_image_time.interpolate("linear")

#.interpolate(method='index')
#single_image.sort_index(inplace=True)
#single_image = single_image.reset_index(drop=True)


vector_b = data_merged['RightEye_distance_B']
#vector_b.rename("RightEye_distance_B")
firstIndex = (min(vector_b.index))
vector_b.loc[firstIndex-1] = 0
vector_b.sort_index(inplace=True)
#vector_b.index = vector_b.index + 1
"""
#counter = 0 
# preStimList = []
# for stim in preDenoise_imageList:
# 	counter += 1
# 	stimNumber = "stim_" + str(counter)
# 	preStimList.append(stimNumber)

# counter = 0 
# postStimList = []
# for stim in postDenoise_imageList:
# 	counter += 1
# 	stimNumber = "stim_" + str(counter)
# 	postStimList.append(stimNumber)

# print (list(set(preStimList) - set(postStimList)))

"""
	fig = plt.figure()

	ax1 = single_image_df.plot(kind='scatter', x='trial_number', y='CursorX', color='r', label='X')
	ax2 = single_image_df.plot(kind='scatter', x='trial_number', y='CursorY', color='g', label='Y', ax=ax1)

	#ax1 = single_image_df.plot(x='trial_number', y='CursorX', style='.-', color='r')
	#ax2 = single_image_df.plot(x='trial_number', y='CursorY', style='.-', color='g', ax=ax1)

	plt.suptitle('subject%s %s'%(subNum, image))
	plt.ylabel("Coordinates")
	plt.xlabel("Trials")
	#plt.show()
	plt.savefig('/study/midusref/DATA/Eyetracking/david_analysis/data_processed/%s/%s_%s.png'%(subNum, subNum, image))
	"""
