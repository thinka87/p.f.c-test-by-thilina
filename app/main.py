from flask import Flask
from flask_restful import Api
from IBANValidator import IBANValidator

app = Flask(__name__) # Get flask app instance
api = Api(app) # Get flask_restful Api instance

api.add_resource(IBANValidator,'/validate-iban') # Add post request handle to validate iban number

if __name__ == "__main__":
    app.run()