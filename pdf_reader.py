import PyPDF2
import pathlib


filename = 'C:\projectPython\data\eletrica\iren\Fattura Iren 1515244_es.pdf'

if pathlib.Path(filename).is_file() == False:    
    print('File non valido')

pdf_read = open (filename,'rb')
pdf_read_start = PyPDF2.PdfFileReader(pdf_read)

print('Numero di pagine',pdf_read_start.getNumPages())
print('Informazioni Documento',pdf_read_start.getDocumentInfo())






