import csv


def clean_tags(tags):
    """Removes dashes and extra whitespace from tags.

    Args:
      tags: A string of tags separated by commas.

    Returns:
      A cleaned string of tags.
    """

    cleaned_tags = tags.replace("-", "")  # Remove dashes
    cleaned_tags = [
        tag.strip() for tag in cleaned_tags.split(",")
    ]  # Split into list, remove whitespace
    if len(cleaned_tags) > 1:
        return ", ".join(cleaned_tags)  # Join with commas and spaces if multiple tags
    else:
        return cleaned_tags[0]  # Return single tag without quotes


def process_csv(input_file, output_file):
    """Processes a CSV file, cleaning up the 'tags' column.

    Args:
      input_file: The path to the input CSV file.
      output_file: The path to the output CSV file.
    """

    with open(input_file, "r") as in_csv, open(output_file, "w", newline="") as out_csv:
        reader = csv.DictReader(in_csv)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(out_csv, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            row["tags"] = clean_tags(row["tags"])
            writer.writerow(row)


# Example usage:
input_csv_file = "metadata.csv"
output_csv_file = "finalmeta.csv"
process_csv(input_csv_file, output_csv_file)
