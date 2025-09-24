from . import db


#Many to Many association table.
country_language = db.Table("country_language",
        db.Column("country_id", db.Integer, db.ForeignKey("country.id"), primary_key=True),
        db.Column("language_id", db.Integer, db.ForeignKey("language.id"), primary_key=True)
        )   

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    capital = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    region = db.Column(db.String(50), nullable=False)
    
    cities = db.relationship("City", back_populates="country")
    economy = db.relationship("Economy", back_populates="country", uselist=False)
    languages = db.relationship("Language", secondary=country_language, back_populates="countries")
    humanIndex = db.relationship("Development", back_populates="country", uselist=False)
    
    #TODO fix to_dict logic as it is very flawed.
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "capital": self.capital,
            "population": self.population,
            "region": self.region
        }
                
    def to_dict_full(self):
        return {
            **self.to_dict(),
            "economy": self.economy.to_dict() if self.economy else None,
            "cities": [c.to_dict() for c in self.cities],
            "languages": [l.to_dict() for l in self.languages],
            "humanIndex": self.index.to_dict() if self.index else None
        }


class Economy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gdp = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(50), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"), unique=True)
    country = db.relationship("Country", back_populates="economy")
    def to_dict(self):
        return {
            "id": self.id,
            "gdp": self.gdp,
            "currency": self.currency,
            "country_id": self.country_id
        }

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    countries = db.relationship("Country", secondary=country_language, back_populates="languages")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "countries": [c.id for c in self.countries]
        }

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"))
    country = db.relationship("Country", back_populates="cities")
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country_id": self.country_id
        }
    
#this class was made with no AI
class Development(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"))
    development_class = db.Column(db.String(150), nullable=True)
    index = db.Column(db.Float, nullable=True)
    
    country = db.relationship("Country", back_populates="humanIndex")

    def to_dict(self):
        return {
            "id": self.id,
            "development_class": self.development_class,
            "index": self.index,
            "country_id": self.country_id
        }
