from flask import request
from flask_restful import Resource
from georeference.handlepost import handle_json_post, handle_xlsx_post, resolutions
from georeference.xls_json_converter import convert_to_json
from commons import validate_resolution_type, is_valid_uuid


class Georeference(Resource):

    def post(self):
        
        jsonData = request.json
        jsonDataKeys = list(jsonData.keys())
        resolutionType = jsonData['resolutionType'].lower()
        
        if not validate_resolution_type(resolutionType):
            return None, 400
        
        if jsonDataKeys[1] == 'addressesDescription':
            addresses = jsonData['addressesDescription']
            content, code = handle_json_post(resolutionType, addresses, request.base_url)
            
        elif jsonDataKeys[1] == 'filePath': 
            addresses = convert_to_json(jsonData['filePath'])  
            content, code = handle_xlsx_post(resolutionType, addresses, request.base_url)
        else:
            return None, 400
        
        return content, code
        
class GeoreferenceId(Resource):

    def get(self, id):
        
        if not is_valid_uuid(id):
            return None, 400
        
        if id in resolutions:
            value = resolutions[id].get()
            return value, 200
        
        return None, 404

    def delete(self, id):
        
        if not is_valid_uuid(id):
            return None, 400
        
        if id in resolutions:
            del resolutions[id]
            return None, 204
        
        return None, 404
        
        
    