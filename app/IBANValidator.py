from flask_restful import Resource
from flask_restful import reqparse
import json
import re


class IBANValidator(Resource):

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('iban_number', required=True, type=str,
                            help='iban_number is required')  # Check IBAN number exist
        args = parser.parse_args()
        # Clean IBAN number removing spaces and other non alphanumeric chars
        iban_number = self._sanitize_iban_number(args["iban_number"])
        is_valid_country = self._validate_iban_country(iban_number)

        if is_valid_country is False:
            # Check IBAN country
            return {"message": "Invalid country", "code": "INVALID_COUNTRY"}, 400

        if self._validate_iban_length(iban_number, int(is_valid_country["iban_length"])) is False:
            # Check IBAN length
            return {"message": "Invalid IBAN length", "code": "INVALID_IBAN_LENGTH"}, 400

        if self._validate_iban_format(iban_number, is_valid_country["iban_format_regex"]) is False:
            # Check IBAN format
            return {"message": "Invalid IBAN format", "code": "INVALID_IBAN_FORMAT"}, 400

        if self._validate_iban_checksum(iban_number) is False:
            # Check IBAN checksum
            return {"message": "Invalid IBAN checksum value", "code": "INVALID_IBAN_CHECKSUM"}, 400

        return {"message": "Iban number is valid", "code": "IBAN_IS_VALID"}, 200

    # Sanitize iban number
    def _sanitize_iban_number(self, iban_number):

        iban_number = iban_number.replace(" ", "")  # Remove spaces
        iban_number = iban_number.upper()  # Convert to uppercase
        iban_number = self._remove_prefix(
            iban_number, "IBAN")  # Remove IBAN Prefix if exist
        # Filter alphanumeric characters
        iban_number = ''.join(filter(str.isalnum, iban_number))

        return iban_number

    def _remove_prefix(self, text, prefix):

        if text.startswith(prefix):
            text = text.replace(prefix, "", 1)
        return text

    def _validate_iban_country(self, iban_number):

        # Check IBAN country exist
        iban_registry_file = open('iban_registry.json')
        iban_registry = json.load(iban_registry_file)
        iban_registry_file.close()

        if not (iban_registry.get(iban_number[:2]) is None):
            return iban_registry.get(iban_number[:2])

        else:
            return False

    def _validate_iban_length(self, iban_number, iban_number_length):
        # Validate length
        if len(iban_number) == iban_number_length:
            return True

        return False

    def _validate_iban_format(self, iban_number, regx_format):
        # Validate iban format
        iban_format = re.compile(regx_format, re.I)
        return bool(iban_format.match(iban_number))

    def _validate_iban_checksum(self, iban_number):

        # Validate IBAN checksum
        '''The number is then divided by 97 to obtain the remainder. The remainder is
           subtracted from 98, and the resulting two digits are the check digit pair for the
           IBAN'''

        iban_number_formated = iban_number[:2] + '00' + iban_number[4:]
        calcualted_check_digit = self._get_iban_numeric_value(
            iban_number_formated)
        format_check_digit = '{:0>2}'.format(
            98 - (int(calcualted_check_digit) % 97))

        # Get numerical representation of IBAN number
        iban_numeric_value = int(self._get_iban_numeric_value(iban_number))

        # Divided by 97. If the remainder is 1, the IBAN is valid
        if format_check_digit == iban_number[2:4] and iban_numeric_value % 97 == 1:
            return True

        return False

    def _get_iban_numeric_value(Self, iban_number):
        # Concat first for chars into last part of IBAN
        # Replace letters with standard numbers
        # Eg : SE4550000000058398257466 -> 50000000058398257466SE45 -> 50000000058398257466281445
        '''The characters are now replaced by numbers according to the following table.
        A 10 F 15 K 20 P 25 U 30
        B 11 G 16 L 21 Q 26 V 31
        C 12 H 17 M 22 R 27 W 32
        D 13 I 18 N 23 S 28 X 33
        E 14 J 19 O 24 T 29 Y 34
        Z 35 '''
        return re.sub('[A-Z]', lambda m: str(ord(m.group()) - 55), (iban_number[4:] + iban_number[:4]))
