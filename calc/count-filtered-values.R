#install tidyverse
if (!require("tidyverse")) install.packages("tidyverse")
library("tidyverse")

df <- read_csv('fieldmapping.csv')

df[grepl("account", df$sf_object),]