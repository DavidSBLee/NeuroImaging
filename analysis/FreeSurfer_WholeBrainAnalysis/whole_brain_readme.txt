Couple things about QDEC

Cons
1. Deprecated (No Longer in Use, use commandline way)
2. Would not take manually resampled + smoothed files (the input needs to be reconstructed with -qcache)
3. Would not take study-specific templates (would only take fsaverage)
4. Can't put more than two covariates and two 

Pros
1. Easy to test different variables quickly as long as I have dataframe(qdec table)
2. Creates FSGD file for me! Though it is easy to create one manually, this saves little bit of time 
3. I can alter between 5mm to 25mm smoothing kernels as -qcache has already done all kernels for me (otherwise, I have to create my stduy specific tempalte in all kernel sizes - I can, but I only have 10mm right now. that is the defulat.)
4. Can click on each vertex, and look at the plots for that

Conclusion
1. Create QDEC table with all of your variable of interest
2. Run differnt pilot analyses as a exploratory testing
3. Try diffent kernel sizes to see which one best visualizes your results
4. Use the fsgd created to explore results in "study specific template". remember QDEC can only use the default template! not good! concerning the age range in MIDUSREF sample
4. Multiple Comparisons?

Caveat
1. First Column name of QDEC table MUST BE "fsid"
2. FSGD files can be created either manullay or by script, if manually done, save it as tab deliemated file using excel, and eliminate carriage returns that cannot be read by UNIX 
tr '\r' '\n' < input.txt > new.fsgd
3. QDEC would not take subjects with N/A's in any of their variables


export SUBJECTS_DIR=/study4/midusref/DATA/mri/processed/freesurfer
echo $SUBJECTS_DIR
cd $SUBJECTS_DIR


freeview -f $SUBJECTS_DIR/fsaverage_david/surf/lh.inflated:annot=aparc.annot:annot_outline=1:overlay=david/lh.age_pwb_david.glmdir/lh-avg-thickness-age-pwb-cor/sig.mgh:overlay_threshold=1.3,5 -viewport 3d


# Thickness with Age, controlling for Gender
freeview -f $SUBJECTS_DIR/fsaverage_david/surf/lh.inflated:annot=aparc.annot:annot_outline=1:overlay=david/thickness_age_cor/lh.gender_age_david.glmdir/lh-Avg-thickness-age-Cor/sig.mgh:overlay_threshold=4,5 -viewport 3d

# Thickness with PWB, controlling for Gender
freeview -f $SUBJECTS_DIR/fsaverage_david/surf/lh.inflated:annot=aparc.annot:annot_outline=1:overlay=david/thickness_pwb_cor/lh.gender_pwb.thickness.glmdir/lh-Avg-thickness-pwb-cor/sig.mgh:overlay_threshold=4,5 -viewport 3d

# Thickness with Age (Scaled), controlling for Gender
freeview -f $SUBJECTS_DIR/fsaverage_david/surf/lh.inflated:annot=aparc.annot:annot_outline=1:overlay=david/thickness_age_scaled_cor/lh.gender_age_scaled_david.glmdir/lh-avg-thickness-age-cor/sig.mgh:overlay_threshold=4,5 -viewport 3d

# Simulation
mri_glmfit-sim \
  --glmdir david/lh.gender_pwb.thickness.glmdir \
  --cache 4 neg \
  --cwp  0.05\
  --2spaces


# Viweing Clutsers
freeview -f $SUBJECTS_DIR/fsaverage/surf/rh.inflated:overlay=david/rh.gender_pwb.thickness.glmdir/rh-Avg-thickness-pwb-cor/cache.th13.pos.sig.cluster.mgh

freeview -f $SUBJECTS_DIR/fsaverage/surf/lh.inflated:overlay=david/thickness_pwb_cor/lh.gender_pwb.thickness.glmdir/lh-Avg-thickness-pwb-cor/cache.th40.neg.sig.cluster.mgh:overlay_threshold=2,5:annot=david/thickness_pwb_cor/lh.gender_pwb.thickness.glmdir/lh-Avg-thickness-pwb-cor/cache.th40.neg.sig.ocn.annot -viewport 3d