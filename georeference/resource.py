from flask import request
from flask_restful import Resource
from multiprocessing import Pool
from db_interaction import retrieve_data
from ..commons import utils
import uuid


resolutions = {}

class Georeference(Resource):

    def post(self):
        jsonData = request.json
        resolutionType = jsonData['resolutionType'].lower()
        addresses = jsonData['addressesDescription']
        
        if not utils.validate_resolution_type(resolutionType):
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
            id = utils.create_uuid()
            workers = Pool(2)
            global resolutions
            result = workers.map_async(self.address_resolution, addresses)
            resolutions[id] = result
            if resolutionType == 'id':
                return  {'id': id}, 200
            else:
                url = utils.create_url(request.base_url, 'georef')
                return {'url': url}, 200
            
    def address_resolution(self, add):
        geocode = retrieve_data(add)
        return geocode

class GeoreferenceId(Resource):
    def get(self, id):
        
        global resolutions
        
        if not utils.is_valid_uuid(id):
            return None, 400
        
        if id in resolutions:
            value = resolutions[id].get()
            return value, 200
        
        return None, 404


    def delete(self, id):
        global resolutions
        
        if not utils.is_valid_uuid(id):
            return None, 400
        
        if id in resolutions:
            del resolutions[id]
            return None, 204
        
        return None, 404
        
        
    