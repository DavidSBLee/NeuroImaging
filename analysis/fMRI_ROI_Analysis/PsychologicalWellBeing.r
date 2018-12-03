subCor_data <- read.csv("/study4/midusref/DATA/mri/processed/freesurfer/ExtractedValueSpreadsheets/2018-04-04-aseg-volume-table.csv", header=TRUE)
behv_data <- read.csv("/home/slee/Desktop/MIDUSREF_beh_original.csv", header=TRUE)
numb_data <- read.csv("/home/slee/Desktop/MIDUSREF_SUBID_MRID.csv", header=TRUE)
pwb_data <- read.csv("/study4/midusref/Analyses/PWB/MIDUSREF_PWB_138_merged.csv", header=TRUE)

all <- merge(pwb_data, behv_data, by.x = 'RESPID', by.y = 'ID' )
data_merge <- merge(numb_data, all, by.x = 'MIDUSID', by.y = 'RESPID')
data_all <- merge(data_merge, subCor_data, by.x='subID', by.y='ID')

# Combine AA and Other subjects
data_all$PWB_Autonomy_7 <- rowSums(data_all[, c("RA1SPWBA2", "RAASPWBA2")], na.rm=T)
data_all$PWB_EnvMastery_7 <- rowSums(data_all[, c("RA1SPWBE2", "RAASPWBE2")], na.rm=T)
data_all$PWB_PersonalGrowth_7 <- rowSums(data_all[, c("RA1SPWBG2", "RAASPWBG2")], na.rm=T)
data_all$PWB_PosRelationsOthers_7 <- rowSums(data_all[, c("RA1SPWBR2", "RAASPWBR2")], na.rm=T)
data_all$PWB_PurposeLife_7 <- rowSums(data_all[, c("RA1SPWBU2", "RAASPWBU2")], na.rm=T)
data_all$PWB_SelfAcceptance_7 <- rowSums(data_all[, c("RA1SPWBS2", "RAASPWBS2")], na.rm=T)
data_all$PWB_Composite <- rowSums(data_all[, c("PWB_Autonomy_7", "PWB_EnvMastery_7", "PWB_PersonalGrowth_7", "PWB_PosRelationsOthers_7", "PWB_PurposeLife_7", "PWB_SelfAcceptance_7")])
data_all$PWB_Average <- rowMeans(data_all[, c("PWB_Autonomy_7", "PWB_EnvMastery_7", "PWB_PersonalGrowth_7", "PWB_PosRelationsOthers_7", "PWB_PurposeLife_7", "PWB_SelfAcceptance_7")])

# Mean Centering Continous Variable and adding as a column
scaled_PWB_Autonomy_7 <- scale(data_all$PWB_Autonomy_7, center = TRUE, scale = FALSE)
data_all["scaled_PWB_Autonomy_7"] <- scaled_PWB_Autonomy_7
mean(data_all$scaled_PWB_Autonomy_7)

scaled_PWB_EnvMastery_7 <- scale(data_all$PWB_EnvMastery_7, center = TRUE, scale = FALSE)
data_all["scaled_PWB_EnvMastery_7"] <- scaled_PWB_EnvMastery_7
mean(data_all$scaled_PWB_EnvMastery_7)

scaled_PWB_PersonalGrowth_7 <- scale(data_all$PWB_PersonalGrowth_7, center = TRUE, scale = FALSE)
data_all["scaled_PWB_PersonalGrowth_7"] <- scaled_PWB_PersonalGrowth_7
mean(data_all$scaled_PWB_PersonalGrowth_7)

scaled_PWB_PosRelationsOthers_7 <- scale(data_all$PWB_PosRelationsOthers_7, center = TRUE, scale = FALSE)
data_all["scaled_PWB_PosRelationsOthers_7"] <- scaled_PWB_PosRelationsOthers_7
mean(data_all$scaled_PWB_PosRelationsOthers_7)

scaled_PWB_PurposeLife_7 <- scale(data_all$PWB_PurposeLife_7, center = TRUE, scale = FALSE)
data_all["scaled_PWB_PurposeLife_7"] <- scaled_PWB_PurposeLife_7
mean(data_all$scaled_PWB_PurposeLife_7)

scaled_PWB_SelfAcceptance_7 <- scale(data_all$PWB_SelfAcceptance_7, center = TRUE, scale = FALSE)
data_all["scaled_PWB_SelfAcceptance_7"] <- scaled_PWB_SelfAcceptance_7
mean(data_all$scaled_PWB_SelfAcceptance_7)

scaledAge <- scale(data_all$R5PAGE, center = TRUE, scale = FALSE)
data_all["scaled_age"] <- scaledAge
mean(data_all$scaled_age)

scaledPWBComp <- scale(data_all$PWB_Composite, center = TRUE, scale = FALSE)
data_all["scaled_PWB_Composite"] <- scaledPWBComp
mean(data_all$scaled_PWB_Composite)

scaledPWBAvg <- scale(data_all$PWB_Average, center = TRUE, scale = FALSE)
data_all["scaled_PWB_Average"] <- scaledPWBAvg
mean(data_all$scaled_PWB_Average)

# Scale merged document
scaled_Autonomy_7Items <- scale(data_all$Autonomy_7Items, center = TRUE, scale = FALSE)
data_all["scaled_Autonomy_7Items"] <- scaled_Autonomy_7Items
mean(data_all$scaled_Autonomy_7Items)

scaled_EnvironmentalMastery_7Item <- scale(data_all$EnvironmentalMastery_7Item, center = TRUE, scale = FALSE)
data_all["scaled_EnvironmentalMastery_7Item"] <- scaled_EnvironmentalMastery_7Item
mean(data_all$scaled_EnvironmentalMastery_7Item)

scaled_PersonalGrowth_7Items <- scale(data_all$PersonalGrowth_7Items, center = TRUE, scale = FALSE)
data_all["scaled_PersonalGrowth_7Items"] <- scaled_PersonalGrowth_7Items
mean(data_all$scaled_PersonalGrowth_7Items)

scaled_PurposeInLife_7Items <- scale(data_all$PurposeInLife_7Items, center = TRUE, scale = FALSE)
data_all["scaled_PurposeInLife_7Items"] <- scaled_PurposeInLife_7Items
mean(data_all$scaled_PurposeInLife_7Items)

scaled_PositiveRelationsWithOthers_7Items <- scale(data_all$PositiveRelationsWithOthers_7Items, center = TRUE, scale = FALSE)
data_all["scaled_PositiveRelationsWithOthers_7Items"] <- scaled_PositiveRelationsWithOthers_7Items
mean(data_all$scaled_PositiveRelationsWithOthers_7Items)

scaled_SelfAcceptance_7Items <- scale(data_all$SelfAcceptance_7Items, center = TRUE, scale = FALSE)
data_all["scaled_SelfAcceptance_7Items"] <- scaled_SelfAcceptance_7Items
mean(data_all$scaled_SelfAcceptance_7Items)

scaled_Age_from_MR_Screen <- scale(data_all$Age_from_MR_Screen, center = TRUE, scale = FALSE)
data_all["scaled_Age_from_MR_Screen"] <- scaled_Age_from_MR_Screen
mean(data_all$scaled_Age_from_MR_Screen)

scaled_TotalPWB_7 <- scale(data_all$TotalPWB_7, center = TRUE, scale = FALSE)
data_all["scaled_TotalPWB_7"] <- scaled_TotalPWB_7
mean(data_all$scaled_TotalPWB_7)

scaled_TotalAvePWB_7 <- scale(data_all$TotalAvePWB_7, center = TRUE, scale = FALSE)
data_all["scaled_TotalAvePWB_7"] <- scaled_TotalAvePWB_7
mean(data_all$scaled_TotalAvePWB_7)

names(data_all)

write.csv(data_all,"/home/slee/Desktop/freesurfer_with_pwb.csv", row.names=FALSE)

cor.test(data_all$Left.Hippocampus, data_all$scaled_Age_from_MR_Screen)

str(data_all$Gender )
data_all$R5PGENDER <- as.factor(data_all$R5PGENDER)
str(data_all$R5C)
data_all$R5C <- as.factor(data_all$R5C)

# Relationship between LFHF volume and age
# Assumes that the relationship is same for all covariates (Gender)
model1 <- lm(Left.Hippocampus ~ scaled_Age_from_MR_Screen, data = data_all)
summary(model1)

# Linear model extension (Multiple Regression)
# Separate intercept for each gender
# Assumes that LFHF volume decrease by age is consistent, but the volume is different between male and female in the irst place
# What would the association between HF volume and age when there were NO DIFFERENCES among other variables
model2 <- lm(Left.Hippocampus ~ Age_from_MR_Screen*R5CPM, data = data_all)
summary(model2)

#install.packages("jtools")
#library("jtools")

interact_plot(model2, 
              pred = "Age_from_MR_Screen", 
              modx="R5CPM", 
              modxvals = "plus-minus", 
              plot.points=TRUE,
              legend.main = "Early Recovery from POS",
              color.class = "Oranges")



#compare two models using F-test 
anova(model1, model2)

# Allow Volume reduction rate to vary by gender
model3 <- lm(Left.Hippocampus ~ scaled_Age_from_MR_Screen + R5PGENDER + scaled_Age_from_MR_Screen:R5PGENDER, data=data_all)
summary(model3)

# Feature Engineering for a new categorical variable (Age Group)
old <- data_all[which(data_all$R5PAGE >= 49),]
old_data <- data.frame(ageGroup = rep("older", nrow(old)), old[,])
young <- data_all[which(data_all$R5PAGE < 49),]
young_data <- data.frame(ageGroup = rep("younger", nrow(young)), young[,])

# combine new data sets
data <- rbind(old_data, young_data)

# Cast categorical "Factor"
data$ageGroup <- as.factor(data$ageGroup)

library(ggplot2)
theme_update(plot.title = element_text(hjust = 0.5))
ggplot(data, aes(x= ageGroup, y= Right.Hippocampus)) +
  geom_bar(position=position_dodge(), stat="identity") + 
  #geom_errorbar(aes(ymin=Left.Hippocampus-se, ymax=Left.Hippocampus+se), width=.2, position=position_dodge(.9))
  facet_wrap(~R5PGENDER) + # This is where PWB would go 
  xlab("Age_Group") + 
  ylab("Left_Hippocampal_Volume(mm)") + 
  ggtitle("Left Hippocampal Volume by Age", subtitle=NULL)


cor_value = cor(data_all$Left.Amygdala, data_all$RPAGE)

library(ggplot2)
theme_update(plot.title = element_text(hjust = 0.5))
ggplot(data_all, aes(x= R5PAGE, y= Left.Amygdala, color=Gender, shape=Gender, size=NULL)) +
  geom_point() + 
  xlab("Age(years)") + 
  ylab("Volume") + 
  geom_smooth(method=lm, se=FALSE, level=0.95) +
  ggtitle("Left Amygdala Volume by Age", subtitle=NULL) +
  annotate("text", label="Wow what a brain", x=60, y=2100) +
  geom_hline(yintercept=mean(data_all$Left.Amygdala)) +
  annotate("text", label="Mean Left.AMG Volume", x=65, y=mean(data_all$Left.Amygdala)-25) +
  geom_vline(xintercept=mean(data_all$R5PAGE)) +
  annotate("text", label="Mean Age", y=1000, x=mean(data_all$R5PAGE)+5) +
  annotate("text", label=paste("R = ", cor_value), x=70, y=1000)
  #theme(panel.background=element_blank(), legend.key=element_blank()) +
  #scale_color_discrete(name="gender") +
  #labs(shape="gender", color="gender")



t.test(Left.Hippocampus ~ R5PGENDER, data=data_all)
