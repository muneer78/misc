#install.packages("SmartEDA")
if (!require("SmartEDA")) install.packages("SmartEDA")
library("SmartEDA")

df <- read.csv("DS4261-20240528.csv")

# Overview of the data - Type = 1
ExpData(data=df,type=1)

# Structure of the data - Type = 2
ExpData(data=df,type=2)

# Metadata Information with additional statistics like mean, median and variance
ExpData(data=df,type=2, fun = c("mean", "median", "var"))
