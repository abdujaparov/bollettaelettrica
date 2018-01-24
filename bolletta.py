class Bolletta:
    def __init__(self,codiceFornitura=''):
        self.codiceFornitura=codiceFornitura


class BollettaLuce(Bolletta):

    tipo = 'Luce'
    
    def __init__(self,codicePod='',codiceFornitura=''):
        super().__init__(codiceFornitura)
        self.codicePod=codicePod

class BollettaLuceIren(BollettaLuce):

    gestore='IREN'

    def __init__(self,codicePod='',codiceFornitura=''):
        super().__init__(codicePod,codiceFornitura)
        self.consumiFasce={'F1': 0.0, 'F2': 0.0, 'F3': 0.0}

    def consumoTotale(self):
        self.conTot=0
        for key,value in self.consumiFasce.items():
            self.conTot += value
        return self.conTot

    

            

    
