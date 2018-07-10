# Read in BMI and other Basic variables
bmi = read.csv("/Users/SB/Desktop/ref_bmi.csv", header=TRUE, sep=",", na.strings="NA")
names(bmi)
bmi <- bmi[c(1,2,8:14)]

# Read in MIDUSREF MRID and Group
ref <- read.csv("/Users/SB/Desktop/ref.csv", header=TRUE, sep=",", na.strings="NA")
colnames(ref)
ref <- ref[c(2,9)]

# Read in FreeSurfer Extracted Values
lh_desikan_thickness <- read.table("/Users/SB/Desktop/2018-05-02-aparc-lh-thickness-table.csv", header=TRUE, sep=",", na.strings="NA")
rh_desikan_thickness <- read.table("/Users/SB/Desktop/2018-05-02-aparc-rh-thickness-table.csv", header=TRUE, sep=",", na.strings="NA")
aseg_volume <- read.table("/Users/SB/Desktop/2018-05-02-aseg-volume-table.csv", header=TRUE, sep=",", na.strings="NA")

data_merged <- full_join(bmi, ref, by=c('ID','ID'))
data_merged <- full_join(data_merged, rh_desikan_thickness, by=c('ID','ID'))
data_merged <- full_join(data_merged, lh_desikan_thickness, by=c('ID','ID'))
data_merged <- full_join(data_merged, aseg_volume, by=c('ID', 'ID'))
colnames(data_merged)

# Exclude subject with missing values
data_subset <- subset(data_merged, BMI != "NA" & MaskVol != "NA") # & filter == 1)
# or
#data = na.omit(dat_merged)
colnames(data_subset)

# Extract All Column Names of interest
#thickness_measures <- grep("*thickness*", names(data))
#thickness_measures <- data[c(thickness_measures)]
data <- data_subset[c(1:4, 9:80, 126, 136, 146)]
colnames(data)

# Age distribution
hist(data$Age_from_Screen)

# BMI Distribution
hist(data$Age_from_Screen, 
     main="Age Distributions in MIDUSREF n=126",
     cex = 2.0,
     xlab="Age",
     ylab="Number of People",
     cex.lab = 1.2,
     col="orange",
     #xlim=c(20,80),
     #las=1, 
     breaks=10)

ggplot(data, aes(x=Age_from_Screen, color=Gender,fill=Gender)) + 
  geom_histogram(binwidth=3) +#,color="red", fill="orange")
  labs(title="Age Distribution in MIDUSREF (n=126)", x="Age", y = "Number of People")  +
  theme(plot.title = element_text(hjust = 0.5, size=20))


# Give some colors based on BMI range
h <- hist(data$BMI, breaks=15)
cuts <- cut(h$breaks, c(0, 18.49, 18.50, 24.99, 50))
#plot(h, col=cuts)
plot(h, xlab = "BMI", 
     ylab = "Number of People",
     cex.lab = 1.2, # for axes,
     #xlim = c(18, 47),
     main="BMI Distributions in MIDUSREF (n=126)",
     cex = 2.0, # for title
     col=c("yellow", "darkred","red", "darkred")[cuts])

legend(35, 18, 
       legend = c("Underweight (<18.50)", "Normal (18.50 - 25.00)", "Overweight ( >25.00)"), 
       fill = c("yellow", "red", "darkred"),
       cex = 0.9,
       text.font = 2,
       bty = "n")
    
       
# ROI x BMI
model0 <- lm(lh_posteriorcingulate_thickness ~ BMI, data)
summary(model0)

# ROI x Age
model1 <- lm(lh_posteriorcingulate_thickness ~ Age_from_Screen, data)
summary(model1)

# ROI x BMI + Age
model2 <- lm(lh_posteriorcingulate_thickness ~ BMI +
               Age_from_Screen, data)
summary(model2)

# ROI x BMI + Age + ETIV
model3 <- lm(lh_posteriorcingulate_thickness ~ BMI +
               Age_from_Screen + EstimatedTotalIntraCranialVol, data)
summary(model3)

# ROI x BMI + Age + Total Brain Volume (TBV)
model4 <- lm(lh_posteriorcingulate_thickness ~ BMI +
               Age_from_Screen + BrainSegVol, data)
summary(model4)

# ROI x Age + Age + TBV + Gender + Sample
model5 <- lm(lh_posteriorcingulate_thickness ~ BMI + 
               Age_from_Screen + 
               BrainSegVol +
               Gender +
               GRP, data=data)
summary(model5)



# Get rid of scientific notation
options(scipen=999)
# Set how many digits you want to view in numerical values
options(digits=9)

# model
fit <- lm(TotalGrayVol ~ BMI, data)
data$predicted <- predict(fit)
data$residuals <- residuals(fit)

# Compute Pearson R and P-value
cor_value = cor(data$BMI, data$TotalGrayVol)
p_value = cor.test(data$BMI, data$TotalGrayVol)$p.value
# Keep trailing zeros
cor_value = sprintf("%.2f", round(cor_value,2)) 
p_value = sprintf("%.3f", round(p_value,3))


library(ggplot2)

ggplot(data, aes(x=BMI , y=TotalGrayVol)) + #, colour=Gender)) +
  geom_point(aes(color=Gender)) +
  stat_smooth(method=lm, se=FALSE) + #, col="black") +
  annotate("text", label=paste("r = ", cor_value, "p = ", p_value), x=40, y=450000) +
  xlab("BMI") +
  ylab("Volume (cm3)") +
  ggtitle("Total Gray Matter Volume X BMI in MIDUSREF (n=126)") + 
  theme(plot.title = element_text(hjust = 0.5, size=20)) +
  geom_point(aes(y=predicted), shape = 1) +
  geom_segment(aes(xend = BMI, yend = predicted), alpha = 0.2) +
  geom_point(aes(alpha = abs(residuals), size = abs(residuals))) +
  #scale_color_continuous(low= "black", high = 'red') +
  theme_bw()


#install.packages("ggpubr")
library(ggpubr)
ggscatter(data, x = "BMI", y = "lh_parsopercularis_thickness",
          add = "reg.line", conf.int = TRUE,
          cor.coef = TRUE, cor.method = "pearson",
          xlab = "BMI", ylab = "lh_superiorfrontal_thickness")

# Multipe Regression
fit2 <- lm(TotalGrayVol ~ BMI + Age_from_Screen, data)
summary(fit2)
data$predicted <- predict(fit2)
data$residuals <- residuals(fit2)

# Plot for one predictor
ggplot(data, aes(x= BMI, y = TotalGrayVol)) +
  geom_segment(aes(xend = BMI, yend = predicted), alpha = .2) +
  geom_point()+
  geom_point(aes(y = predicted), shape=1) +
  theme_bw()

# Plot multiple predictors
# "gather()" from tidyr
# "facet_*() from ggplot
library(tidyr)
data %>%
  gather(key = "iv", value = "x", -TotalGrayVol, -predicted, -residuals) %>%
  ggplot(aes(x = x, y = TotalGrayVol)) +
  geom_segment(aes(xend = x, yend = predicted), alpha = .2) +
  geom_point(aes(color = residuals)) +
  scale_color_gradient2(low = "blue", mid = "white", high = "red") +
  geom_point(aes(y=predictted), shape=1) +
  facet_grid(~ iv, scales = "free") +
  theme_bw
# Some Extra Code

x <- data[5]
y <- data[3:79]

y$Gender <- as.numeric(as.factor(y$Gender))
y$GRP <- as.numeric(y$GRP)

r <- cor(x, y)
frame_r <- data.frame(r)
final_r <- t(frame_r)

write.csv(final_r, "/Users/SB/Desktop/output.csv", sep=",")

#install.packages("Hmisc")
#library(Hmisc)
#cor <-rcorr(as.matrix(data_interest), type="pearson")
#cor$r
#cor$P

cor.test(data$Age_from_Screen, data$lh_medialorbitofrontal_thickness)#$p.value
cor.test(data$BMI, data$TotalGrayVol)
cor.test(data$Age_from_Screen, data$lh_lateraloccipital_thickness)


#data_interest <- data[6:84]
#apply(data_interest[, -1], 2, cor.test, data_interest$BMI, method="pearson")

#vector <- list("rh_caudalanteriorcingulate_thickness",
           #"rh_frontalpole_thickness",
           #"lh_parsopercularis_thickness",
           #"rh_parstriangularis_thickness",
           #"lh_medialorbitofrontal_thickness",
           #"lh_rostralmiddlefrontal_thickness",
           #"rh_lingual_thickness",
           #"lh_parstriangularis_thickness",
           #"lh_superiorfrontal_thickness",
           #"lh_parsorbitalis_thickness",
           #"lh_caudalmiddlefrontal_thickness",
           #"rh_bankssts_thickness",
           #"lh_frontalpole_thickness",
           #"rh_inferiorparietal_thickness",
           #"rh_rostralanteriorcingulate_thickness")

#for (i in 1:15){
  #test <- as.character(vector[i])
  #print (test)
  #cor.test(data$BMI, data$test))
#}
