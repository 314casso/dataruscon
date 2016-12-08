# -*- coding: utf-8 -*-
from suds.client import Client
from __builtin__ import setattr
import base64


class BaseService():
    def __init__(self, settings):
        self.set_client(settings)
            
    def set_client(self, settings):
        for key in settings.iterkeys():             
            setattr(self, key, settings.get(key))   
        base64string = base64.encodestring('%s:%s' % (self.username, self.password)).replace('\n', '')
        authenticationHeader = {
            "SOAPAction" : "ActionName",
            "Authorization" : "Basic %s" % base64string
        }                
        self._client = Client(self.url, headers=authenticationHeader)


class StockDataService(BaseService):    
    def get_data(self):
        result = self._client.service.GetEmptyDemand()        
        if hasattr(result, 'row') and result.row:           
            for crow in result.row:                 
                crow['rest'] = crow['stated'] - crow['done']
        return result.row
    
    def get_simple_data(self):
        result = []        
        string_data = self._client.service.GetEmptyDemandString()
        rows = string_data.split(';')
        for row in rows: 
            parts = row.split()
            result.append({'size': parts[0], 'line': parts[1]})
        return result
        
