import pathlib
from pdf_reader import BollettaIrenParser 

if __name__ == "__main__":
    print("Start")
    filename = '/media/angelo/DATA/bollettaelettrica/pippo.pdf'
    
    if pathlib.Path(filename).is_file() == False:
        print('File non valido')
        exit
        
    parser = BollettaIrenParser(filename)
    
    bolletta = parser.parse()
    print(bolletta)    
    