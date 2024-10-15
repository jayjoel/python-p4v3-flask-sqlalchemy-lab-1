# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

@app.route('/earthquakes/<int:id>')
def find_earthquake(id):    
    returned_earthquake = Earthquake.query.filter_by(id=id).first()
    
    if returned_earthquake:
        response_body = {
            "id": returned_earthquake.id,
            "location": returned_earthquake.location,
            "magnitude": returned_earthquake.magnitude,
            "year": returned_earthquake.year
        }
        
        return jsonify(response_body), 200
    else:
        error_message = {
            "message": f"Earthquake {id} not found."
        }
        return jsonify(error_message), 404
    
@app.route('/earthquakes/magnitude/<float:magnitude>')
def find_minimum_magnitude(magnitude):
    minimum_magnitude_earthquakes = Earthquake.query.filter(Earthquake.magnitude>=magnitude).all()
    
    if minimum_magnitude_earthquakes:
        response_body = {
            "count": len(minimum_magnitude_earthquakes),
            "quakes": [
                {
                    "id": earthquake.id,
                    "location": earthquake.location,
                    "magnitude": earthquake.magnitude,
                    "year": earthquake.year                    
                } for earthquake in minimum_magnitude_earthquakes
            ]
            
        } 
        return jsonify(response_body), 200
    else:
        response_body = {
            "count": 0,
            "quakes": []
        } 
        return jsonify(response_body), 200      
    

if __name__ == '__main__':
    app.run(port=5555, debug=True)