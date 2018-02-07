import pathlib
from pdf_reader import BollettaIrenParser
from dataStore.JSONFileStore import JSONFileStore
import json
from simplejson.encoder import JSONEncoder

if __name__ == "__main__":
    print("Start")
    filename = '/media/angelo/DATA/bollettaelettrica/pippo.pdf'
    
    if pathlib.Path(filename).is_file() == False:
        print('File non valido')
        exit
        
    parser = BollettaIrenParser(filename)
    
    bolletta = parser.parse()
    jsonStore = JSONFileStore('/home/angelo/bolletta.json')
    jsonStore.store(bolletta,'a')
    
