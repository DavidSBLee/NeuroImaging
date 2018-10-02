import pandas as pd
import glob

path = "/study4/midusref/DATA/Eyetracking/david_analysis/data_processed/*/*_valid_IAPS.csv"
files = glob.glob(path)

df_list = []
for file in files:
	df = pd.read_csv(file)
	df_list.append(df)


frame = pd.concat(df_list, join='outer', ignore_index=True)
frame.to_csv("/study4/midusref/DATA/Eyetracking/david_analysis/QA/all_valid_IAPS.csv")


path = "/study4/midusref/DATA/Eyetracking/david_analysis/data_processed/*/*_valid_STIM.csv"
files = glob.glob(path)

df_list = []
for file in files:
	df = pd.read_csv(file)
	df_list.append(df)


frame = pd.concat(df_list, join='outer', ignore_index=True)
frame.to_csv("/study4/midusref/DATA/Eyetracking/david_analysis/QA/all_valid_STIM.csv")