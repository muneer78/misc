import os
import sys
import pypandoc


def convert_html_to_docx(html_file, output_path):
    pypandoc.convert_file(html_file, "docx", outputfile=output_path)


def main(input_folder):
    script_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

    html_files = [f for f in os.listdir(input_folder) if f.endswith(".html")]
    for html_file in html_files:
        input_path = os.path.join(input_folder, html_file)
        docx_file = os.path.splitext(html_file)[0] + ".docx"
        output_path = os.path.join(script_folder, docx_file)

        convert_html_to_docx(input_path, output_path)
        print(f"Converted {input_path} to {output_path}")


if __name__ == "__main__":
    script_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
    input_folder = script_folder
    main(input_folder)
