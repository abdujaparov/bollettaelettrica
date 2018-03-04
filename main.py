from os import listdir
from os.path import isfile, join
import logging.config
import yaml
from pdf_reader import BollettaIrenParser




def extract_data(pdf_list):
    data_list = {'data': [], 'metadata':[]}


    for pdf in pdf_list:
        logging.debug(pdf)
        parser = BollettaIrenParser(pdf)
        data_list['data'].append(parser.parseData())
        data_list['metadata'].append(parser.parseMetadata())

    logging.debug(data_list)

    return data_list



if __name__ == "__main__":


    with open("conf/logging.yaml",'r') as stream:
        config = yaml.load(stream)

    logging.config.dictConfig(config)

    logging.info("Started")
    directory = "D:\\bollettaelettrica"

    bollette_file = [directory+"\\"+f for f in listdir(directory) if (isfile(join(directory,f)) and f.__contains__(".pdf"))]


    bolletta_list=extract_data(bollette_file)


    # parser = BollettaIrenParser(filename)
    #
    # bolletta = parser.parseData()
    # bollettaMetadata=parser.parseMetadata()
    # print(bollettaMetadata.__dict__)
    # print(bolletta.__dict__)
    #jsonStore = JSONFileStore('/home/angelo/bolletta.json')
    #jsonStore.store(bolletta,'a')

    logging.info("Terminated")
    
