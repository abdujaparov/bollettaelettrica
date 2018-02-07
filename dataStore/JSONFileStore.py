'''
Created on 07 feb 2018

@author: angelo
'''
import json


class JSONFileStore(object):
    '''
    classdocs
    '''


    def __init__(self, filename):
        self.filename=filename
        
    def store(self, bolletta,option):
        with open(self.filename,option) as outfile:
            json.dump(vars(bolletta),outfile,indent=1)
            outfile.write('\n')
        