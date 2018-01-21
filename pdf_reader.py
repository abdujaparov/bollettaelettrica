import PyPDF2
import pathlib


def __getFornitura(fp):
    fornitura=''

    return fornitura


filename = 'C:\projectPython\data\eletrica\iren\Fattura Iren 1515244_es.pdf'

if pathlib.Path(filename).is_file() == False:    
    print('File non valido')

pdf_read = open (filename,'rb')
pdf_read_start = PyPDF2.PdfFileReader(pdf_read)

page0=''

if(pdf_read_start.getNumPages() > 0):
    pageObj = pdf_read_start.getPage(0)
    page0=pageObj.extractText()

print('Lunghezza stringa pagina:\n',len(page0))
print('Pagina')
print(page0)
__getFornitura(page0)


pdf_read.close()



