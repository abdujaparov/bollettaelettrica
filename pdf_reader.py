import PyPDF2
import pathlib
import re
from bolletta import BollettaLuceIren


def __getFornitura(fp):
    
    stringa_fornitura = 'Contratto Numero'
    fornituraRegExp = stringa_fornitura+"[0-9]+"
    
    matched = re.search(fornituraRegExp, fp)
    return matched.group().replace(stringa_fornitura,'')
    


def __getPod(fp):

    stringa_pod='Codice POD'
    
    podRegExp = stringa_pod+"[A-Z0-9]{14}"
    matched = re.search(podRegExp, fp)

    return matched.group().replace(stringa_pod,'')

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
#    posFinale = matched.end()
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
    
    totaleDaPagareRegExp = totaleDaPagareStr+"[0-9]+,[0-9]+"
    matched = re.search(totaleDaPagareRegExp,fp)
    
    return float(matched.group().replace(totaleDaPagareStr,'').replace(',','.'))
     

def __getCostoMedioUnitario(fp):
    costoMedioUnitarioStr='Costo medio unitario bolletta'
    costoMedioUnitarioMatEnerStr = 'Costo medio unitario spesa materia energia'
    costoMedioUnitario = fp[fp.find(costoMedioUnitarioStr)+len(costoMedioUnitarioStr):fp.find(costoMedioUnitarioMatEnerStr)].replace(',','.')
    subFp = fp[fp.find(costoMedioUnitarioMatEnerStr)+len(costoMedioUnitarioMatEnerStr):len(fp)]
    costoMedioUnitarioMatEner = subFp[0:subFp.find('Ulteriori')].replace(',','.')
    return {costoMedioUnitarioStr:float(costoMedioUnitario),costoMedioUnitarioMatEnerStr:costoMedioUnitarioMatEner}

def __getDettaglioCosti(fp):
    dettaglioCosti = {}
    
    spesaMateriaEnergiaStr= "Spesa per la materia energia"
    costoRegExp = "[0-9]+,[0-9]+"
    #spesaMateriaEnergiaRegExp = "Spesa per la materia energia[0-9]+,[0-9]+"
    spesaMateriaEnergiaRegExp = spesaMateriaEnergiaStr + costoRegExp
    
    spesaTrasportoGestioneContatoreStr= "Spesa per il trasporto e la gestione del contatore"
    spesaTrasportoGestioneContatoreRegExp = spesaTrasportoGestioneContatoreStr + costoRegExp
    
    speseOneriSistemaStr = 'Spesa per oneri di sistema'
    speseOneriSistemaRegExp = speseOneriSistemaStr + costoRegExp
    
    imposteStr = 'Imposte'
    imposteRegExp = imposteStr + costoRegExp

    altroSoggettoIvaStr = 'Altre partite soggette iva'
    altroSoggettoIvaRegExp = altroSoggettoIvaStr + costoRegExp

    totaleImponibileStr = 'Totale imponibile'
    totaleImponibileRegExp = totaleImponibileStr + costoRegExp

    iva10Str = 'Iva 10%'
    iva10RegExp = iva10Str + costoRegExp

    arrotondamentiStr = 'Arrotondamenti'
    arrotondamentiRegExp = arrotondamentiStr + costoRegExp

    totaleBollettaStr = 'Totale bolletta'
    totaleBollettaRegExp = totaleBollettaStr + costoRegExp
   
    
    matched = re.search(spesaMateriaEnergiaRegExp, fp)
    spesaMateriaEnergia=float(matched.group().replace(spesaMateriaEnergiaStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[spesaMateriaEnergiaStr]=spesaMateriaEnergia
    
    
    matched = re.search(spesaTrasportoGestioneContatoreRegExp, fp)
    spesaTrasportoGestioneContatore=float(matched.group().replace(spesaTrasportoGestioneContatoreStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[spesaTrasportoGestioneContatoreStr]=spesaTrasportoGestioneContatore

    matched = re.search(speseOneriSistemaRegExp,fp)
    speseOneriSistema=float(matched.group().replace(speseOneriSistemaStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[speseOneriSistemaStr]=speseOneriSistema

    matched = re.search(imposteRegExp,fp)
    imposte=float(matched.group().replace(imposteStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[imposteStr]=imposte

    matched = re.search(altroSoggettoIvaRegExp,fp)
    altroSoggettoIva = float(matched.group().replace(altroSoggettoIvaStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[altroSoggettoIvaStr]=altroSoggettoIva

    matched = re.search(totaleImponibileRegExp,fp)
    totaleImponibile = float(matched.group().replace(totaleImponibileStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[totaleImponibileStr] = totaleImponibile

    matched = re.search(iva10RegExp,fp)
    iva10 = float(matched.group().replace(iva10Str,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[iva10Str]=iva10

    matched = re.search(arrotondamentiRegExp,fp)
    arrotondamenti = float(matched.group().replace(arrotondamentiStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[arrotondamentiStr]=arrotondamenti

    matched = re.search(totaleBollettaRegExp,fp)
    totaleBolletta = float(matched.group().replace(totaleBollettaStr,'').replace(',','.') if matched != None else 0.0)
    dettaglioCosti[totaleBollettaStr] = totaleBolletta
    
    return dettaglioCosti
    
def __getTipologiaCliente(fp):
    tipologiaClienteStr = "Tipologia Cliente"
    tipologiaClienteRegExp = tipologiaClienteStr +"[A-Z]{1}[ a-z]+"
    matched = re.search(tipologiaClienteRegExp,fp)
    return matched.group().replace(tipologiaClienteStr,'')

def __getPotenzaDisponibileKw(fp):
    potenzaDisponibileStr = "Potenza disponibile"
    potenzaDisponibileRegExp = potenzaDisponibileStr + "[0-9]+,?[0-9]*"
    matched = re.search(potenzaDisponibileRegExp,fp)
    return float(matched.group().replace(potenzaDisponibileStr,'').replace(',','.'))


#filename = 'C:\projectPython\data\eletrica\iren\Fattura Iren 1515244_es.pdf'
 #filename = 'C:\projectPython\data\eletrica\iren\Fattura Iren 1374175_es.pdf'

#filename = 'D:\Utenti\Angelo\Documenti\bollettaelettrica\TO_20171121454642.pdf'
filename ='D:\\bollettaelettrica\\pippo.pdf'
#filename = '/media/angelo/DATA/bollettaelettrica/pippo.pdf'

if pathlib.Path(filename).is_file() == False:    
    print('File non valido')

pdf_read = open (filename,'rb')
pdf_read_start = PyPDF2.PdfFileReader(pdf_read)

page0=''
page1=''

if(pdf_read_start.getNumPages() > 0):
    pageObj = pdf_read_start.getPage(0)
    page0=pageObj.extractText()
    pageObj1 = pdf_read_start.getPage(1)
    page1=pageObj1.extractText()

pdf_read.close()

bolletta=BollettaLuceIren(__getFattura(page0)[0],__getPod(page0),__getFornitura(page0),__getCostoTotale(page0))
bolletta.consumiFasce['F1']=__getConsumoAnnuo(page0,'F1')
bolletta.consumiFasce['F2']=__getConsumoAnnuo(page0,'F2')
bolletta.consumiFasce['F3']=__getConsumoAnnuo(page0,'F3')
bolletta.consumiFasce['TOT']=__getConsumoAnnuo(page0,'ALL')

#print(bolletta.gestore)
print(__getPotenzaDisponibileKw(page0))










