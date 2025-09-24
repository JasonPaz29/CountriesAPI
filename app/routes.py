from flask import Blueprint, jsonify, request
from .models import Country, db, Economy, City

bp = Blueprint("api", __name__)

@bp.route("/countries", methods=["GET"]) # working on a more efficient algorithim
def get_countries_with_filters():
    query = Country.query
    
    region = request.args.get("region")
    if region:
        query = query.filter(Country.region.ilike("region")).all()
    
    min_population = request.args.get("min_population")
    if min_population:
        try:
            min_population = int(min_population)
            query = query.filter(Country.population >= min_population)
        except ValueError:
            return jsonify({"error": "min_population MUST be an integer."}), 400
    name = request.args.get("name")
    if name:
        query.filter(Country.name.ilike("name")).all()
        
    
    countries = query.all()
    
    return jsonify([c.to_dict() for c in countries])

@bp.route("/countries/<id>", methods=["GET"])
def get_single_country(id):
    single_country = Country.query.filter_by(id=id).first()
    
    if single_country:
        return jsonify([single_country.to_dict()])
    
    return jsonify({"error": "Country with that ID does not exist."}), 400

#Trying to figure out Top 10 logic, with no AI at first.
@bp.route("/countries/top_economies", methods=["GET"])
def top_economies():
    query = Economy.query.order_by((Economy.gdp.desc()).limit(10)).all()
    
    return jsonify(c.to_dict() for c in query)

@bp.route("/countries/<id>/cities", methods=["GET"])
def get_country_cities(id):
    cities = City.query.filter_by(country_id=id).first()
    
    if cities:
        return jsonify([c.to_dict() for c in cities])
    
    return jsonify({"error": "Country with that ID does not exist"}), 400
    