from flask import request
from flask_restful import Resource
from os import remove
from georeference.handlepost import handle_json_post, handle_xlsx_post, resolutions
from georeference.xls_json_converter import convert_to_json
from commons import validate_resolution_type, is_valid_uuid



class Georeference(Resource):

    def post(self):
        
        json_data = request.json
        json_data_keys = list(json_data.keys())
        resolution_type = json_data['resolutionType'].lower()
        
        if not validate_resolution_type(resolution_type):
            return None, 400
        
        if json_data_keys[1] == 'addressesDescription':
            addresses = json_data['addressesDescription']
            content, code = handle_json_post(resolution_type, addresses, request.base_url)
            
        elif json_data_keys[1] == 'filePath': 
            addresses = convert_to_json(json_data['filePath'])  
            content, code = handle_xlsx_post(resolution_type, addresses, request.base_url)
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
            
            try:           
                remove(f'georeference/xls/{id}.xlsx')
            except OSError:
                pass

            return None, 204
        
        return None, 404
        
        
    