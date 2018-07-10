library(tidyverse)
library(readr)
library(data.table)
library(dplyr)

# Read-in Data, what's the memory-free way again? fread?
data = read.table("/Users/SB/Desktop/corrugator.csv", header=TRUE, sep=",", na.strings="NA")
colnames (data)
# View few rows
head(data)

# Memory is so puny, need to cutout the columns of interest
#subData = data[c(1:90)]

# Select rows(Subjects) that have filter quality = 1 (change column name to exclude $)
newData <- subset(data, M3_CORR_ANALYSIS_FILTER == 1 & filter == 1)
# or newData <- data[ which( filter == 1 & M3_CORR_ANALYSIS_FILTER == 1) , ]

#---------- Make long format for 12 epochs
M2corr <- paste("dlog.neu", 1:12, sep="")
M3corr <- paste("dlog_cor.neu", 1:12, sep="")
myvars <- c("RESPID", M2corr, M3corr)
new <- newData[myvars]
gathervars <- c(M2corr, M3corr)
data.long = gather(new, corr, value, gathervars)

# now make a column for long foramt timepoint(1,2) and epoch #(1-3)
data.long$timepoint <- NA
data.long$epoch <- NA
#grepl("cor", dat.log$corr)
data.long <- mutate(data.long, timepoint = ifelse(grepl("dlog.neu", data.long$corr), "1","2"))

# sort dataframe by column
#data.sorted <- data.long[order(data.long$RESPID), ]

# Create a vector 
#vector <- rep(1:12, each=74)

data.long$epoch <- as.numeric(gsub("[^0-9][^0-9]", "", data.long$corr))


# Make epoch and timepoint factor (used to be character)
data.long$epoch <- as.factor(data.long$epoch)
data.long$timepoint <- as.factor(data.long$timepoint)
data.long$RESPID <- as.factor(data.long$RESPID)

class(data.long$epoch)
class(data.long$timepoint)
class(data.long$RESPID)

#----------Make long format for 3 averaged epochs
# Extract Column Headers in a vector
colHead <- (names(newData))
colnames(newData)
# Make longformat for averaged 3 epochs

#colHead <- (names(newData))
#grx <- glob2rx("M2_dcor.neg.*")
#M2_data <- grep(grx, colHead)

# In a single line
# M2 data
M2_data <- grep(glob2rx("M2_dcor.neg.*"), colHead)
# Subset the character vector
M2_data <- M2_data[c(1, 2, 3)]
# M3 data
M3_data <- grep(glob2rx("M3_dcor.neg.*"), colHead)
# Subset the character vector
M3_data <- M3_data[c(1, 2, 3)]

# Check variable headers of interest
#M2_data <- grep("M2_dcor.[a-z][a-z][a-z].*", colHead)
names(newData)[M2_data]
names(newData)[M3_data]

# Merge Column Numbers for RESPID, M2_Corr, and M3_Corr
myvars <- c(1, M2_data, M3_data)
myvars
# Create a dataframe with variables of interest
new <- newData[myvars]
#new <- newData[myvars]
#gathervars <- c(M2_data, M3_data)

# Transform dataframe into long fomrat using dplyr's "gather" function
data.long = gather(new, corr, value, c(-1))

# now make a column for long foramt timepoint(1,2) and epoch #(1-3)
data.long$timepoint <- NA
data.long$epoch <- NA
#grepl("cor", dat.log$corr)
data.long <- mutate(data.long, timepoint = ifelse(grepl("M2", data.long$corr), "1","2"))

data.long <- mutate(data.long, epoch = ifelse(grepl("early", data.long$corr), "1", 
                                         ifelse(grepl("mid", data.long$corr), "2",
                                         ifelse(grepl("late", data.long$corr), "3", "error"))))

# Make epoch and timepoint factor (used to be character)
data.long$epoch <- as.factor(data.long$epoch)
data.long$timepoint <- as.factor(data.long$timepoint)
data.long$RESPID <- as.factor(data.long$RESPID)

class(data.long$epoch)
class(data.long$timepoint)
class(data.long$RESPID)

# 0. Plot the data 
library(ggplot2)
ggplot(data.long, aes(x = epoch, y = value, color = timepoint, group = timepoint)) + 
  geom_point() +
  geom_line() +
  facet_wrap(~ RESPID) 
  
# 1. Epoch Analysis (Use Partial Data by extracting only single timepoint)
# Subset a datafame with only MIDUS2 or MIDUS3 
newData <- data.long[data.long$timepoint == 1,]
newData <- data.long[data.long$timepoint == 2,]

#install.packages("lmerTest")
library(lmerTest)

# compare means for epoch1 vs. epoch2, epoch1 vs. epoch3
# within subject in the random effects structure
# between subject in the fixed effects structure
mod <- lmer(value ~ epoch +1  + (1 | RESPID), newData)
summary(mod)

# buy putting 1 instead of epoch, compare means for epoch2 vs. epoch3
mod2 <- lmer(value ~ 1 + (1 | RESPID), newData)
summary(mod2)

anova(mod, mod2)

# 2. Interaction (Use all data for two timepoints)

mod3 <- lmer(value ~ epoch*timepoint + (1 | RESPID), data.long)
summary(mod3)

# 2.1 2-way Interaction betwwen time and epoch (nested model)
# are there effects between epochs within a time or between times within an epoch
mod1 = lmer(value ~ epoch * timepoint + (1 | RESPID), data = data.long)
summary(mod1)
mod2 = lmer(value ~ epoch + timepoint + (1 | RESPID), data = data.long)
summary(mod2)
anova(mod1, mod2)

# 3. T2 vs. T1 (1EPOCH)
# Subset a dataframe with single Epoch
singleEpochData <- data.long[data.long$epoch == 3,]

mod4 <- lmer(value ~ 1 + timepoint + (1 | RESPID), singleEpochData)
summary(mod4)

# 4. Twins???
# Not enough twins in the dataset! 



# Install lme4 package
# install.packages("lme4")

# Import lme4 library
#library("lme4")

# Fit a linear model 
#for (i in 1:12){
  #print(i)
  #sprintf("model%s", i) <- sprintf("lm(dlog.neg%s ~ dlog_cor.neg%s), data=newData", i, i)
  #model[i] <- lm(dlog.neg[i] ~ dlog_cor.neg[i], data=newData)
#}
#model1 <- lm(dlog.pos4 ~ dlog_cor.pos4, data=newData)
#summary(model1)

# Plot the data
#library(ggplot2)
#ggplot(newData, aes(x=dlog.pos3, y=dlog_cor.pos3)) +
  #geom_point() +
  #geom_smooth(method = "lm")

# Mixed Model (Random Effects Structure)
# For negative Trials 
# Between Subject Variance, then Within Subject Variance
mixed.model1 <- lmer(value ~ epoch + (1 + timepoint | RESPID), data=data.long) # REML = FALSE
summary(mixed.model1)

plot(mixed.model1)

qqnorm(resid(mixed.model1))
qqline(resid(mixed.model1))
