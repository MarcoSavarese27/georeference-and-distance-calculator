from flask import Flask
from flask_restful import Api
from georeference.resource import Georeference, GeoreferenceId
from distancematrix.resource import DistanceMatrix, DistanceMatrixId


app = Flask(__name__)
api = Api(app)
base_path = '/api/v1'

api.add_resource(Georeference, f'{base_path}/georef')
api.add_resource(GeoreferenceId, f'{base_path}/georef/<string:id>')
api.add_resource(DistanceMatrix, f'{base_path}/dm')
api.add_resource(DistanceMatrixId, f'{base_path}/dm/<string:id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)   