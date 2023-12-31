from flask import request
from flask_restful import Resource
import os
from multiprocessing import Pool
from distancematrix.distancematrix import get_matrix_osrm
from commons import create_url, create_uuid, validate_resolution_type, is_valid_uuid, convert_to_json



matrix = {}

class DistanceMatrix(Resource):
    
    def post(self):
        
        data = request.json
        data_keys = list(data.keys())
        resolution_type = data['resolutionType'].lower()
        
        if not validate_resolution_type(resolution_type):
            return None, 400
        
        if data_keys[1] == 'addresses':
            georeferenced_addresses = data['addresses']
            
        elif data_keys[1] == 'filePath': 
            georeferenced_addresses = convert_to_json(path=data['filePath'], campi=['address', 'latitude', 'longitude'])  
        else:
            return None, 400
        
        id = create_uuid()
        if resolution_type == 'inline':
            matrix_fd = get_matrix_osrm(georeferenced_addresses, id)
            return matrix_fd, 200
        
        else:
            workers = Pool(1)
            global matrix
            matrix_arg = (georeferenced_addresses, id)
            matrix[id] = workers.apply_async(get_matrix_osrm, matrix_arg)
            if resolution_type == 'id':
                return  {'id': id}, 200
            elif resolution_type == 'url':
                url = create_url(request.base_url, id)
                return {'url': url}, 200


class DistanceMatrixId(Resource):
    
    global matrix 

    def get(self, id):
        if not is_valid_uuid(id):
            return None, 400
        
        if id in matrix:
            value = matrix[id].get()
            return value, 200
        
        return None, 404


    def delete(self, id):
        if not is_valid_uuid(id):
            return None, 400
        
        if id in matrix:
            del matrix[id]
            os.remove(f'distancematrix/xls/{id}')
            return None, 204
        
        return None, 404