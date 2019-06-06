from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)


class woodenGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    weight = db.Column(db.Integer)
    material = db.Column(db.String(40))
    height = db.Column(db.Integer)
    price = db.Column(db.Integer)
    producer = db.Column(db.String(40))
    width = db.Column(db.Integer)

    def __init__(self, name="noName", weight=0, material="noMaterial", height=0, price=0, producer="noProducer", width=0,
                length=0):
        self.name = name
        self.weight = weight
        self.material = material
        self.height = height
        self.price = price
        self.producer = producer
        self.width = width
        self.length = length

    def __str__(self):
        return ('The item is called {0}, it weights {1} kg, made of {2}'
                + 'height = {3} sm, price = '
                + ' {4}$, it\'s produced by {5}, width = {6} sm \n').format(self.name,
                                                                            self.weight,
                                                                            self.height,
                                                                            self.price,
                                                                            self.producer,
                                                                            self.width, )


class woodenGoodsSchema(ma.Schema):
    
    class Meta:
        fields = ('id', 'name', 'weight',
                  'material', 'height', 'price', ' producer', 'width', 'length')


wooden_good_schema = woodenGoodsSchema()
wooden_goods_schema = woodenGoodsSchema(many=True)


@app.route('/woodenGoods', methods=['POST'])
def add_woodenGoods():
    name = request.json['name']
    weight = request.json['weight']
    material = request.json['material']
    height = request.json['height']
    price = request.json['price']
    producer = request.json['producer']
    width = request.json['width']

    new_woodenGoods = woodenGoods(name, weight, material,
                                height, price, producer, width)

    db.session.add(new_woodenGoods)
    db.session.commit()

    return wooden_good_schema.jsonify(new_woodenGoods)


@app.route('/woodenGoods', methods=['GET'])
def get_all_woodenGoods():
    all_woodenGoods = woodenGoods.query.all()
    result = wooden_goods_schema.dump(all_woodenGoods)
    return jsonify(result)


@app.route('/woodenGoods/<e_id>', methods=['GET'])
def get_woodenGoods(e_id):
    woodenGood = woodenGoods.query.get(e_id)
    result = wooden_good_schema.dump(woodenGood)
    return jsonify(result)


@app.route('/woodenGoods/<e_id>', methods=['DELETE'])
def delete_all_woodenGoods(e_id):
    db.session.delete(woodenGoods.query.get(e_id))
    db.session.commit()
    return jsonify(f'Object with id {e_id} is deleted!')


@app.route('/woodenGoods/<e_id>', methods=['PUT'])
def update_woodenGoods(e_id):
    woodenGood = woodenGoods.query.get(e_id)
    name = request.json['name']
    weight = request.json['weight']
    material = request.json['material']
    height = request.json['height']
    price = request.json['price']
    producer = request.json['producer']
    width = request.json['width']

    woodenGood.name = name
    woodenGood.weight = weight
    woodenGood.material = material
    woodenGood.height = height
    woodenGood.price = price
    woodenGood.producer = producer
    woodenGood.width = width

    db.session.commit()
    return wooden_good_schema.jsonify(woodenGood)


if __name__ == '__main__':
    app.run(debug=True)