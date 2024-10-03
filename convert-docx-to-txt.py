import os
from docx import Document

def extract_text_from_docx(docx_file_path):
    doc = Document(docx_file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def write_to_text_file(text, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text)

def convert_docx_files_to_text(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".docx"):
            docx_file_path = os.path.join(input_dir, filename)
            output_text_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.txt")

            text = extract_text_from_docx(docx_file_path)
            write_to_text_file(text, output_text_file_path)

if __name__ == "__main__":
    # Set the input and output directories relative to the script's location
    script_directory = os.path.dirname(os.path.realpath(__file__))
    input_directory = script_directory  # Script's directory will be the input directory
    output_directory = script_directory  # Script's directory will be the output directory

    convert_docx_files_to_text(input_directory, output_directory)
