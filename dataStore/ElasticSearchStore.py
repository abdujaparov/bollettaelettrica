'''
Created on 18 feb 2018

@author: angelo
'''

import elasticsearch

class ElasticSearchStore(object):
    '''
    classdocs
    '''

    es = None

    def __init__(self, params):
        '''
        Constructor
        '''
        logging.debug("Params: host={} port={}".format(params["host"],params["port"]))
        self.es=elasticsearch.Elasticsearch({'host': params["host"],'port':params["port"]})


    def put_metadata(self,index_name, index_type,metadata_list):

        for metadata in metadata_list:
            print(self.es.index(index=index_name,doc_type=index_type,metadata,metadata_list[metadata_list]))
