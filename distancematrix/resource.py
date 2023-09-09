from flask import request
from flask_restful import Resource
from distancematrix.distancematrix import get_matrix_osrm
from multiprocessing import Pool
import commons
import os


matrix = {}

class DistanceMatrix(Resource):
    
    def post(self):
        
        data = request.json
        resolutionType = data['resolutionType'].lower()
        georeferencedAddresses = data['addresses']

        if not commons.validate_resolution_type(resolutionType):
            return None, 400
        
        id = commons.create_uuid()
        if resolutionType == 'inline':
            matrixfd = get_matrix_osrm(georeferencedAddresses, id)
            return matrixfd, 200
        
        else:
            workers = Pool(1)
            global matrix
            matrixArg = (georeferencedAddresses, id)
            matrix[id] = workers.apply_async(get_matrix_osrm, matrixArg)
            if resolutionType == 'id':
                return  {'id': id}, 200
            elif resolutionType == 'url':
                url = commons.create_url(request.base_url, id)
                return {'url': url}, 200


class DistanceMatrixId(Resource):
    
    global matrix 

    def get(self, id):
        if not commons.is_valid_uuid(id):
            return None, 400
        
        if id in matrix:
            value = matrix[id].get()
            return value, 200
        
        return None, 404


    def delete(self, id):
        if not commons.is_valid_uuid(id):
            return None, 400
        
        if id in matrix:
            del matrix[id]
            os.remove(f'distancematrix/xls/{id}')
            return None, 204
        
        return None, 404