import pathlib
from pdf_reader import BollettaIrenParser
from dataStore.JSONFileStore import JSONFileStore
import json
from simplejson.encoder import JSONEncoder
from bolletta import BollettaMetadata

if __name__ == "__main__":
    print("Start")
    filename = '/media/angelo/DATA/bollettaelettrica/pippo.pdf'
    
    if pathlib.Path(filename).is_file() == False:
        print('File non valido')
        exit
        
    parser = BollettaIrenParser(filename)
    
    bolletta = parser.parseData()
    bollettaMetadata=parser.parseMetadata()
    print(bollettaMetadata.__dict__)
    print(bolletta.__dict__)
    #jsonStore = JSONFileStore('/home/angelo/bolletta.json')
    #jsonStore.store(bolletta,'a')
    
