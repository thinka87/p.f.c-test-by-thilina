from flask_restful import Resource
from flask_restful import reqparse
import json

class IBANValidator(Resource):

    def post(self):

            parser = reqparse.RequestParser()
            parser.add_argument('iban_number', required=True, type=str, help='iban_number is required')
            args = parser.parse_args()
            iban_number= self._sanitize_iban_number(args["iban_number"])
            is_valid_country =self._validate_iban_country(iban_number)

            if is_valid_country is False:
                return {"message" : "Invalid country","code" : "INVALID_COUNTRY" }, 400
            
            if self._validate_iban_length(iban_number,int(is_valid_country["iban_length"])) is False:
                return {"message" : "Invalid IBAN length","code" : "INVALID_IBAN_LENGTH" }, 400

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
    
    def _validate_iban_country(self ,iban_number):


        iban_registry_file = open('iban_registry.json') 
        iban_registry = json.load(iban_registry_file)
        iban_registry_file.close()

        if not (iban_registry.get(iban_number[:2]) is None):
            return iban_registry.get(iban_number[:2])
            
        else:
            return False
    
    def _validate_iban_length(self,iban_number,iban_number_length):

        if len(iban_number) == iban_number_length:
            return True
        
        return False