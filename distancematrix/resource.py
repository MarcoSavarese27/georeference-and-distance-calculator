from flask import request
from flask_restful import Resource
from distancematrix.distancematrix import get_matrix_osrm
from pprint import pprint
import commons


matrices = {}

class DistanceMatrix(Resource):
    
    def post(self):
        
        data = request.json
        resolutionType = data['resolutionType'].lower()
        georeferencedAddresses = data['addresses']

        if not commons.validate_resolution_type(resolutionType):
            return None, 400
        
        if resolutionType == 'inline':
            matrixfd = get_matrix_osrm(georeferencedAddresses)
            return matrixfd, 200

class DistanceMatrixId(Resource):
    pass