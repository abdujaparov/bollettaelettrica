class BollettaIren:

    def __init__(self,codicePod='',codiceFornitura=''):
        self.codicePod=codicePod
        self.codiceFornitura=codiceFornitura
        self.consumiFasce={'F1': 0.0, 'F2': 0.0, 'F3': 0.0}

    def consumoTotale(self):
        self.conTot=0
        for key,value in self.consumiFasce.items():
            self.conTot += value
        return self.conTot

    

            

    
