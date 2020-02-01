from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

# CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Card(db.Model):
    _tablename__ = "cards"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    # price = db.Column(db.Numeric(10, 2))
    # offer = db.Column(db.Numeric(10, 2))
    price = db.Column(db.String(20))
    offer = db.Column(db.String(20))
    image_url = db.Column(db.String(500))

    def __init__(self, name, price, offer, image_url):
        self.name = name
        self.price = price
        self.offer = offer
        self.image_url = image_url


class CardSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "offer", "image_url")


card_schema = CardSchema()
cards_schema = CardSchema(many=True)


@app.route("/")
def greeting():
    return "<h1>Card Seller API<h1>"


#POST
@app.route("/add-card", methods=["POST"])
def add_card():
    name = request.json["name"]
    price = request.json["price"]
    offer = request.json["offer"]
    image_url = request.json["image_url"]

    new_card = Card(name, price, offer, image_url)

    db.session.add(new_card)
    db.session.commit()

    return jsonify("Card POSTED")


#GET all cards
@app.route("/cards", methods=["GET"])
def get_cards():
    all_cards = Card.query.all()
    result = cards_schema.dump(all_cards)

    return jsonify(result)


#GET one card
@app.route("/card/<id>", methods=["GET"])
def get_card(id):
    card = Card.query.get(id)

    return card_schema.jsonify(card)


#PUT
@app.route("/card/<id>", methods=["PUT"])
def update_card(id):
    card = Card.query.get(id)
    name = request.json['name']
    price = request.json['price']
    offer = request.json['offer']
    image_url = request.json['image_url']

    card.name = name
    card.price = price
    card.offer = offer
    card.image_url = image_url

    db.session.commit()
    return card_schema.jsonify(card)


#DELETE a card
@app.route("/card/<id>", methods=["DELETE"])
def delete_card(id):
    card = Card.query.get(id)

    db.session.delete(card)
    db.session.commit()

    return "CARD WAS SUCCESSFULLY DELETED"


if __name__ == "__main__":
    app.debug = True
    app.run()