# IBAN Validation API using python flask


## Technologies
***
A list of technologies used within the project:
* python3, flask, flask_restful
* Docker
* cypress js (for testing)
* npm (node package manager)
* node js

## How to setup the project
***
Steps
* clone the repositery
* in terminal run -> npm install
* to run the api without docker  ->  npm run build, then -> npm start , it will start api on  "http://localhost:5000/"
* to run the api with docker  ->  npm run build-docker-image , it will start docker contatiner on port 5000, you access to api using "http://localhost:5000/"
* api document - https://documenter.getpostman.com/view/1510812/Uyr5oK1a
* you can find postman collection from "PFC_IBAN_VALIDATOR_API_BY_THILINA.postman_collection.json"
* To valiadate an IBAN number send a POST request to "http://localhost:5000/validate-iban" including below json body
* {
    "iban_number": "AL47212110090000000235698741"
  }
  
* Content-Type heder should be application/json
* To more detailes about the API , Please refer api document url

## How to run test cases
***
* config apiUrl base url in cypress.json
* in terminal run -> npm test
* you see the test output in cypress folder
* you can find api test case file inside cypress/integration/iban_api.spec.js

## References
***
*  https://www.fsc.gi/uploads/legacy/download/adobe/banking/Note07.pdf
*  https://www.iban.com/

## Notes
***
* To run the npm start command in windows, please change the command as "cd app && set FLASK_APP=main.py && python3 -m flask run" in package.json file
