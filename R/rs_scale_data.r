data <- read.csv("/home/slee/Desktop/ref_anon.csv", header=TRUE)
goodData <- read.csv("/home/slee/Desktop/MIDUSREF_Good_Resting_subID_5minutes.txt", header=FALSE)

# Merge data by subjects of interest
data.merged <- merge(data, goodData, by.x = 'MRID', by.y = 'V1')

# Mean Centering Continous Variable and adding as a column
scaledAge <- scale(data.merged$RA1PRAGE, center = TRUE, scale = FALSE)
goodData["scaeld_age"] <- scaledAge
colnames(goodData)[1] <- "MRID"

# Check mean-centered (output should be 0)
mean(goodData$scaeld_age)

# write to csv
write.table(goodData, "/home/slee/Desktop/MIDUSREF_rest_scaled_age.csv", row.names=FALSE, sep=",")

# Extract age 
rest_data <- read.csv("/home/slee/Desktop/midusref_rest_left_amygdala.csv", header=TRUE)
interest <- data.merged$RA1PRAGE
rest_data["age"] <- interest

# Extract corrugator
interest <- data.merged$RA5CNL
rest_data["RA5CNL"] <- interest

# Check datatype and covert to numeric values
str(rest_data$RA5CNL)
rest_data$RA5CNL <- as.numeric(as.character(rest_data$RA5CNL), na.rm=TRUE)

# Compute correlation for all variations
wonderful <- cor(rest_data)
df <- data.frame(wonderful)


#extract last row and transpose the dataframe
corr <- df[ c(238), ]
age_TR <- t(corr)
age_TR <- as.data.frame(age_TR)


cor.test(rest_data$average, rest_data$RA5CNL)

lm.model <- lm(X236 ~ age, data = rest_data)
summary(lm.model)
