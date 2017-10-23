# This script loops through all subjects and creates onset files.  I'm starting simple, only creating the onset files needed for the IAPS stimuli.  

##IMPORTANT:  I PLAN TO TRIM 5 VOLUMES FROM THE BOLD DATA, SO 10S MUST BE SUBTRACTED FROM ONSET TIMES!!!

#Note: Maindir was updated for MIDUS3 data on 6/9/17; other tweaks to script may be necessary to adapt it to MIDUS3 data (e.g., changing definitions of subID, runnum, ?type?; also need directory to write out onset files. FIRST, where are .tsv files???)-MK

library(tidyr)

maindir = "/study3/midus3/processed_data/my_dataset"

files = Sys.glob(sprintf("%s/sub*/func/*.tsv", maindir))

num.files = length(files)

# I want to double check the min time between the onset of two stimuli to set my window properly for the FIR model
min.soa = rep(NA, num.files)
num.stim = rep(NA, num.files)
max.time = rep(NA, num.files)
min.time = rep(NA, num.files)

for (i in 1:num.files){
  cur.filename = files[i]
  cur.fileroot = basename(cur.filename)

    # extract subject ID- This will break if files are moved
  subid = unlist(strsplit(cur.fileroot, "_"))[1]  
  subid = unlist(strsplit(subid, "-"))[3]
  # Ditto for run number
  runnum = unlist(strsplit(cur.fileroot, "_"))[3]
  # Read in the data
  cur.dat = read.table(files[i], sep = "\t", header = TRUE)
  dim.cur.dat = dim(cur.dat)[1]

  if (dim.cur.dat>10) {
    # First determine whether this is a 1/3s or no face stimulus  
    trial.num.diff = c(diff(cur.dat$trial_number), 0)
    iaps.ind = 1-trial.num.diff[cur.dat$database == "IAPS"]    # 0 = no face
    ons.diff = c(diff(cur.dat$onset), 0)
    ons.diff.iaps = ons.diff[cur.dat$database == "IAPS"]-4
    iaps.ind = iaps.ind*ons.diff.iaps  #Takes value of 0, 1 or 3
    
    # Extract IAPs time points first
    dat.iaps = cur.dat[cur.dat$database == "IAPS",]
    min.soa[i] = min(diff(dat.iaps$onset))
    num.stim[i] = dim(cur.dat)[1]
    max.time[i] = max(cur.dat$onset)
    min.time[i] = min(cur.dat$onset)
    # I'm going to create zero duration onsets for the FIR models (these don't get used...)
   
   # Write out onset file
    for (type in c("neg", "neu", "pos")){
      for (face in c(0, 1, 3)){
        cur.onset = dat.iaps$onset[dat.iaps$iaps_valence == type & iaps.ind == face]-10
        num.onset = length(cur.onset)
        three.col.format = cbind(cur.onset, rep(0, num.onset), rep(1, num.onset)) 
        write.table(three.col.format, file = sprintf("%s/sub-M2ID-%s/beh/%s_iaps_%s_face_zero_dur_%s.txt", maindir, subid, type,face, runnum), col.names = FALSE, quote = FALSE, row.names = FALSE)
    }
   }
  }

 }

