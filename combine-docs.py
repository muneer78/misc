from docx import Document
import os


def combine_word_documents():
    # Get the current script's directory
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Get all Word files in the script's directory
    files = [file for file in os.listdir(script_directory) if file.endswith(".txt")]

    # Create a combined document
    combined_document = Document()

    count, number_of_files = 0, len(files)

    for file in files:
        file_path = os.path.join(script_directory, file)

        # Read each Word document and append its content to the combined document
        sub_doc = Document(file_path)

        # Don't add a page break if you've reached the last file.
        if count < number_of_files - 1:
            sub_doc.add_page_break()

        for element in sub_doc.element.body:
            combined_document.element.body.append(element)

        count += 1

    # Save the combined document to a new Word file
    combined_file_path = os.path.join(script_directory, "bft.txt")
    combined_document.save(combined_file_path)


if __name__ == "__main__":
    combine_word_documents()
