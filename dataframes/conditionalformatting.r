# Step 1: Read CSV
df <- read.csv("path/to/your/file.csv")

# Step 2: Determine the color for each row based on the percentiles of the 'total' column
percentiles <- quantile(df$total, probs = c(0.05, 0.25, 0.75))

df$row_color <- ifelse(df$total >= percentiles[3], "green",
                ifelse(df$total >= percentiles[2], "yellow",
                ifelse(df$total >= percentiles[1], "red", "black")))

# Step 3: Create a table grob with colored rows and export it to a PDF
library(ggplot2)
library(gridExtra)
library(grid)

# Convert the dataframe to a table grob without the row_color column
table_grob <- tableGrob(df[, -ncol(df)])

# Apply the row colors
for (i in 1:nrow(df)) {
  color <- df$row_color[i]
  table_grob$grobs[i + 1, ]$gp <- gpar(fill = color)
}

# Export the table grob to a PDF
pdf("colored_dataframe.pdf", height = nrow(df) / 2 + 1, width = ncol(df) + 2)
grid.draw(table_grob)
dev.off()
