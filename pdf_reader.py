import PyPDF2
import re
from bolletta import BollettaLuceIren

class BollettaIrenParser:
    
    def __init__(self,filename):
        pdf_read = open (filename,'rb')
        pdf_read_start = PyPDF2.PdfFileReader(pdf_read)
        
        self.page0 = ''
        
        if(pdf_read_start.getNumPages() > 0):
            pageObj = pdf_read_start.getPage(0)
            self.page0=pageObj.extractText()
            #pageObj1 = pdf_read_start.getPage(1)
            #page1=pageObj1.extractText()
        
        pdf_read.close()
        
        self.bolletta=BollettaLuceIren()

     
    def parse(self):
        self.bolletta.codiceFornitura=self.__getFornitura()
        self.bolletta.codicePod= self._getPod()
        self.costoTotale=self.__getCostoTotale()
        self.bolletta.consumiFasce['F1']=self.__getConsumoAnnuo('F1')
        self.bolletta.consumiFasce['F1']=self.__getConsumoAnnuo('F2')
        self.bolletta.consumiFasce['F1']=self.__getConsumoAnnuo('F3')
        self.bolletta.consumiFasce['F1']=self.__getConsumoAnnuo('ALL')
        self.bolletta.tipologiaCliente=self.__getTipologiaCliente()
        self.bolletta.potenzaDisponibile=self.__getPotenzaDisponibileKw()
         
    
    def __getFornitura(self):
        
        stringa_fornitura = "Contratto Numero"
        fornituraRegExp = stringa_fornitura+"[0-9]+"
        
        matched = re.search(fornituraRegExp, self.page0)
        return matched.group().replace(stringa_fornitura,'')


    def __getPod(self):
    
        stringa_pod="Codice POD"
        
        podRegExp = stringa_pod+"[A-Z0-9]{14}"
        matched = re.search(podRegExp, self.page0)
    
        return matched.group().replace(stringa_pod,'')

    def __getPeriodo(self,fp):
        stringa_periodo='PERIODO'
        stringa_fattura='Fattura'
        posPeriodo=fp.find(stringa_periodo)
        posFattura=fp.find(stringa_fattura)
        periodo=fp[posPeriodo+len(stringa_periodo):posFattura]
    
        return periodo

    def __getConsumoAnnuo(self,fascia):
        regExpString = r"Consumo dal [0-9]{2}/[0-9]{2}/[0-9]{4} al [0-9]{2}/[0-9]{2}/[0-9]{4}.*non distinto perfasce.*COSTO"
    
        subFp = self.page0[self.page0.find('Consumo dal'):len(self.page0)]    
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

    def __getFattura(self,fp):
        stringaFattura = 'Fattura n.'
        subFp=fp[fp.find(stringaFattura):len(fp)]
        posDel=subFp.find('del')
        return [subFp[len(stringaFattura):posDel],subFp[subFp.find('del')+len('del')+1:subFp.find('Per')]]
    
    def __getCostoTotale(self):
        totaleDaPagareStr='Totale da pagare Euro'
        
        totaleDaPagareRegExp = totaleDaPagareStr+"[0-9]+,[0-9]+"
        matched = re.search(totaleDaPagareRegExp,self.page0)
        
        return float(matched.group().replace(totaleDaPagareStr,'').replace(',','.'))
     

    def __getCostoMedioUnitario(self):
        costoMedioUnitarioStr='Costo medio unitario bolletta'
        costoMedioUnitarioMatEnerStr = 'Costo medio unitario spesa materia energia'
        costoMedioUnitario = self.page0[self.page0.find(costoMedioUnitarioStr)+len(costoMedioUnitarioStr):self.page0.find(costoMedioUnitarioMatEnerStr)].replace(',','.')
        subFp = self.page0[self.page0.find(costoMedioUnitarioMatEnerStr)+len(costoMedioUnitarioMatEnerStr):len(self.page0)]
        costoMedioUnitarioMatEner = subFp[0:subFp.find('Ulteriori')].replace(',','.')
        return {costoMedioUnitarioStr:float(costoMedioUnitario),costoMedioUnitarioMatEnerStr:costoMedioUnitarioMatEner}

    def __getDettaglioCosti(self):
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
       
        
        matched = re.search(spesaMateriaEnergiaRegExp, self.page0)
        spesaMateriaEnergia=float(matched.group().replace(spesaMateriaEnergiaStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[spesaMateriaEnergiaStr]=spesaMateriaEnergia
        
        
        matched = re.search(spesaTrasportoGestioneContatoreRegExp, self.page0)
        spesaTrasportoGestioneContatore=float(matched.group().replace(spesaTrasportoGestioneContatoreStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[spesaTrasportoGestioneContatoreStr]=spesaTrasportoGestioneContatore
    
        matched = re.search(speseOneriSistemaRegExp,self.page0)
        speseOneriSistema=float(matched.group().replace(speseOneriSistemaStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[speseOneriSistemaStr]=speseOneriSistema
    
        matched = re.search(imposteRegExp,self.page0)
        imposte=float(matched.group().replace(imposteStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[imposteStr]=imposte
    
        matched = re.search(altroSoggettoIvaRegExp,self.page0)
        altroSoggettoIva = float(matched.group().replace(altroSoggettoIvaStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[altroSoggettoIvaStr]=altroSoggettoIva
    
        matched = re.search(totaleImponibileRegExp,self.page0)
        totaleImponibile = float(matched.group().replace(totaleImponibileStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[totaleImponibileStr] = totaleImponibile
    
        matched = re.search(iva10RegExp,self.page0)
        iva10 = float(matched.group().replace(iva10Str,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[iva10Str]=iva10
    
        matched = re.search(arrotondamentiRegExp,self.page0)
        arrotondamenti = float(matched.group().replace(arrotondamentiStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[arrotondamentiStr]=arrotondamenti
    
        matched = re.search(totaleBollettaRegExp,self.page0)
        totaleBolletta = float(matched.group().replace(totaleBollettaStr,'').replace(',','.') if matched != None else 0.0)
        dettaglioCosti[totaleBollettaStr] = totaleBolletta
        
        return dettaglioCosti
    
    def __getTipologiaCliente(self):
        tipologiaClienteStr = "Tipologia Cliente"
        tipologiaClienteRegExp = tipologiaClienteStr +"[A-Z]{1}[ a-z]+"
        matched = re.search(tipologiaClienteRegExp,self.page0)
        return matched.group().replace(tipologiaClienteStr,'')

    def __getPotenzaDisponibileKw(self):
        potenzaDisponibileStr = "Potenza disponibile"
        potenzaDisponibileRegExp = potenzaDisponibileStr + "[0-9]+,?[0-9]*"
        matched = re.search(potenzaDisponibileRegExp,self.page0)
        return float(matched.group().replace(potenzaDisponibileStr,'').replace(',','.'))
















