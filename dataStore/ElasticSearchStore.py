'''
Created on 18 feb 2018

@author: angelo
'''

import elasticsearch
import logging.config

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
        self.es=elasticsearch.Elasticsearch(["http://{}:{}@{}:{}/".format(params["user"],params["pass"],params["host"],params["port"])])


    def put_metadata(self,index_name, index_type,id,metadata):
        logging.info(self.es.index(index=index_name,doc_type=index_type,id=id,body=metadata.__dict__))