import re
from time import strptime
from flask_restful import Resource
from flask_restful import reqparse

class IBANValidator(Resource):

    def post(self):

            parser = reqparse.RequestParser()
            parser.add_argument('iban_number', required=True, type=str, help='iban_number is required')
            args = parser.parse_args()
            return self._sanitize_iban_number(args["iban_number"])

    def _sanitize_iban_number(self,iban_number):

        iban_number = iban_number.replace(" ", "")
        iban_number =iban_number.upper()
        iban_number =self._remove_prefix(iban_number,"IBAN")
        iban_number = ''.join(filter(str.isalnum, iban_number))

        return iban_number

    def _remove_prefix(self,text, prefix):

        if text.startswith(prefix):
            text = text.replace(prefix, "", 1)
        return text
