from flask import Flask
from flask_restful import Api
from IBANValidator import IBANValidator
import os

app = Flask(__name__) # Get flask app instance
api = Api(app) # Get flask_restful Api instance

api.add_resource(IBANValidator,'/validate-iban') # Add post request handle to validate iban number

@app.errorhandler(404)
def page_not_found(e):
    return {"message": e.description}, e.code

@app.route('/ping')
def hello_world():
    return 'hello'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))