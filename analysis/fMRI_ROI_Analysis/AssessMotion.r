#library(ggsignif)
library(ggplot2)
#library(ggpubr)
# To do
# ANNOTATE R AND P VALUES


data <- read.csv("/Users/SB/Desktop/rs_fmri_motion_all_studies.csv", sep=',', header=TRUE)

# Check columnames
colnames(data)

# N for each Study
table(data$group)

# Violin Plot by Study
ggplot(data, aes(group, lossPercent, color=group)) +
  #geom_violin(trim=FALSE, aes(fill=group)) +
  geom_violin() +
  geom_boxplot(width=0.1) +
  xlab("Study") +
  ylab("TR Loss (%)") +
  labs(color='Study') +
  theme_minimal()

# Scatter Plot by age
ggplot(data, aes(x=age, y=lossPercent)) +
  geom_point(aes(color=group)) +
  xlab("Age (Year)") +
  ylab("TR Loss (%)") +
  geom_smooth(method='lm', se = FALSE, col="black") +
  labs(color='Study') +
  theme_bw()

# Quick Corr Test
cor.test(data$lossPercent, data$age)

# Linear Regression
mod3 = lm(lossPercent ~ age, data)
summary(mod3)

# Diagnostic Plot
par(mfrow=c(2,2))
plot(mod3)

# Subset by row index
MIDUS_Iterations <- data[1:192,,drop=F]
MIDUS3 <- data[1:49,,drop=F]
MIDUSREF <- data[73:192,,drop=F]
EMOWRAP <- data[50:72,,drop=F]
NERDS <- data[193:285,,drop=F]

# Descriptive Stats for each Study
hist(data$lossPercent, breaks=15, col="red")
hist(data$age, breaks=15, col="blue")
mean(data$lossPercent)
median(data$lossPercent)

median(MIDUSREF$lossPercent)
median(EMOWRAP$lossPercent)
median(MIDUS3$lossPercent)
median(NERDS$lossPercent)

median(MIDUSREF$age)
median(EMOWRAP$age)
median(MIDUS3$age)
median(NERDS$age)

# Plot average motion of each TR across three studies
data_by_TR <- read.csv("/Users/SB/Desktop/rs_fmri_motion_each_TR.csv", sep=',', header=TRUE)

colnames(data_by_TR)

ggplot(data_by_TR, aes(x=numberTR, y=averageMotion)) +
  geom_point(aes(color=group)) +
  xlab("TR number") +
  ylab("Motion (FD)") +
  labs(color='Study') +
  geom_line(aes(color=group)) +
  theme_bw()

# Plot motion for ts FMRI data

# Read in task motion data
ts_data <- read.csv("/Users/SB/Desktop/ts_fmri_motion_all_studies.csv", sep=',', header=TRUE)
colnames(ts_data)

MIDUS3_ts <- ts_data[358:504,,drop=F]
MIDUSREF_ts <- ts_data[1:357,,drop=F]
EMOWRAP_ts <- ts_data[505:579,,drop=F]

# Read in demographics data
demo <- read.csv("/Users/SB/Desktop/demographics_all_studies.csv", sep=',', header=TRUE)

MIDUS3_demo <- demo[1:49,,drop=F]
MIDUSREF_demo <- demo[73:192,,drop=F]
EMOWRAP_demo <- demo[50:72,,drop=F]

# Merge them by study
MIDUS3_merge <- merge(MIDUS3_ts, MIDUS3_demo,by=c("subject","subject"))
MIDUSREF_merge <- merge(MIDUSREF_ts, MIDUSREF_demo,by=c("subject","subject"))
EMOWRAP_merge <- merge(EMOWRAP_ts, EMOWRAP_demo,by=c("subject","subject"))

#write.csv(merge, "/Users/SB/Desktop/demo_ref.csv")
# Merge all studies
merge <- rbind(MIDUS3_merge, MIDUSREF_merge)
merge <- rbind(merge, EMOWRAP_merge)
colnames(merge)

# Quick corr test
cor.test(merge$lossPercent, merge$age)

# Linear Regression
mod = lm(lossPercent~ age, merge)
summary(mod)

# Diagnostic Plot
par(mfrow=c(2,2))
plot(mod)

# Violin Plot by Study
ggplot(merge, aes(group.x, lossPercent, color=group.x)) +
  #geom_violin(trim=FALSE, aes(fill=group)) +
  geom_violin() +
  geom_boxplot(width=0.1) +
  xlab("Study") +
  ylab("TR Loss (%)") +
  labs(color='Study') +
  theme_minimal()

# Scatter Plot by age
ggplot(merge, aes(x=age, y=lossPercent)) +
  geom_point(aes(color=group.x)) +
  xlab("Age (Year)") +
  ylab("TR Loss (%)") +
  geom_smooth(method='lm', se = FALSE, col="black") +
  labs(color='Study') +
  #geom_text(aes(label=subject),hjust=0, vjust=0) +
  theme_bw()

# Plot both task and resting
both <- read.csv("/Users/SB/Desktop/rs_ts_motion.csv", sep=',', header=TRUE)
colnames(both)

both$runNumber <- as.factor(both$runNumber)

# Violin Plot by Study
ggplot(both, aes(group, absoluteDisplacement, color=group)) +
  #geom_violin(trim=FALSE, aes(fill=group)) +
  geom_violin() +
  geom_boxplot(width=0.1) +
  xlab("Study") +
  ylab("Motion (FD)") +
  labs(color='Study') +
  ggtitle("Average Motion in Task and Resting fMRI data by Study") +
  theme_minimal()

# Violin Plot by runNumber
p <- ggplot(both, aes(runNumber, absoluteDisplacement, color=runNumber)) +
  #geom_violin(trim=FALSE, aes(fill=group)) +
  geom_violin() +
  geom_boxplot(width=0.1) +
  xlab("ScanType") +
  ylab("Motion (FD)") +
  labs(color='ScanType') +
  ggtitle("Average Motion in Task and Resting fMRI data by Scan Type") +
  theme_minimal()

p + scale_colour_hue(name="ScanType", 
                      breaks=c("1", "2", "3", "4"),
                      labels=c("task_1", "task_2", "task_3", "resting")) +
  scale_x_discrete(labels = c("task_1", "task_2", "task_3", "resting"))






# Scatter Plot by age
ggplot(both, aes(x=age, y=lossPercent)) +
  geom_point(aes(color=runNumber)) +
  xlab("Age (Year)") +
  ylab("TR Loss (%)") +
  geom_smooth(method='lm', se = FALSE, col="black") +
  labs(color='Study') +
  theme_bw()
# Other useful plots
# If date needs be ploted
#data_filtered$date <- as.Date(data_filtered$date,'%m/%d/%Y')

# Remove NA data
data_filtered <- na.omit(data)

# BarPlot by ScanTech
ggplot(data_filtered, aes(scan.tech, lossPercent, fill=group)) +
  geom_signif(comparisons = list(c("Michael", "Ron", "Scott")), map_signif_level=TRUE) +
  stat_summary(geom="bar", fun.y="mean", position="dodge") +
  ggtitle("MIDUS3/EMORWAP rs-fMRI motion by MR tech") +
  theme(plot.title=element_text(hjust =0.5, size = 20))
  #stat_summary(geom="errorbar", fun.data = mean_se, position="dodge")

# Barplot by ScanTech with error bars
ggbarplot(data_filtered, x = "scan.tech", y = "absoluteDisplacement", add = "mean_se",
          color = "group", palette = "jco", 
          position = position_dodge(0.8))+
  stat_compare_means(aes(group = group), label = "p.signif", label.y = 0.5)


# Check how many scans per scantech
table(data$scan.tech)
#length((data_filtered$scan.tech))

# Scatter Plot by Experimenter
ggplot(data_filtered, aes(x=experimenter, y=absoluteDisplacement)) +
  geom_point(aes(color=group)) +
  geom_text(aes(label=subject),hjust=0, vjust=0)
#geom_text(aes(label=subject))

# Remove Outliers 3 SD
SDthreshHigh <- mean(data_filtered$absoluteDisplacement,na.rm=T)+3*(sd(data_filtered$absoluteDisplacement, na.rm=T))
SDthreshLow <- mean(data_filtered$absoluteDisplacement,na.rm=T)-3*(sd(data_filtered$absoluteDisplacement, na.rm=T))

SDthreshHigh
SDthreshLow

# Subset w/o Outliers
data_clean <- subset(data_filtered, absoluteDisplacement < SDthreshHigh & absoluteDisplacement > SDthreshLow )

