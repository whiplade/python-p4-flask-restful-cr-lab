#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    
    def get(self):
        
        plants = Plant.query.all()
        plant_data = []
        for plant in plants:
            plant_data.append({
                'id': plant.id,
                'name': plant.name,
                'image': plant.image,
                'price': plant.price
            })

        return jsonify(plant_data)
     
    def post(self):

        data = request.json

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price']
        )

        db.session.add(new_plant)
        db.session.commit()

        return jsonify({"message": "Plant record created successfully"}), 201

api.add_resource(Plants, '/plants')

class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.get(id)

        if plant is None:
            return jsonify({"error": "Plant not found"}), 404

        plant_data = {
            'id': plant.id,
            'name': plant.name,
            'image': plant.image,
            'price': plant.price
        }

        return jsonify(plant_data)
    
api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
