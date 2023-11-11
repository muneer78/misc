from pdf2docx import Converter
pdf_file = 'pdf_file.pdf'
docx_file = 'docx_file.docx'
cv = Converter(pdf_file)
cv.convert(docx_file)
cv.close