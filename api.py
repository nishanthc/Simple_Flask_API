from flask import Flask
from flask_restful import Resource, Api, abort
import json

app = Flask(__name__)
api = Api(app)
with open('tracks.json') as json_file:
    all_tracks = json.load(json_file)

class TrackList(Resource):
    def get(self):
        return {'tracks': all_tracks}

api.add_resource(TrackList, '/tracklist')

if __name__ == '__main__':

    app.run(debug=True)