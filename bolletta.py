import uuid

class BollettaMetadata:

    def __init__(self,filename,testo):
        #super().__init__(bolletta.codiceFattura,bolletta.codiceFornitura,self.codiceFattura, self.costoTotale, self.tipologiaCliente,self.tipo,self.gestore)
        self.filename=filename
        self.testo=testo
        self.uuid=uuid.uuid4().__str__()
        self.tipo=''
        self.gestore=''
        self.codFattura =''
        self.dataFattura = ''



class Bolletta:
    def __init__(self,tipo,gestore,codiceFattura='',codiceFornitura='',costoTotale=0,tipologiaCliente=''):
        self.codiceFornitura=codiceFornitura
        self.codiceFattura=codiceFattura
        self.costoTotale=costoTotale
        self.tipologiaCliente=tipologiaCliente
        self.tipo=tipo
        self.gestore=gestore
        self.uuid=uuid.uuid4().__str__()

        

class BollettaLuce(Bolletta):

    
    def __init__(self,gestore,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0,tipologiaCliente='',potenzaDisponibile=0.0):
        super().__init__('Luce',gestore,codiceFattura,codiceFornitura,costoTotale,tipologiaCliente='')
        self.codicePod=codicePod
        self.potenzaDisponibile=potenzaDisponibile


class BollettaGas(Bolletta):
    
    def __init__(self,gestore, codiceFattura='', codicePdr='',codiceFornitura='',costoTotale=0):
        super().__init__('Gas',gestore,codiceFattura,codiceFornitura,costoTotale)
        self.codicePdr=codicePdr
        

class BollettaLuceIren(BollettaLuce):


    def __init__(self,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0,tipologiaCliente='',potenzaDisponibile=0.0):
        super().__init__('IREN',codiceFattura,codicePod,codiceFornitura,costoTotale,tipologiaCliente='',potenzaDisponibile=0.0)
        self.consumiFasce={'F1': 0.0, 'F2': 0.0, 'F3': 0.0, 'TOT' : 0.0}
    
    def __str__(self):
        return "Bolletta: {}, gestore: {}, fattura: {}, fornitura: {}, codice POD: {}, costo: {}€, consumi {}".format(self.tipo, self.gestore, self.codiceFattura,
                                                                                                          self.codiceFornitura, self.codicePod, self.costoTotale,
                                                                                                          self.consumiFasce)


    

            

    
