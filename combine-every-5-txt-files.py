from docx import Document
import os


def combine_word_documents(files, group_size=5):
    # Get the current script's directory
    script_directory = os.path.dirname(os.path.realpath(__file__))

    # Split the list of files into groups of size 'group_size'
    file_groups = [files[i : i + group_size] for i in range(0, len(files), group_size)]

    for group_index, file_group in enumerate(file_groups, start=1):
        combined_document = Document()

        for count, file in enumerate(file_group, start=1):
            file_path = os.path.join(script_directory, file)

            # Read each Word document and append its content to the combined document
            sub_doc = Document(file_path)

            # Don't add a page break if it's the last file in the group
            if count < len(file_group):
                sub_doc.add_page_break()

            for element in sub_doc.element.body:
                combined_document.element.body.append(element)

        # Save the combined document to a new Word file
        combined_file_path = os.path.join(
            script_directory, f"combined_documents_{group_index}.txt"
        )
        combined_document.save(combined_file_path)


if __name__ == "__main__":
    # Get all Word files in the script's directory
    script_directory = os.path.dirname(os.path.realpath(__file__))
    files = [file for file in os.listdir(script_directory) if file.endswith(".txt")]

    combine_word_documents(files)
