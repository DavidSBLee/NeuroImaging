data <- read.csv("/Users/SB/Desktop/freesurfer_with_pwb.csv", header=TRUE)

model1 <- lm(Left.Hippocampus ~ R5PAGE + PWB_Average + PWB_Autonomy_7 + PWB_EnvMastery_7 + PWB_PersonalGrowth_7 +
               PWB_PosRelationsOthers_7 + PWB_PurposeLife_7 + PWB_SelfAcceptance_7, data=data)
summary(model1)

model2 <- lm(Left.Hippocampus ~  scaeld_age , data=data)
summary(model2)

summ(model2, scale=TRUE)

# Test Interaction Model
# Does the effects of Age on Left Hippocampal Volume depend on PWB Average Values
model3 <- lm(Left.Hippocampus ~  scaled_PWB_Average, data=data)
summary(model3)

data$SAMPLMAJ <- as.factor(data$SAMPLMAJ)
data$R5PGENDER <- as.factor(data$R5PGENDER)
data$PWB_EnvMastery_7 <- as.numeric(data$PWB_EnvMastery_7)

str(data$SAMPLMAJ)

colnames(data)
names(data)

# When Error in Plot
par("mar")
par(mar=c(1,1,1,1))

cor_coef = round(cor(data$scaeld_age, data$EstimatedTotalIntraCranialVol),2)
cor_coef

cor(data$PWB_EnvMastery7, data$scaeld_age, use="pairwise.complete.obs")

getOption("na.action")
str(data$PWB_EnvMastery_7)
str(data$scaled_age)
library(ggplot2)
theme_update(plot.title = element_text(hjust = 0.5))
ggplot(data, aes(x=scaled_PWB_Average, y=Left.Hippocampus, colour=SAMPLMAJ)) +
  geom_point(shape=19, size=1) + 
  xlab("Age") + 
  ylab("Left HF Volume") + geom_smooth(method=lm, se=FALSE) +
  ggtitle("Left HF Volume by Age", subtitle=NULL) +
  stat_fit_glance(method = 'lm',
                  method.args = list(formula = formula),
                  geom = 'text',
                  aes(label = paste("P-value = ", signif(..p.value.., digits = 4), sep = "")))
annotate(geom="text", x=1, y=1, label=paste("R = ", cor_coef), colour="black", size=5, fontface="italic")

library(ggpubr)
library(magrittr)
sp <- ggscatter(data, x="scaeld_age", y="EstimatedTotalIntraCranialVol",
          add = "reg.line",
          add.params = list(color="blue", fill="lightgray"),
          conf.int= TRUE)

sp + stat_cor(method="pearson", label.x=10, label.y=100)


#install.packages("jtools")
library("jtools")
interact_plot(model3, pred = "scaeld_age", modx = "scaled_PWB_Average", modxvals = "plus-minus", plot.points=TRUE)
interact_plot(model3, pred = "PWB_Average", modx = "SAMPLMAJ", modxvals=NULL, plot.points=TRUE)
