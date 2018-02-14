import uuid

class BollettaMetadata:

    def __init__(self,bolletta,filename,location,testo):
        super().__init__(bolletta.codiceFattura,bolletta.codiceFornitura,self.codiceFattura, self.costoTotale, self.tipologiaCliente,self.tipo,self.gestore)
        self.filename
        self.location
        self.testo
        self.uuid=uuid.uuid4()
        self.bolletta=bolletta.uuid


class Bolletta:
    def __init__(self,codiceFattura='',codiceFornitura='',costoTotale=0,tipologiaCliente='',tipo,gestore):
        self.codiceFornitura=codiceFornitura
        self.codiceFattura=codiceFattura
        self.costoTotale=costoTotale
        self.tipologiaCliente=tipologiaCliente
        self.tipo=tipo
        self.gestore
        self.uuid=uuid.uuid4()

        

class BollettaLuce(Bolletta):

    
    def __init__(self,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0,tipologiaCliente='',potenzaDisponibile=0.0,gestore):
        super().__init__(codiceFattura,codiceFornitura,costoTotale,tipologiaCliente='','Luce',gestore)
        self.codicePod=codicePod
        self.potenzaDisponibile=potenzaDisponibile


class BollettaGas(Bolletta):
    
    def __init__(self, codiceFattura='', codicePdr='',codiceFornitura='',costoTotale=0,gestore):
        super().__init__(codiceFattura,codiceFornitura,costoTotale,'Gas',gestore)
        self.codicePdr=codicePdr
        

class BollettaLuceIren(BollettaLuce):


    def __init__(self,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0,tipologiaCliente='',potenzaDisponibile=0.0):
        super().__init__(codiceFattura,codicePod,codiceFornitura,costoTotale,tipologiaCliente='',potenzaDisponibile=0.0,'IREN')
        self.consumiFasce={'F1': 0.0, 'F2': 0.0, 'F3': 0.0, 'TOT' : 0.0}
    
    def __str__(self):
        return "Bolletta: {}, gestore: {}, fattura: {}, fornitura: {}, codice POD: {}, costo: {}€, consumi {}".format(self.tipo, self.gestore, self.codiceFattura,
                                                                                                          self.codiceFornitura, self.codicePod, self.costoTotale,
                                                                                                          self.consumiFasce)


    

            

    
