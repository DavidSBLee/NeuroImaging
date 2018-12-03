###Load MIDUSREF Dataset
data <- read.csv("/Users/SB/Desktop/ref_anon.csv", header=TRUE)

### Data Type Manipulation
# Check datatype
str(data$RA5CPL)

# Convert data type to numbers
data$rest_percent <- as.numeric(as.character(data$rest_percent), na.rm=TRUE)

### corrleation
# Linear Regression
lm.model <- lm(RA1PRAGE ~ RA5CPL, data = data)
summary(lm.model)

# Bivarite Association (Two quantitative variables)
library(ggplot2)
theme_update(plot.title = element_text(hjust = 0.5))
ggplot(data, aes(x= RA1PRAGE, y= RA5CPL)) +
  geom_point(shape=19) + 
  xlab("Age") + 
  ylab("Late Recovery Positive Pictures") + geom_smooth(method=lm, se=FALSE) +
  ggtitle("Positivity Picture Late Recovery by Age", subtitle=NULL)

cor.test(data$RA1PRAGE, data$RA5NEPC)

### Feature Engineering
# How many unique values?
length(unique(as.numeric(data$RA5NEPC)))

# Create a new dataframe with "age_group" column with row #s that match original dataframe
#age.group <- data.frame(age_group = rep("None", nrow(data)))

# Distribution of variable
boxplot(data$RA5CPL, horizontal = TRUE, outline=FALSE)
boxplot.stats(data$RA5CPL)
hist(data$RA5CPL)
mean(data$RA5NEPC3, na.rm=TRUE)

# Feature Engineering for a new Categorical Variable (Corrugator Reactivity to Neg Stimuli)
high_neg <- data[which(data$RA5CNE > 0.95),]
high_neg_data <- data.frame(corr_neg = rep("high_neg", nrow(high_neg)), high_neg[,])
#med_neg <- data[which(data$RA5CNE > 0.5 & data$RA5CNE < 1.3),]
#med_neg_data <- data.frame(corr_neg = rep("med_neg", nrow(med_neg)), med_neg[,])
low_neg <- data[which(data$RA5CNE <= 0.95),]
low_neg_data <- data.frame(corr_neg = rep("low_neg", nrow(low_neg)), low_neg[,])

data.combined <- rbind(high_neg_data, low_neg_data)
data.combined$corr_neg <- as.factor(data.combined$corr_neg)


# write to csv
write.table(data.combined, "/Users/SB/Desktop/corr_neg.csv", row.names=FALSE, sep=",")

# Feature Engineering for a new categorical variable (Age Group)
old <- data.combined[which(data.combined$RA1PRAGE >= 65),]
old_data <- data.frame(ageGroup = rep("older", nrow(old)), old[,])
middle <- data.combined[which(data.combined$RA1PRAGE >= 45 & data.combined$RA1PRAGE <65),]
middle_data <- data.frame(ageGroup = rep("middle", nrow(middle)), middle[,])
young <- data.combined[which(data.combined$RA1PRAGE < 45),]
young_data <- data.frame(ageGroup = rep("younger", nrow(young)), young[,])

# combine new data sets
data.combined.again <- rbind(old_data, middle_data, young_data)

# Cast categorical "Factor"
data.combined.again$ageGroup <- as.factor(data.combined.again$ageGroup)

### Charts on single Categorical Variable ###
# Bar Charts
plot(data.combined$corr_neg)

#barplot(data.combined$corr_neg)
corr <- table(data.combined$corr_neg)
barplot(corr)
# Ordering by frequncy
barplot(corr[order(corr, decreasing=TRUE)])
# Customize the chart
par(oma = c(2, 2, 2, 2)) # set outside margins
par(mar = c(1, 5, 2, 1)) # set plot margins
barplot(corr[order(corr)],
        horiz = TRUE,
        las = 1, #las gives orientation of axis labels
        col = c("bisque1"),
        border = TRUE, #no borders on bars (N/A)
        main = "Frequencies of Corrugator Reactivity\n to Negative Pictures",
        xlab = "Strength of Corrugator Reactivity")

### Two-Sample T-Test(Between Group)(Most common inferential stats)

# Box Plot comparing two distributions
boxplot(RA5CPL ~ corr_neg, data=data.combined.again)
boxplot(RA1PRAGE ~ ageGroup, data=data.combined.again, outline=FALSE)

# Independant 2-group t-test
t.test(RA5CPL ~ RA1PRAGE, data=data.combined.again)

# t-test with options
t.test(RA5NEPC ~ ageGroup, 
       data=data.combined.again,
       alternative="less", # One tailed test
       conf.level = 0.80) # 80% CI (vs. 95%)

### Ways of removing outliers

# Remove outliers based on a varaible 
subdata <- subset(data.combined, RA5NEPC >35)
boxplot(subdata$RA5NEPC, horizontal = TRUE)
mean(subdata$RA5NEPC)

# Based on 25, 75% quartile criteria
remove_outliers <- function(x, na.rm = TRUE, ...) {
  qnt <- quantile(x, probs=c(.25, .75), na.rm = na.rm, ...)
  H <- 1.5 * IQR(x, na.rm = na.rm)
  y <- x
  y[x < (qnt[1] - H)] <- NA
  y[x > (qnt[2] + H)] <- NA
  y
}

boxplot(data.combined.again$RA5NEPC3)
data.combined.again$RA5NEPC3 <- remove_outliers(data.combined.again$RA5NEPC3)
boxplot(data.combined.again$RA5NEPC3)

# Based on a package
#install.packages("outliers")
library("outliers")
rm.outlier(data.combined.again$RA5NEPC3, fill = FALSE, median = FALSE, opposite = FALSE)

# Paired T-test (within subject, pre&post)

# Comparing means with a one-factor analysis of variance
# one-factor ANOVA (common measure in inferential stats)
# Conduct one-way ANOVA (multiple groups)
# Group Catgory in one column and values on the other
anova1 <- aov(RA5CPL ~ RA1PRAGE, data = data.combined)
summary(anova1)

# check how many levels are in one categorical variable
levels(data.combined$corr_neg)

# Summary descriptive statistics
library("dplyr")
group_by(data.combined, corr_neg) %>%
  summarise(
    count=n(),
    mean = mean(RA5NEPC3, na.rm =TRUE),
    sd = sd(RA5NEPC3, na.rm=TRUE)
  )

# More sophisticated box plot
#install.packages("ggpubr")
library("ggpubr")
ggboxplot(data.combined.again, x = "ageGroup", y = "RA5CPE",
       color = "ageGroup", pallette = c("#00AFBB", "#E7B800"),# "#FC4E07"),
       order = c("older", "younger"),
       ylab = "Corr Late Recovery Pos", xlab = "age",
       outlier.shape = NA)

# Post-hoc comparisons
#install.packages("TukeyC")
#install.packages("doBy")
library(doBy)
library(TukeyC)

TukeyHSD(anova1)
#pairwise.t.test(anova1)
#p.adjust(anova1)

### Cross Tabs for more than two categorical variables
### Computing robust statistics bivariate asscociations
### In case of bevariate ouliers ,a quntile regression can be much more effective
### as it does not get influenced by outliers
install.packages("quantreg")
#install.packages("robust")
#install.packages("robustbase")
#install.packages("MASS")
library(quantreg)
data(engel)
attach(engel) # remember to detach it at the end

# Create empty plot
plot(income, 
     foodexp,
     xlab = "income",
     ylab = "food expeniture",
     type = "n",
     cex = .5)
# Points in plot
points(income,
       foodexp,
       pch = 16, 
       col = "lightgray")
# Specify the quantiles
taus <- c(.05, .1, .25, .75, .9, .95)
# X value sequence (Divide into 100 pieces)
xx <- seq(min(income), max(income), 100)
# Coefficients (rq= regression quantile)
f <- coef(rq((foodexp)~(income), tau=taus))
# Y values (use x and f to calculate expected Y)
yy <- cbind(1, xx)%*%f

for(i in 1:length(taus)){
  lines(xx, yy[, i], col="darkgray")
}

# draw two regrssion lines
# lm for linear model
# Standard LS REGRSSION
abline(lm(foodexp ~ income),
       col = "darkred",
       lwd =2) # lwd == pixel thickness or line width

# Median LS Regression
abline(rq(foodexp ~ income),
       col = "blue",
       lwd = 2)
#add legend
legend(3000, 1000, # location
       c("mean fit", "median fit"),
       col = c("darkred", "blue"),
       lty = 1, # lty 1 == solid lines
       lwd = 2)

### Multivariate Charts

### Clusterd Bar Chart for Means
# Associateion between two categorical predictor variables 
# and a single quantitative outcome (mean)
# This won't work
barplot(free_recall_total ~ ageGroup*corr_neg, data = data.combined.again)

# Making a dataframe with mean Free Recall for each category
# na.rm == exclude n/a (missing data)
mean_data <- tapply(data.combined.again$free_recall_total,
                    list(data.combined.again$corr_neg,
                         data.combined.again$ageGroup),
                    mean, na.rm=TRUE)

barplot(mean_data,
        beside =TRUE,
        col = c("steelblue3", "thistle3"),
        bor = NA,
        main = "Total Free Recall by AgeGroup and Corr_Reac_to_Neg",
        xlab = "Age Group",
        ylab = "Total mean FREE RECALL")

legend(locator(1), # locator(1) == interactive lets you click
       rownames(mean_data),
       fill = c("steelblue3", "thistle3"))

### Scatter Plots for mixed-type multiple variables
# Relationship betweeen categorical and quantitative variables
# 1 categorical and 2 quantitative
require(car) # remember to detach later
# Chart total free recall as a function of total correct cube&paper broken down by ageGroup
sp(free_recall_total ~ cb_total | ageGroup,
   data = data.combined,
   xlab = "total correct cube&paper",
   ylab = "total free recall",
   main = "free recall by cube&paper in each agegroup",
   labels = row.names(data.combined))

detach("package:car", unload=TRUE)


### Scatter plot matrix
#Scatter Plot of multiple quntitative variables
# Several Quantitative variables

# using column #s
pairs(data.combined[13:18])

# Bringin color pastel
require("RColorBrewer")
display.brewer.pal(5, "Pastel1")

# Function for putting historgarm in diagnal
panel.hist <- function(x, ...)
{
  usr <- par("usr"); on.exit(par(usr))
  par(usr = c(usr[1:2], 0, 1.5) )
  h <- hist(x, plot = FALSE)
  breaks <- h$breaks; nB <- length(breaks)
  y <- h$counts; y <- y/max(y)
  rect(breaks[-nB], 0, breaks[-1], y,  ...)
  # Removed "col = "cyan" from code block; original below
  # rect(breaks[-nB], 0, breaks[-1], y, col = "cyan", ...) 
}

pairs(data.combined[13:18], 
      panel = panel.smooth,  # Optional smoother through each SP
      main = "Scatterplot Matrix for MIDUSREF Using pairs Function",
      diag.panel = panel.hist, 
      pch = 16, 
      col = brewer.pal(5, "Pastel1")[unclass(data.combined$ageGroup)])

# Similar with "car" package
# Gives kernal density and rugplot for each variable
library(car)
scatterplotMatrix(~Petal.Length + Petal.Width + Sepal.Length + Sepal.Width | Species,
                  data = iris,
                  col = brewer.pal(3, "Dark2"),
                  main="Scatterplot Matrix for Iris Data Using \"car\" Package")

# Clean up
palette("default")  # Return to default
detach("package:RColorBrewer", unload = TRUE)
detach("package:car", unload=TRUE)
rm(list = ls())

### 3-Dimensional Scatter Plots
require("scatterplot3d")
install.packages("scatterplot3d")

# Plot 3 quantitative variables in a 3D space
scatterplot3d(data[7:9])

# Add coloring and vertical lines that connect to the floor
s3d <- scatterplot3d(data[7:9],
                     pch = 16,
                     highlight.3d = TRUE,
                     type = 'h',
                     main = "3D Scatterplot")
# Add regression plane
# Predict RA5PHM(Age based on Height and BMI)
plane <- lm(data.combined.again$RA1PRAGE ~ data.combined.again$RA5CPL + data.combined.again$RA5CNE)
s3d$plane3d(plane)

# Spinning 3D scatterplot
# install and load the "rgl" pacakge ("3D visualization device system(openGL)")
# Note: does NOT work in Rstudio, run it on console version of R
# Spinning 3D scatterplot
# install and load the "rgl" pacakge ("3D visualization device system(openGL)")
# Note: does NOT work in Rstudio, run it on console version of R
install.packages("rgl")
require("rgl")
#require("RColorBrewer")
plot3d(data$RA5PHC,
       data$RA5PHM,
       data$RA5PB,
       xlab = "age",
       ylab = "Weight",
       zlab = "BMI",
       col = brewer.pal(3, "Dark2"[unclass(data$RA5PHM)]))

# clean u p
deatch("package:rgl", unload = TRUE)
detach("package:RColorBrewer", unload = TRUE)
rm(list = ls())


### Multiple Regression
# Several variables are used collectively to predict scores on a single outcome variable, 
# a quantitative  usually (age)
reg1 <- lm(RA1PRAGE ~ RA5D + RA5FR,
           data = data.combined)
reg1
summary(reg1)

# Other information
anova(reg1)
coef(reg1)
confint(reg1)
resid(reg1)
hist(residuals(reg1))

# regression backwards, 
regb <- step(reg1,
             direction= "backward",
             trace = 0) # don't pring every steps

summary(regb)

# minimal model
reg0 <- lm(cb_total ~ 1, data=data.combined)
reg0
regf <- step(reg0,
             direction = "forward",
             scope = (~ cb_total),
                      data = data.combined,
                      trac = 0)
regf
