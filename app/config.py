import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
                           
class Config:
    #Configuraiton class for Countries API
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "countries.db")
    
    # Disable Flask-SQLAlchemy event system to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False

