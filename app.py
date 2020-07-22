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
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)

    def __init__(self, address, city, state, zipcode):
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode


class ListingSchema(ma.Schema):
    class Meta:
        fields = ("id", "address", "city", "state", "zipcode")


listing_schema = ListingSchema()
listings_schema = ListingSchema(many=True)


@app.route("/listing/add", methods=["POST"])
def add_listing():
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

    
    post_data = request.get_json()
    address = post_data.get("address")
    city = post_data.get("city")
    state = post_data.get("state")
    zipcode = post_data.get("zipcode")


    record = Listing(address, city, state, zipcode)
    db.session.add(record)
    db.session.commit()

    return jsonify("Listing Added")


@app.route("/listing/get", methods=["GET"])
def get_all_listings():
    all_listings = db.session.query(Listing).all()
    return jsonify(listings_schema.dump(all_listings))


@app.route("/listing/get/<id>", methods=["GET"])
def get_listing_by_id(id):
    listing = db.session.query(Listing).filter(Listing.id == id).first()
    return jsonify(listing_schema.dump(listing))


@app.route("/listing/delete/<id>", methods=["DELETE"])
def delete_listing_by_id(id):
    listing = db.session.query(Listing).filter(Listing.id == id).first()
    db.session.delete(listing)
    db.session.commit()
    return jsonify("Listing Deleted")


@app.route("/listing/update/<id>", methods=["PUT"])
def update_listing_by_id(id):
    if request.content_type != "application/json":
        return jsonify("Error: Data must be sent as JSON")

        put_data = request.get_json()
        address = put_data.get("address")
        city = put_data.get("city")
        state = put_data.get("state")
        zipcode = put_data.get("zipcode")

        listing = db.session.query(Listing).filter(Listing.id == id).first()
        listing.address = address
        listing.city = city
        listing.state = state
        listing.zipcode = zipcode

        db.session.commit()

    return jsonify("Listing Updated")




if __name__ == "__main__":
    app.run(debug=True)