from flask import Flask
from flask_restful import Api
from georeference.resource import Georeference, GeoreferenceId
from distancematrix.resource import DistanceMatrix, DistanceMatrixId


app = Flask(__name__)
api = Api(app)
basePath = '/api/v1'

api.add_resource(Georeference, f'{basePath}/georef')
api.add_resource(GeoreferenceId, f'{basePath}/georef/<string:id>')
api.add_resource(DistanceMatrix, f'{basePath}/dm')
api.add_resource(DistanceMatrixId, f'{basePath}/dm/<string:id>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)   
