# Install DataExplorer package
if (!require("DataExplorer")) install.packages("DataExplorer")
library(DataExplorer)

data <- read.csv("DS4261-20240528.csv")

# Generate a comprehensive report
report <- create_report(data)

# Open the report in your web browser
browseURL(report$report_file)