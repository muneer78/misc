# from docx import Document
# import os
# from ebooklib import epub

# def combine_word_documents():
    # # Get the current script's directory
    # script_directory = os.path.dirname(os.path.realpath(__file__))

#     script_directory = '/Users/muneer78/Downloads/docs'
#     files = [file for file in os.listdir(script_directory) if file.endswith(".txt")]
#     files.sort()  # Optional: sort files alphabetically
#
#     combined_text = ""
#     for idx, file in enumerate(files):
#         file_path = os.path.join(script_directory, file)
#         with open(file_path, 'r', encoding='utf-8') as f:
#             combined_text += f.read()
#         if idx < len(files) - 1:
#             combined_text += "\n\n---\n\n"  # Markdown page break
#
#     # Write to Markdown file
#     md_path = os.path.join(script_directory, "combined.md")
#     with open(md_path, 'w', encoding='utf-8') as f:
#         f.write(combined_text)
#
#     # Write to EPUB file
#     book = epub.EpubBook()
#     book.set_identifier('id123456')
#     book.set_title('Combined Document')
#     book.set_language('en')
#     book.add_author('Author Name')
#
#     chapter = epub.EpubHtml(title='Combined', file_name='chap_1.xhtml', lang='en')
#     # Convert Markdown to HTML for EPUB
#     import markdown
#     chapter.content = markdown.markdown(combined_text, extensions=['extra'])
#     book.add_item(chapter)
#     book.toc = (epub.Link('chap_1.xhtml', 'Combined', 'chap_1'),)
#     book.add_item(epub.EpubNcx())
#     book.add_item(epub.EpubNav())
#     book.spine = ['nav', chapter]
#
#     epub_path = os.path.join(script_directory, "combined.epub")
#     epub.write_epub(epub_path, book, {})
#
#
# if __name__ == "__main__":
#     combine_txt_documents()

import os
from docx import Document
from ebooklib import epub

def para_to_html(para):
    # Map docx paragraph style to HTML
    style = para.style.name.lower()
    text = ""
    for run in para.runs:
        run_text = run.text.replace('\n', '<br/>')
        if run.bold:
            run_text = f"<b>{run_text}</b>"
        if run.italic:
            run_text = f"<i>{run_text}</i>"
        if run.underline:
            run_text = f"<u>{run_text}</u>"
        text += run_text

    if style.startswith('heading'):
        level = ''.join(filter(str.isdigit, style)) or "1"
        return f"<h{level}>{text}</h{level}>"
    elif style in ['list paragraph', 'bullet', 'number']:
        # Lists will be handled in the main loop
        return text
    else:
        return f"<p>{text}</p>"

def docx_to_html(doc):
    html = ""
    in_list = False
    list_type = None
    for para in doc.paragraphs:
        style = para.style.name.lower()
        if style in ['list paragraph', 'bullet', 'number']:
            if not in_list:
                list_type = 'ul' if 'bullet' in style else 'ol'
                html += f"<{list_type}>"
                in_list = True
            html += f"<li>{para_to_html(para)}</li>"
        else:
            if in_list:
                html += f"</{list_type}>"
                in_list = False
            html += para_to_html(para)
    if in_list:
        html += f"</{list_type}>"
    return html

def combine_docx_to_epub():
    script_directory = '/Users/muneer78/Downloads/docs'
    files = [file for file in os.listdir(script_directory) if file.endswith(".docx")]
    files.sort()

    combined_html = ""
    for idx, file in enumerate(files):
        file_path = os.path.join(script_directory, file)
        try:
            doc = Document(file_path)
        except Exception as e:
            print(f"Skipping {file}: {e}")
            continue
        combined_html += docx_to_html(doc)
        if idx < len(files) - 1:
            combined_html += '<hr style="page-break-after:always;">'

    book = epub.EpubBook()
    book.set_identifier('id123456')
    book.set_title('Combined Document')
    book.set_language('en')
    book.add_author('Author Name')

    chapter = epub.EpubHtml(title='Combined', file_name='chap_1.xhtml', lang='en')
    chapter.content = f"<html><body>{combined_html}</body></html>"
    book.add_item(chapter)
    book.toc = (epub.Link('chap_1.xhtml', 'Combined', 'chap_1'),)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav', chapter]

    epub_path = os.path.join(script_directory, "combined.epub")
    epub.write_epub(epub_path, book, {})

if __name__ == "__main__":
    combine_docx_to_epub()