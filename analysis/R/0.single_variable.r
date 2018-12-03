###Load MIDUSREF Dataset
data <- read.csv("/Users/SB/Desktop/ref_anon.csv", header=TRUE)

# Frequency Chart of a catgoroical variable
hand <- table(data$RA5C)
hand

# Pie Chart
pie(hand)
?pie

# Modify the pie chart
pie(hand[order(hand, decreasing = TRUE)],
    init.angle = 90,   # Starts as 12 o'clock instead of 3
    clockwise = TRUE,  # Default is FALSE
    col = c("plum1", "cadetblue2"), #, "lightpink", "lightcyan", "seashell", "papayawhip"),
    main = "Handedeness of MIDUSREF") # Title

# THE PROBLEM WITH PIE CHARTS
# Three data sets
pie.a <- c(22, 14, 18, 20, 14, 12)
pie.b <- c(20, 18, 16, 18, 16, 12)
pie.c <- c(12, 14, 20, 18, 14, 22)

# Changing graphical parameters for a minute
oldpar <- par()   # Stores old graphical parameters
par(mfrow    = c(1, 3),  # Num. rows/cols
    cex.main = 3)   #  Main title 3x bigger
colors <- c("grey98", "grey90", "lightskyblue", "lightgreen", "grey98", "grey90")
?colors

# Three pie charts side by side
# Is the green slice or blue slice bigger?
pie(pie.a, main = "Pie A", col = colors)
pie(pie.b, main = "Pie B", col = colors)
pie(pie.c, main = "Pie C", col = colors)


# Three bar charts side by side
# Is the green bar or blue bar bigger?
barplot(pie.a, main = "Bar A", col = colors)
barplot(pie.b, main = "Bar B", col = colors)
barplot(pie.c, main = "Bar C", col = colors)

par(oldpar)

rm(list = lm())  # Clean up
