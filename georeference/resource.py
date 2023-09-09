from flask import request
from flask_restful import Resource
from multiprocessing import Pool
from georeference.db_interaction import retrieve_data
import commons


resolutions = {}

class Georeference(Resource):

    def post(self):
        
        jsonData = request.json
        resolutionType = jsonData['resolutionType'].lower()
        addresses = jsonData['addressesDescription']
        
        if not commons.validate_resolution_type(resolutionType):
            return None, 400
        
        if resolutionType == 'inline':
            reslist = []
            for k in addresses:
                res = self.address_resolution(k)
        
                if isinstance(res, str):
                    continue
                
                reslist.append(res)
            return reslist, 200
        
        else:

            id = commons.create_uuid()
            workers = Pool(2)
            global resolutions
            resolutions[id] = workers.map_async(self.address_resolution, addresses)
            
            if resolutionType == 'id':
                return  {'id': id}, 200
            elif resolutionType == 'url':
                url = commons.create_url(request.base_url, id)
                return {'url': url}, 200
            
    def address_resolution(self, add):
        geocode = retrieve_data(add)
        return geocode

class GeoreferenceId(Resource):

    global resolutions
    
    def get(self, id):
        
        if not commons.is_valid_uuid(id):
            return None, 400
        
        if id in resolutions:
            value = resolutions[id].get()
            return value, 200
        
        return None, 404


    def delete(self, id):
        
        if not commons.is_valid_uuid(id):
            return None, 400
        
        if id in resolutions:
            del resolutions[id]
            return None, 204
        
        return None, 404
        
        
    