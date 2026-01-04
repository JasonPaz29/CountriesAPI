from flask import Blueprint, jsonify, request
from sqlalchemy import func
from .models import Country, db, Economy, City

bp = Blueprint("api", __name__)

def filter_countries(region=None, min_population=None, name=None, min_gdp=None):
    query = Country.query
    
    if region:
        query = query.filter(Country.region.ilike("region")).all()
    
    if min_population:
        
        query = query.filter(Country.population >= min_population)

    if name:
        query.filter(Country.name.ilike("name")).all()
    
    if min_gdp:
        query = query.join(Economy).filter(Economy.gdp >= min_gdp)

    return query.all()

@bp.route("/countries", methods=["GET"]) # working on a more efficient algorithim
def get_countries_with_filters():
    region = request.args.get("region")
    min_population = request.args.get("min_population", type=int)
    name = request.args.get("name")
    min_gdp = request.args.get("min_gdp", type=int)
    
    countries = filter_countries(region=region, min_population=min_population, name=name, min_gdp=min_gdp)
    
    return jsonify([c.to_dict() for c in countries])

@bp.route("/countries/<id>", methods=["GET"])
def get_single_country(id):
    single_country = Country.query.filter_by(id=id).first()
    
    if single_country:
        return jsonify([single_country.to_dict()])
    
    return jsonify({"error": "Country with that ID does not exist."}), 400

@bp.route("/countries/top_economies", methods=["GET"])
def top_economies():
    query = Economy.query.order_by((Economy.gdp.desc()).limit(10)).all()
    
    return jsonify([c.to_dict() for c in query])

@bp.route("/countries/<id>/cities", methods=["GET"])
def get_country_cities(id):
    cities = City.query.filter_by(country_id=id).first()
    
    if cities:
        return jsonify([c.to_dict() for c in cities])
    
    return jsonify({"error": "Country with that ID does not exist"}), 400
    
@bp.route("/countries/most_populated_countries", methods=['GET'])
def populated_countries():
    query = Country.query.order_by((Country.population.desc()).limit(15)).all()
    
    return jsonify([c.to_dict() for c in query])

@bp.route('/countries/capital/<capital>', methods=['GET'])
def countries_capital(capital):
    query = Country.query.filter(Country.capital == capital).first()
    
    return jsonify([query.to_dict()])

@bp.route('/countries/compare/<id1>/<id2>', methods=["GET"])
def compare_countries(id1, id2):
    query1 = Country.query.filter(Country.id == id1).first()
    query2 = Country.query.filter(Country.id == id2).first()
    
    return jsonify([query1.to_dict_full(), query2.to_dict_full()])

@bp.route('/countries/bottom_economies', methods="GET")
def bottom_economies():
    query = Economy.query.filter_by((Economy.gdp.asc()).limit(10)).all()
    
    return jsonify([c.to_dict() for c in query])
#EXPAND THIS FUNCTION LATER
@bp.route("/economies", methods=["GET"])
def economies_with_filters():
    query = Economy.query
    
    currency = request.args.get("currency")
    
    if currency:
        query = query.filter(Economy.currency == currency).all()
        
    return jsonify([c.to_dict() for c in query])

@bp.route('/economies/stats', method=['GET'])
def economies_stats():
    avg_gdp = db.session.query(func.avg(Economy.gdp)).scalar()
    
    region_avgs = (
        db.session.query(Country.region, func.avg(Economy.gdp))
        .join(Economy)
        .group_by(Country.region)
        .all()
    )
    richest_region = max(region_avgs, key=lambda x: x[1])

    return jsonify({
    "region_averages": {r: round(avg, 2) for r, avg in region_avgs},
    "richest_region": {
        "region": richest_region[0],
        "average_gdp": round(richest_region[1], 2)
    }
})


    