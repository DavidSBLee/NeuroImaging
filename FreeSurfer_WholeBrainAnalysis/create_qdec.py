import pandas as pd
import numpy as np

# DEMEAN AGE
# DEMEAN COVARIATES


infile = "/Volumes/study4/midusref/DATA/mri/processed/freesurfer/david/freesurfer_with_pwb.csv"
outfile = "/Users/SB/Desktop/qdec.table.dat"

def create_variables():
	df1 = pd.read_csv(infile, sep=',')
	df2 = df1.iloc[:, [0, 3, 4, 9, 12, 52, 53, 54, 55, 56, 57, 58, 59, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626]]
	df3 = df2.sort_values(["subID"])

	# Rename Columns
	#df3 = df3.rename(columns={'R5PGENDER':'gender'})

	"""
	# Round decimals
	df3.loc[:,'PWB_Autonomy_7'] = df3.loc[:,'PWB_Autonomy_7'].round(0)
	df3.loc[:,'PWB_EnvMastery_7'] = df3.loc[:,'PWB_EnvMastery_7'].round(0)
	df3.loc[:,'PWB_PersonalGrowth_7'] = df3.loc[:,'PWB_PersonalGrowth_7'].round(0)
	df3.loc[:,'PWB_PosRelationsOthers_7'] = df3.loc[:,'PWB_PosRelationsOthers_7'].round(0)
	df3.loc[:,'PWB_PurposeLife_7'] = df3.loc[:,'PWB_PurposeLife_7'].round(0)
	df3.loc[:,'PWB_SelfAcceptance_7'] = df3.loc[:,'PWB_SelfAcceptance_7'].round(0)
	df3.loc[:,'PWB_Composite'] = df3.loc[:,'PWB_Composite'].round(0)
	df3.loc[:,'PWB_Average'] = df3.loc[:,'PWB_Average'].round(2)
	df3.loc[:,'PWB_AUTxAge'] = df3.loc[:,'PWB_AUTxAge'].round(0)
	df3.loc[:,'PWB_ENVxAge'] = df3.loc[:,'PWB_ENVxAge'].round(0)
	df3.loc[:,'PWB_PGROWTHxAge'] = df3.loc[:,'PWB_PGROWTHxAge'].round(0)
	df3.loc[:,'PWB_POSRELxAge'] = df3.loc[:,'PWB_POSRELxAge'].round(0)
	df3.loc[:,'PWB_PURPOSExAge'] = df3.loc[:,'PWB_PURPOSExAge'].round(0)
	df3.loc[:,'PWB_SELFACCEPTxAge'] = df3.loc[:,'PWB_SELFACCEPTxAge'].round(0)
	df3.loc[:,'PWB_COMPxAGE'] = df3.loc[:,'PWB_COMPxAGE'].round(0)
	df3.loc[:,'PWB_AVGxAGE'] = df3.loc[:,'PWB_AVGxAGE'].round(2)
	

	# Round decimals
	df3.loc[:,'scaled_PWB_Autonomy_7'] = df3.loc[:,'scaled_PWB_Autonomy_7'].round(2)
	df3.loc[:,'scaled_PWB_EnvMastery_7'] = df3.loc[:,'scaled_PWB_EnvMastery_7'].round(2)
	df3.loc[:,'scaled_PWB_PersonalGrowth_7'] = df3.loc[:,'scaled_PWB_PersonalGrowth_7'].round(2)
	df3.loc[:,'scaled_PWB_PosRelationsOthers_7'] = df3.loc[:,'scaled_PWB_PosRelationsOthers_7'].round(2)
	df3.loc[:,'scaled_PWB_PurposeLife_7'] = df3.loc[:,'scaled_PWB_PurposeLife_7'].round(2)
	df3.loc[:,'scaled_PWB_SelfAcceptance_7'] = df3.loc[:,'scaled_PWB_SelfAcceptance_7'].round(2)
	df3.loc[:,'scaled_age'] = df3.loc[:,'scaled_age'].round(2)
	df3.loc[:,'scaled_PWB_Average'] = df3.loc[:,'scaled_PWB_Average'].round(2)
	df3.loc[:,'PWB_AUTxAge'] = df3.loc[:,'PWB_AUTxAge'].round(2)
	df3.loc[:,'PWB_ENVxAge'] = df3.loc[:,'PWB_ENVxAge'].round(2)
	df3.loc[:,'PWB_PGROWTHxAge'] = df3.loc[:,'PWB_PGROWTHxAge'].round(2)
	df3.loc[:,'PWB_POSRELxAge'] = df3.loc[:,'PWB_POSRELxAge'].round(2)
	df3.loc[:,'PWB_PURPOSExAge'] = df3.loc[:,'PWB_PURPOSExAge'].round(2)
	df3.loc[:,'PWB_SELFACCEPTxAge'] = df3.loc[:,'PWB_SELFACCEPTxAge'].round(2)
	df3.loc[:,'PWB_AVGxAge'] = df3.loc[:,'PWB_AVGxAge'].round(2)
	"""
	# Convert column subID's datatype as strings
	df3.loc[:,'subID'] = df3.loc[:,'subID'].astype(str)
	df3.loc[:,'SAMPLMAJ'] = df3.loc[:,'SAMPLMAJ'].astype(str)
	df3.loc[:,'BMI'] = df3.loc[:,'BMI'].astype(float)

	#df3.loc[:,'Variables'] = df3.loc[:,'Variables'].astype(int)
	# Replace R5PGENDER coding
	df3.loc[df3['SAMPLMAJ'] == '20', 'SAMPLMAJ'] = 'Non-Milwaukee'
	df3.loc[df3['SAMPLMAJ'] == '21', 'SAMPLMAJ'] = 'Milwaukee'

	# Zero pad subID
	df3['subID'] = df3['subID'].apply(lambda x: x.zfill(3))

	print (df3)
	
	# Make fsdg file 
	df3.to_csv(outfile, index=False, sep=' ', header=True) #float_format='%.2f')
	
	

create_variables()
