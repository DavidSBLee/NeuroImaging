# Read in BMI and other Basic variables
age = read.csv("/Users/SB/Desktop/demean_age_ref.csv", header=TRUE, sep=",", na.strings="NA")
names(age)
age <- age[c(1,4,5)]

# Read in FreeSurfer Extracted Values
lh_vmpfc <- read.table("/Users/SB/Desktop/119_left_vmPFC.txt", header=TRUE, sep=",", na.strings="NA")
rh_vmpfc <- read.table("/Users/SB/Desktop/119_right_vmPFC.txt", header=TRUE, sep=",", na.strings="NA")
lh_vlpfc <- read.table("/Users/SB/Desktop/119_left_vlPFC.txt", header=TRUE, sep=",", na.strings="NA")
rh_vlpfc <- read.table("/Users/SB/Desktop/119_right_vlPFC.txt", header=TRUE, sep=",", na.strings="NA")

data <- cbind(age, lh_vmpfc, rh_vmpfc, lh_vlpfc, rh_vlpfc)
class(data$gender)
data$gender <- as.factor(data$gender)
colnames(data)

# Age distribution
hist(data$age)
  
# ROI x Age
model1 <- lm(rh_vmpfc_activity ~ age, data)
summary(model1)

# Compute Pearson R and P-value
cor_value = cor(data$age, data$lh_vmpfc_activity)
p_value = cor.test(data$age, data$lh_vmpfc_activity)$p.value
# Keep trailing zeros
cor_value = sprintf("%.2f", round(cor_value,2)) 
p_value = sprintf("%.3f", round(p_value,3))


library(ggplot2)

ggplot(data, aes(x=age , y=lh_vmpfc_activity)) + #, colour=Gender)) +
  geom_point(aes(color = gender)) +
  stat_smooth(method=lm, se=FALSE) + #, col="black") +
  annotate("text", label=paste("r = ", cor_value, "p = ", p_value), x=70, y=0) +
  xlab("Age") +
  ylab("Activity (POS-NEU)") +
  ggtitle("Left vmPFC activity During Positive Picture Viewing(n=119)") + 
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5, size =20)) 

# Compute Pearson R and P-value
cor_value = cor(data$age, data$lh_vlpfc_activity)
p_value = cor.test(data$age, data$lh_vlpfc_activity)$p.value
# Keep trailing zeros
cor_value = sprintf("%.2f", round(cor_value,2)) 
p_value = sprintf("%.3f", round(p_value,3))


library(ggplot2)

ggplot(data, aes(x=age , y=lh_vlpfc_activity)) + #, colour=Gender)) +
  geom_point(aes(color = gender)) +
  stat_smooth(method=lm, se=FALSE) + #, col="black") +
  annotate("text", label=paste("r = ", cor_value, "p = ", p_value), x=70, y=0) +
  xlab("Age") +
  ylab("Activity (POS-NEU)") +
  ggtitle("Left vlPFC activity During Positive Picture Viewing(n=119)") + 
  theme_bw() +
  theme(plot.title = element_text(hjust = 0.5, size =20)) 
  #geom_point(aes(y=predicted), shape = 1) +
  #geom_segment(aes(xend = BMI, yend = predicted), alpha = 0.2) +
  #geom_point(aes(alpha = abs(residuals), size = abs(residuals))) +
  #scale_color_continuous(low= "black", high = 'red') +


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
#