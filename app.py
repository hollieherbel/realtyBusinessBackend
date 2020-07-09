from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://wqabsnnealqdno:c5a7cfae8f5385de99afa2db3b17b8026e71f8ac74f28652b62b94a5dc63473d@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dpngfh52qj1s2"

db = SQLAlchemy(app)
ma = Marshmallow(app)

heroku = Heroku(app)
CORS(app)


class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(), nullable=False, unique=True)
    city = db.Column(db.String(), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    def __init__(self, address, city, zipcode):
        self.address = address
        self.city = city
        self.zipcode = zipcode


class ListingSchema(ma.Schema):
    class Meta:
        fields = ("id", "address", "city", "zipcode")


listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)




