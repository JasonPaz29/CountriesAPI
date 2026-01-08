from flask import Blueprint, jsonify, request
from sqlalchemy import func
from .models import Country, db, Economy, City, Development, Language

bp = Blueprint("api", __name__)

def filter_countries(region=None, min_population=None, name=None, min_gdp=None):
    query = Country.query
    
    if region:
        query = query.filter(Country.region.ilike(f"%{region}%"))
    
    if min_population is not None:
        query = query.filter(Country.population >= min_population)

    if name:
        query = query.filter(Country.name.ilike(f"%{name}%"))
    
    if min_gdp is not None:
        query = query.join(Economy).filter(Economy.gdp >= min_gdp)

    return query.all()

@bp.route("/countries", methods=["GET"]) # working on a more efficient algorithim
def get_countries_with_filters():
    region = request.args.get("region")
    min_population = request.args.get("min_population", type=int)
    name = request.args.get("name")
    min_gdp = request.args.get("min_gdp", type=float)
    
    countries = filter_countries(region=region, min_population=min_population, name=name, min_gdp=min_gdp)
    
    return jsonify([c.to_dict() for c in countries])

@bp.route("/countries/<int:id>", methods=["GET"])
def get_single_country(id):
    single_country = Country.query.get(id)
    
    if single_country:
        return jsonify(single_country.to_dict())
    
    return jsonify({"error": "Country with that ID does not exist."}), 404

@bp.route("/countries/top_economies", methods=["GET"])
def top_economies():
    query = Economy.query.order_by(Economy.gdp.desc()).limit(10).all()
    
    return jsonify([c.to_dict() for c in query])

@bp.route("/countries/<int:id>/cities", methods=["GET"])
def get_country_cities(id):
    country = Country.query.get(id)
    
    if country:
        return jsonify([c.to_dict() for c in country.cities])
    
    return jsonify({"error": "Country with that ID does not exist"}), 404
    
@bp.route("/countries/most_populated_countries", methods=['GET'])
def populated_countries():
    query = Country.query.order_by(Country.population.desc()).limit(15).all()
    
    return jsonify([c.to_dict() for c in query])

@bp.route('/countries/capital/<capital>', methods=['GET'])
def countries_capital(capital):
    query = Country.query.filter(Country.capital.ilike(f"%{capital}%")).first()
    
    if not query:
        return jsonify({"error": "Country with that capital does not exist."}), 404
    
    return jsonify(query.to_dict())

@bp.route("/countries/compare/<int:id1>/<int:id2>", methods=["GET"])
def compare_countries(id1, id2):
    query1 = Country.query.get(id1)
    query2 = Country.query.get(id2)
    
    if not query1 or not query2:
        return jsonify({"error": "One or both countries do not exist."}), 404
    
    return jsonify([query1.to_dict_full(), query2.to_dict_full()])

@bp.route("/countries/bottom_economies", methods=["GET"])
def bottom_economies():
    query = Economy.query.order_by(Economy.gdp.asc()).limit(10).all()
    
    return jsonify([c.to_dict() for c in query])
#EXPAND THIS FUNCTION LATER
@bp.route("/economies", methods=["GET"])
def economies_with_filters():
    query = Economy.query
    
    currency = request.args.get("currency")
    
    if currency:
        query = query.filter(Economy.currency == currency)
        
    return jsonify([c.to_dict() for c in query.all()])

@bp.route("/economies/stats", methods=["GET"])
def economies_stats():
    avg_gdp = db.session.query(func.avg(Economy.gdp)).scalar()
    
    region_avgs = (
        db.session.query(Country.region, func.avg(Economy.gdp))
        .join(Economy)
        .group_by(Country.region)
        .all()
    )
    richest_region = max(region_avgs, key=lambda x: x[1]) if region_avgs else None

    return jsonify(
        {
            "region_averages": {r: round(avg, 2) for r, avg in region_avgs},
            "richest_region": {
                "region": richest_region[0],
                "average_gdp": round(richest_region[1], 2),
            }
            if richest_region
            else None,
            "average_gdp": round(avg_gdp, 2) if avg_gdp is not None else None,
        }
    )

@bp.route('/cities/largest', methods=['GET'])
def largest_cities():
    query = City.query.order_by(City.population.desc()).limit(10).all()
    
    return jsonify([c.to_dict() for c in query])

@bp.route("/cities/smallest", methods=["GET"])
def smallest_cities():
    query = City.query.order_by(City.population.asc()).limit(10).all()
    
    return jsonify([c.to_dict() for c in query])


@bp.route("/countries/<id>/development")
def get_country_with_development(id):
    development = Development.query.filter_by(country_id=id).first()
    if not development:
        return jsonify({"error": "Development data for that country does not exist."}), 404
    
    return jsonify(development.to_dict())

@bp.route("/development/highest_hdi", methods=["GET"])
def highest_hdi_countries():
    query = Development.query.order_by(Development.index.desc()).limit(10).all()
    
    return jsonify([d.to_dict() for d in query])

@bp.route("/development/lowest_hdi", methods=["GET"])
def lowest_hdi_countries():
    query = Development.query.order_by(Development.index.asc()).limit(10).all()
    
    return jsonify([d.to_dict() for d in query])

@bp.route("/development/average_hdi", methods=["GET"])
def average_hdi():
    avg_hdi = db.session.query(func.avg(Development.index)).scalar()
    
    if not avg_hdi:
        return jsonify({"error": "No HDI data available."}), 404
    
    return jsonify({"average_hdi": round(avg_hdi, 3)})

@bp.route("/economies/currency/<currency>", methods=["GET"])
def economies_by_currency(currency):
    query = Economy.query.filter(Economy.currency.ilike(f"%{currency}%")).all()
    
    if not query:
        return jsonify({"error": "No economies found with that currency."}), 404
    
    return jsonify([e.to_dict() for e in query])

@bp.route("/economies/average_gdp", methods=["GET"])
def average_gdp():
    avg_gdp = db.session.query(func.avg(Economy.gdp)).scalar()
    
    if not avg_gdp:
        return jsonify ({"error": "No GDP data available."}), 404

    return jsonify([g.to_dict() for g in avg_gdp])

@bp.route("/languages", methods=["GET"])
def languages():
    query = Language.query.all()
    
    if not query:
        return jsonify({"error": "Language data is missing!"}), 404
    
    return jsonify([l.to_dict() for l in query])

@bp.route("/counties/language/<language>", methods=["GET"])
def countries_by_language(language):
    lang = Language.query.filter(Language.name.ilike(f"%{language}%")).first()
    
    if not lang:
        return jsonify({"error": "No countries found with that language."}), 404
    
    return jsonify([c.to_dict() for c in lang.countries])
