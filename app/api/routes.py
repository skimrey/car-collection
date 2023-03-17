from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')
# add car
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):

    
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    serial = request.json['serial']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(make, model, serial, year, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

# display all cars
@api.route('/cars', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    cars = Car.query.filter_by(user_token = a_user).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

# display single car
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_contact_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

#update car
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    car = Car.query.get(id) 
    car.name = request.json['name']
    car.email = request.json['email']
    car.phone_number = request.json['phone_number']
    car.address = request.json['address']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

# delete car
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)