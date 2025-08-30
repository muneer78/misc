import csv
import re


def remove_special_chars(text):
    """Removes special characters from a given text."""
    return re.sub(r"[^\w\s]", "", text)


def process_csv(csv_file):
    """
    Reads a CSV file, creates .md files based on its content, removing special characters from filenames.

    Args:
      csv_file: Path to the CSV file.
    """

    with open(csv_file, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            filename = remove_special_chars(row["Node_article_Title"]) + ".md"
            file_text = row["IMG_Alt"]

            with open(filename, "w") as md_file:
                md_file.write(file_text)


if __name__ == "__main__":
    csv_file = "article2.csv"  # Replace with your CSV file path
    process_csv(csv_file)
