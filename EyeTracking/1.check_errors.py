import os
import glob

path = "/study/midusref/DATA/Eyetracking/david_analysis/python/logs/process_eyetracking_[0-9][0-9][0-9].out"

files = glob.glob(path)

for file in files:
	subNum = file.split('/')[8][-7:-4]
	print (subNum)
	os.system("tail -n 1 %s >> /study/midusref/DATA/Eyetracking/david_analysis/QA/error.txt"%(file))
