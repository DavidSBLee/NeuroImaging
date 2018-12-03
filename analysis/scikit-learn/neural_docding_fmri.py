get_ipython().magic('matplotlib inline')


# Extract the fMRI data on a mask and convert it to data series


mask = '/Volumes/study4/midusref/midusref_imaging_public2/imaging_updated_2018-02-12/MIDUSREF_Imaging_Analysis/sub-MRID-30024/anat/sub-MRID-30024_T1w_1_brain_mask.nii.gz'


anat = '/Volumes/study4/midusref/midusref_imaging_public2/imaging_updated_2018-02-12/MIDUSREF_Imaging_Analysis/sub-MRID-30024/anat/sub-MRID-30024_T1w_1.nii.gz'


func = '/Volumes/study4/midusref/midusref_imaging_public2/imaging_updated_2018-02-12/MIDUSREF_Imaging_Analysis/sub-MRID-30024/func/sub-MRID-30024_task-emotion-regulation_run-3_bold_mod.nii.gz'


from nilearn import plotting


plotting.plot_roi(mask,bg_img=anat, cmap='Paired')


from nilearn.input_data import NiftiMasker


masker = NiftiMasker(mask_img=mask, standardize=True)


# Retrieve 2D Array data of fMRI time series


fmri_masked = masker.fit_transform(func)


fmri_masked.shape


fmri_masked[:5]


import pandas as pd 
import numpy as np

def label_IAPS_TR(columnName, valueName):

		indexList = df5.index[df5[columnName] == valueName].tolist()
		indexList1 = [i+1 for i in indexList]
		indexList2 = [i+2 for i in indexList]
		indexList3 = [i+3 for i in indexList]
		FullIndexList = indexList1 + indexList2 + indexList3 
		FullIndexList = sorted(FullIndexList)
		for i in FullIndexList:
			df5.loc[i, columnName] = valueName

infile = '/Volumes/study4/midusref/midusref_imaging_public2/imaging_updated_2018-02-12/sub-MRID-30024/func/sub-MRID-30024_task-emotion-regulation_run-2_events.tsv'
outfile = '/Users/SB/Desktop/30024_run2_output.csv'

with open (outfile, 'wb') as output:
	# Read csv as pandas dataframe
	df1 = pd.read_csv(infile, sep='\t')
	# Extract Columns of interest
	df2 = df1.iloc[:,[0,1,2,6,7,9]]
	# Round onset column to 0 decimal point, and cast integer
	df2.loc[:,'onset'] = df2.loc[:,'onset'].round(0).astype(int)

	# Create a column with 1~227
	#df2.insert(0, 'time', range(1, 227))
	#df3 = df2.assign(time = pd.Series(np.arange(1, 227, 1)))
	df3 = pd.DataFrame({'onset':np.arange(1, 455, 1)})

	# Combine data frames by column
	df4 = pd.concat([df2, df3], ignore_index=True, axis=0)
	# Sort data frames based on two columns
	df4 = df4.sort_values(["onset", "database"])
	
	df5 = df4.drop_duplicates(subset='onset', keep='first')
	df5 = df5.reset_index()

	label_IAPS_TR('database', 'IAPS')
	label_IAPS_TR('valence', 'positive')
	label_IAPS_TR('valence', 'negative')
	label_IAPS_TR('valence', 'neutral')

	# Replace NaN in valence column
	df5['database'] = df5['database'].fillna('rest')
	df5['valence'] = df5['valence'].fillna('rest')

	# LUMP TRs to fit 227 TRs
	#df5 = df5.iloc[::2]
	df5 = df5.drop(df5[(df5.onset%2 != 0)].index)
	df5 = df5.reset_index()
	#df5 = df5.drop(df5[(df5.onset%2 == 0) & (df5.valence != 'positive') & (df5.valence != 'negative') & (df5.valence != 'neutral')].index)
	#df5 = df5[:227]

	# Extract column of interest
	df5 = df5[['valence']]
	df5.to_csv(outfile, index=False)
	df6 = pd.read_csv(outfile, squeeze=True)

	# Create a mask the corresponds to postivie and negative IAPS (True&False)
	condition_mask = df6.isin(['positive', 'negative'])

	# Apply to mask to both data and labels
	conditions = df6[condition_mask]
	fmri_masked_four = fmri_masked[condition_mask]
	
	# Write to CSV
	#print (conditions)
	#conditions.to_csv(outfile, index=False)
	


condition_mask.shape


from sklearn.svm import SVC
svc = SVC(kernel='linear')
print(svc)


svc.fit(fmri_masked_two, conditions)


prediction = svc.predict(fmri_masked_three)
print(prediction)


print((prediction == conditions).sum() / float(len(conditions)))


svc.fit(fmri_masked_two[:-20], conditions[:-20])

prediction = svc.predict(fmri_masked_two[-20:])
print((prediction == conditions[-20:]).sum() / float(len(conditions[-20:])))


from sklearn.cross_validation import KFold

cv = KFold(n=len(fmri_masked_two), n_folds=5)

for train, test in cv:
    conditions_masked = conditions.values[train]
    svc.fit(fmri_masked_two[train], conditions_masked)
    prediction = svc.predict(fmri_masked_two[test])
    print((prediction == conditions.values[test]).sum()
           / float(len(conditions.values[test])))


from sklearn.cross_validation import cross_val_score
cv_score = cross_val_score(svc, fmri_masked_two, conditions)
print(cv_score)


cv_score = cross_val_score(svc, fmri_masked_two, conditions, cv=5)
print(cv_score)


coef_ = svc.coef_
print(coef_)


print(coef_.shape)


coef_img = masker.inverse_transform(coef_)
print(coef_img)


coef_img.to_filename('/Users/SB/Desktop/MIDUSREFE_svc_weights.nii.gz')


from nilearn.plotting import plot_stat_map, show

plot_stat_map(coef_img, bg_img=mask,
              title="SVM weights", display_mode="yx")

show()

