from flask_restful import Resource
from flask_restful import reqparse

class IBANValidator(Resource):

    def post(self):

            parser = reqparse.RequestParser()
            parser.add_argument('iban_number', required=True, type=str, help='iban_number is required')
            args = parser.parse_args()
