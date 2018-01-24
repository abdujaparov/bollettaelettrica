class Bolletta:
    def __init__(self,codiceFattura='',codiceFornitura='',costoTotale=0):
        self.codiceFornitura=codiceFornitura
        self.codiceFattura=codiceFattura
        self.costoTotale=costoTotale


class BollettaLuce(Bolletta):

    tipo = 'Luce'
    
    def __init__(self,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0):
        super().__init__(codiceFattura,codiceFornitura,costoTotale)
        self.codicePod=codicePod


class BollettaGas(Bolletta):
    tipo = 'Gas'
    def __init__(self, codiceFattura='', codicePdr='',codiceFornitura='',costoTotale=0):
        super().__init__(codiceFattura,codiceFornitura,costoTotale)
        self.codicePdr=codicePdr
        

class BollettaLuceIren(BollettaLuce):

    gestore='IREN'

    def __init__(self,codiceFattura='',codicePod='',codiceFornitura='',costoTotale=0):
        super().__init__(codiceFattura,codicePod,codiceFornitura,costoTotale)
        self.consumiFasce={'F1': 0.0, 'F2': 0.0, 'F3': 0.0}

    def consumoTotale(self):
        self.conTot=0
        for key,value in self.consumiFasce.items():
            self.conTot += value
        return self.conTot

    

            

    
