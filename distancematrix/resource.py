from flask import request
from flask_restful import Resource
from distancematrix.distancematrix import get_matrix_osrm
from multiprocessing import Pool
from commons import create_url, create_uuid, validate_resolution_type, is_valid_uuid
import os


matrix = {}

class DistanceMatrix(Resource):
    
    def post(self):
        
        data = request.json
        resolution_type = data['resolutionType'].lower()
        georeferenced_addresses = data['addresses']

        if not validate_resolution_type(resolution_type):
            return None, 400
        
        id = create_uuid()
        if resolution_type == 'inline':
            matrixfd = get_matrix_osrm(georeferenced_addresses, id)
            return matrixfd, 200
        
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