class Bolletta:
    def __init__(self,codiceFattura='',codiceFornitura='',costoTotale=0,tipologiaCliente=''):
        self.codiceFornitura=codiceFornitura
        self.codiceFattura=codiceFattura
        self.costoTotale=costoTotale
        self.tipologiaCliente=tipologiaCliente


class BollettaLuce(Bolletta):

    tipo = 'Luce'
    
    def __init__(self,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0,tipologiaCliente='',potenzaDisponibile=0.0):
        super().__init__(codiceFattura,codiceFornitura,costoTotale,tipologiaCliente='')
        self.codicePod=codicePod
        self.potenzaDisponibile=potenzaDisponibile


class BollettaGas(Bolletta):
    tipo = 'Gas'
    def __init__(self, codiceFattura='', codicePdr='',codiceFornitura='',costoTotale=0):
        super().__init__(codiceFattura,codiceFornitura,costoTotale)
        self.codicePdr=codicePdr
        

class BollettaLuceIren(BollettaLuce):

    gestore='IREN'

    def __init__(self,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0,tipologiaCliente='',potenzaDisponibile=0.0):
        super().__init__(codiceFattura,codicePod,codiceFornitura,costoTotale,tipologiaCliente='',potenzaDisponibile=0.0)
        self.consumiFasce={'F1': 0.0, 'F2': 0.0, 'F3': 0.0, 'TOT' : 0.0}
    
    def __str__(self):
        return "Bolletta: {}, gestore: {}, fattura: {}, fornitura: {}, codice POD: {}, costo: {}€, consumi {}".format(self.tipo, self.gestore, self.codiceFattura,
                                                                                                          self.codiceFornitura, self.codicePod, self.costoTotale,
                                                                                                          self.consumiFasce)


    

            

    
