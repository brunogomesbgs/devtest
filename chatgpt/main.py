from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///elevator.db'
db = SQLAlchemy(app)


class ElevatorDemand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    floor = db.Column(db.Integer, nullable=False)
    

class ElevatorState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    floor = db.Column(db.Integer, nullable=False)
    vacant = db.Column(db.Boolean, nullable=False)


class ElevatorOrigins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    floor = db.Column(db.Integer, nullable=False)
    qtt = db.Column(db.Integer, nullable=False)


@app.route('/demand', methods=['POST'])
def create_demand():
    data = request.get_json()
    new_demand = ElevatorDemand(floor=data['floor_destiny'])
    db.session.add(new_demand)
    db.session.commit()
    origin = db.session.execute(db.select(ElevatorOrigins).where(ElevatorOrigins.floor == data['floor_origin']))
    new_origin = origin.qtt + 1
    new_origen = ElevatorOrigins(floor=data['floor_origen'], qtt=new_origin)
    db.session.add(new_origen)
    db.session.commit()
    return jsonify({'message': 'Demand created'}), 201


@app.route('/state', methods=['POST'])
def create_state():
    data = request.get_json()
    new_state = ElevatorState(floor=data['floor'], vacant=data['vacant'])
    db.session.add(new_state)
    db.session.commit()
    return jsonify({'message': 'State created'}), 201


@app.route('/prediction', methods=['GET'])
def get_prediction_floor():
    floor = db.session.execute(db.select(ElevatorOrigins).order_by(ElevatorOrigins.qtt.desc()))
    return jsonify({'data': floor}), 200


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
