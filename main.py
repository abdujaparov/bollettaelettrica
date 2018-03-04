from os import listdir
from os.path import isfile, join
import logging.config
import yaml
from pdf_reader import BollettaIrenParser
from dataStore.ElasticSearchStore import ElasticSearchStore



def extract_data(pdf_list):
    data_list = {'data': [], 'metadata':[]}


    for pdf in pdf_list:
        logging.debug(pdf)
        parser = BollettaIrenParser(pdf)
        data_list['data'].append(parser.parseData())
        data_list['metadata'].append(parser.parseMetadata())

    logging.debug("Data parsed: {}".format(len(data_list['data'])))
    logging.debug("Metadata extracted: {}".format(len(data_list['metadata'])))

    return data_list


def save_metadata(metadata_list):

    ess = ElasticSearchStore({"host":"192.168.1.151","port":9200,"user":"elastic","pass":"elastic"})

    for meta in metadata_list:
        ess.put_metadata("bolletta","luce_iren",meta.uuid,meta)




if __name__ == "__main__":


    with open("conf/logging.yaml",'r') as stream:
        config = yaml.load(stream)

    logging.config.dictConfig(config)

    logging.info("Started")
    directory = "D:\\bollettaelettrica"

    bollette_file = [directory+"\\"+f for f in listdir(directory) if (isfile(join(directory,f)) and f.__contains__(".pdf"))]


    bolletta_list=extract_data(bollette_file)

    save_metadata(bolletta_list["metadata"])

    # parser = BollettaIrenParser(filename)
    #
    # bolletta = parser.parseData()
    # bollettaMetadata=parser.parseMetadata()
    # print(bollettaMetadata.__dict__)
    # print(bolletta.__dict__)
    #jsonStore = JSONFileStore('/home/angelo/bolletta.json')
    #jsonStore.store(bolletta,'a')

    logging.info("Terminated")
    
