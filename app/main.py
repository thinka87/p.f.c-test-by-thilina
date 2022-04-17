from flask import Flask
from flask_restful import Api
from IBANValidator import IBANValidator
import os

app = Flask(__name__)  # Get flask app instance
api = Api(app)  # Get flask_restful Api instance

# Add post request handle to validate iban number
api.add_resource(IBANValidator, '/validate-iban')

# Custome 404 error handler with json response


@app.errorhandler(404)
def page_not_found(e):
    return {"message": e.description}, e.code

# Api Health check route


@app.route('/ping')
def hello_world():
    return 'hello'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
