#Start the web server and make it accesible
from app import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
    
    

