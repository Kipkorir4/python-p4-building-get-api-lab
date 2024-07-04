#!/usr/bin/env python3

from flask import Flask, jsonify, abort
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries_list = Bakery.query.all()
    bakeries_json = [bakery.to_dict() for bakery in bakeries_list]
    return jsonify(bakeries_json)

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get(id)
    if not bakery:
        abort(404, description="Bakery not found")
    bakery_json = bakery.to_dict()
    
    bakery_json['baked_goods'] = [bg.to_dict() for bg in bakery.baked_goods]
    return jsonify(bakery_json)

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_list = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_json = [bg.to_dict() for bg in baked_goods_list]
    return jsonify(baked_goods_json)

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if most_expensive:
        return jsonify(most_expensive.to_dict())
    return jsonify({"message": "No baked goods found"}), 404

if __name__ == '__main__':
    app.run(port=5555, debug=True)
