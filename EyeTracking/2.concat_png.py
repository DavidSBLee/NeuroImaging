import os
import glob

path = "/study4/midusref/DATA/Eyetracking/david_analysis/data_processed/[0-9][0-9][0-9]/*.png"
outhtml = "/study4/midusref/DATA/Eyetracking/david_analysis/QA/QA.html"

files = glob.glob(path)

for file in files:
	subNum = file.split('/')[7]
	IAPSnum = file.split('/')[8][-8:-4]

	print (subNum)
	print (IAPSnum)
	
	os.system("echo '<br><br> EyeGaze Plot %s %s <br><IMG BORDER=0 SRC=%s WIDTH=1000></BODY></HTML> <p>==========================================================<p>' >> %s"%(subNum, IAPSnum, file, outhtml))