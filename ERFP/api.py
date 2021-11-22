from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import json, os , requests

app = Flask(__name__)
api = Api(app)

IMDB_key = ""

class MoviePosterService(Resource):
    
    def get(self):
        json_data = request.get_json(force=True)
        ID = json_data["imdb_id"]
        #print(f"imdb_id: {ID}")
        
        request_string = "https://imdb-api.com/en/API/Posters/" + IMDB_key + "/" + ID
        response = requests.get(request_string)
        print(response.text)
        response_json = response.json()
        
        return_dict = {"poster": response_json }
        return return_dict
        

api.add_resource(MoviePosterService, '/poster')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6000)) 
    app.run(port=port, debug=True)
    
