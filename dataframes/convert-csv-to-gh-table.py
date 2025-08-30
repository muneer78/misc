import csv


def csv_to_markdown(csv_file, output_file):
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)

        # Generate the header row
        header = rows[0]
        markdown = "| " + " | ".join(header) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(header)) + " |\n"

        # Generate the rest of the rows
        for row in rows[1:]:
            markdown += "| " + " | ".join(row) + " |\n"

        # Export to a text file
        with open(output_file, "w", encoding="utf-8") as output:
            output.write(markdown)


# Example usage
csv_file = "/Users/muneer78/Downloads/tv.csv"  # Replace with your CSV file path
output_file = "/Users/muneer78/Downloads/output.md"  # The file where the markdown table will be saved
csv_to_markdown(csv_file, output_file)

print(f"Markdown table has been exported to {output_file}")
