'''
Created on 07 feb 2018

@author: angelo
'''
import json
from json.encoder import JSONEncoder


class JSONFileStore(object):
    '''
    classdocs
    '''

    def __init__(self,filename):
        self.filename = filename

    def store(self,bolletta,option):
        # with open(self.filename,option) as outfile:
        #    json.dump(vars(bolletta),outfile,indent=1)
        #    outfile.write('\n')
        self.f = open(self.filename,option)
        json.dump(bolletta.__dict__,self.f,indent=1)
        self.f.write('\n')

    def close(self):
        self.f.close()
