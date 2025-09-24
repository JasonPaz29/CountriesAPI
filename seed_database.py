import pandas as pd
import app
from app.models import Country, Economy, Language, City, Development
from app import db, create_app

app = create_app()

# See if we can change from pandas to csv library/module
df = pd.read_csv('countries_data.csv')
with app.app_context():
    for index, row in df.iterrows():
        try:
            country = Country(
                name = row['country_name'],
                population = int(row['population']),
                capital = row['capital'],
                region = row['region']    
            )
            db.session.add(country)
            db.session.flush()
            
            economy = Economy(
                gdp=float(row['gdp_billion_usd']),  
                currency=row['currency'],
                country_id=country.id               
            )
            db.session.add(economy)
            
            languages_list = row['languages'].split(';')  # "French;English" → ["French", "English"]
            
            for lang_name in languages_list:
            # Check if language already exists
                language = Language.query.filter_by(name=lang_name).first()
                if not language:
                    language = Language(name=lang_name)
                    db.session.add(language)
                    db.session.flush()
            
                # Link language to country
                country.languages.append(language)
            #Jason Addition; not using AI at all in the beginning, and then refining with AI.
            cities_list = row['major_cities'].split(';') #Splits the major cities
            
            for city_name in cities_list:
                # city = City.query.filter_by(name=city_name, country_id=country.id).first()
                # if not city:
                city = City(
                    name=city_name.strip(),
                    country_id=country.id
                ) #population is being used a placeholder here
                db.session.add(city)
            #TODO change to DevelopmentClass    
            development = Development(
                country_id=country.id,
                development_class=row["development_class"],
                index=row['hdi_value']
            )
            db.session.add(development)
            db.session.flush()
        except Exception as e:
            print(f"Error at row {index}:{e}" )
            db.session.rollback()
            continue
    db.session.commit()
    print("All the countries were added successfully.")
    print(app.config["SQLALCHEMY_DATABASE_URI"])