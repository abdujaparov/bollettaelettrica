import PyPDF2
import pathlib
import string
import re
from bolletta import BollettaLuceIren


def __getFornitura(fp):
    fornitura=''
    stringa_fornitura = 'Contratto Numero'
    pos=fp.find(stringa_fornitura)
    fornitura=fp[pos+len(stringa_fornitura):pos+24]
    return fornitura

def __getPod(fp):
    pod=''
    stringa_pod='Codice POD'
    pos=fp.find(stringa_pod)
    pod=fp[pos+len(stringa_pod):pos+24]
    return pod

def __getPeriodo(fp):
    periodo=''
    stringa_periodo='PERIODO'
    stringa_fattura='Fattura'
    posPeriodo=fp.find(stringa_periodo)
    posFattura=fp.find(stringa_fattura)
    periodo=fp[posPeriodo+len(stringa_periodo):posFattura]
    return periodo

def __getConsumoAnnuo(fp,fascia):
    regExpString = r"Consumo dal [0-9]{2}/[0-9]{2}/[0-9]{4} al [0-9]{2}/[0-9]{2}/[0-9]{4}.*non distinto perfasce.*COSTO"

    subFp = fp[fp.find('Consumo dal'):len(fp)]    
    matched = re.match(regExpString,subFp)
    posFinale = matched.end()
    tuttiDati = matched.group()

    value = ''

    if fascia != 'ALL':
        temp = tuttiDati[tuttiDati.find(fascia):len(tuttiDati)]
        value = temp[len(fascia):temp.find('Consumo')] 
    else:
        temp = tuttiDati[tuttiDati.find('perfasce'):len(tuttiDati)]
        value = temp[len('perfasce'):temp.find('COSTO')]

    
    return float(value.split()[0])

def __getFattura(fp):
    stringaFattura = 'Fattura n.'
    subFp=fp[fp.find(stringaFattura):len(fp)]
    posDel=subFp.find('del')
    return [subFp[len(stringaFattura):posDel],subFp[subFp.find('del')+len('del')+1:subFp.find('Per')]]

def __getCostoTotale(fp):
    totaleDaPagareStr='Totale da pagare Euro'
    scadenzaStr='Scadenza'
    subFp=fp[fp.find(totaleDaPagareStr)+len(totaleDaPagareStr):len(fp)]
    return float(subFp[0:subFp.find(scadenzaStr)].replace(',','.'))


#filename = 'C:\projectPython\data\eletrica\iren\Fattura Iren 1515244_es.pdf'
filename = 'C:\projectPython\data\eletrica\iren\Fattura Iren 1374175_es.pdf'

if pathlib.Path(filename).is_file() == False:    
    print('File non valido')

pdf_read = open (filename,'rb')
pdf_read_start = PyPDF2.PdfFileReader(pdf_read)

page0=''

if(pdf_read_start.getNumPages() > 0):
    pageObj = pdf_read_start.getPage(0)
    page0=pageObj.extractText()


print('Dalla pagina numero: ',pdf_read_start.getPageNumber(pdf_read_start.getPage(0))+1)
bolletta=BollettaLuceIren(__getFattura(page0)[0],__getPod(page0),__getFornitura(page0),__getCostoTotale(page0))
bolletta.consumiFasce['F1']=__getConsumoAnnuo(page0,'F1')
bolletta.consumiFasce['F2']=__getConsumoAnnuo(page0,'F2')
bolletta.consumiFasce['F3']=__getConsumoAnnuo(page0,'F3')
#print(bolletta.tipo)
#print(bolletta.gestore)
#print(bolletta.consumoTotale())
print(bolletta.costoTotale)

testArr = [1,2,3,4]





pdf_read.close()



