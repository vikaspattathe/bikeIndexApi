from flask import Flask, request
from flask_restx import Api, Resource, fields, Namespace
from datetime import datetime, timedelta
from bike_index import BikeIndex

app = Flask(__name__)
bi = BikeIndex()

api = Api(app, version='1.0', title='Bike Index for Bonafi', description='API to search and filter stolen bikes from BikeIndex website.',)

ns = Namespace('bikeindex', description='search operations')
api.add_namespace(ns)
# Define models for API documentation
bike_model = api.model('Bike', {
    'id': fields.Integer(description='Bike ID'),
    'manufacturer_name': fields.String(description='Manufacturer Name'),
    'manufacturer_details': fields.String(description='Manufacturer details'),
    'date_stolen': fields.String(description='Date Stolen (DD-MM-YYYY)'),
    'image_base64': fields.String(description='Image in base64 encoding'),
    'description': fields.String(description='Description of the listing'),
    'frame_colors': fields.List(fields.String, description='Frame colors'),
    'frame_model': fields.String(description=''),
    'is_stock_img': fields.Boolean(description='Stock image or not'),
    'large_img': fields.String(description='Image url'),
    'location_found': fields.String(description='Location found'),
    'manufacturer_name': fields.String(description='Manufacturer Name'),
    'external_id': fields.Integer(description='External ID'),
    'registry_name': fields.String(description='Registry Name'),
    'registry_url': fields.String(description='Registry URL'),
    'serial': fields.String(description='Serial number of the bike'),
    'status': fields.String(description='Status - Stolen or Not'),
    'stolen': fields.Boolean(description='Stolen or not'),
    'stolen_coordinates': fields.List(fields.Integer,description='Stolen Coordinates'),
    'stolen_location': fields.String(description='Stolen Location'),
    'thumb': fields.String(description='Thumbnail url'),
    'title': fields.String(description='Title of the ad'),
    'url': fields.String(description='URL of the ad'),
    'year': fields.Integer(description='Year of Manufacture'),
    'propulsion_type_slug': fields.String(description='Propulsion Type'),
    'cycle_type_slug': fields.String(description='Cycle Type')
})

@ns.route('/search')
class BikeSearch(Resource):
    @ns.doc(params={
        'location': 'Search location (IP location by default)',
        'duration': 'Duration in months (Default is 6 months)',
        'manufacturer': 'Manufacturer name',
        'distance': 'Range in kms (Default is 10Km)'
    })
    @api.response(200, 'Success', [bike_model])
    def get(self):
        location = request.args.get('location')
        duration = int(request.args.get('duration', 6))
        manufacturer = request.args.get('manufacturer', '')
        distance = request.args.get('distance', 10)
        if not location:
            location = request.remote_addr

        try:
            results = bi.search(location, distance, manufacturer,duration)
            response_data = {
                'number of bikes': len(results),
                'bikes': results
            }
            return response_data, 200
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return {'error': error_message}, 500

if __name__ == '__main__':
    app.run(debug=True)
