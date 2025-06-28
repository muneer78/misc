from markitdown import MarkItDown

markitdown = MarkItDown()
result = markitdown.convert("/Users/muneer78/Downloads/convert/3-pandas-functions-for-dataframe-merging-by-cornellius-yudha-wijaya-aug-2023-towards-ai.pdf")

print(result.text_content)
# output_file = "/Users/muneer78/Downloads/convert/result.md"

# # Write the result to the Markdown file
# with open(output_file, "w", encoding="utf-8") as file:
#     file.write(result)

# print(f"Markdown file successfully written to {output_file}")