from flask import Flask
from flask_restful import reqparse, Resource, Api, abort
import json

app = Flask(__name__)

# Removes buggy 404 Helper
app.config['ERROR_404_HELP'] = False
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('artist')
parser.add_argument('duration')
parser.add_argument('last_play')

with open('tracks.json') as json_file:
    all_tracks = json.load(json_file)


def CheckTrackExists(track_id):
    track = (list(filter(lambda track: track['id'] == track_id, all_tracks)))

    if not track:
        abort(404, message="track {} doesn't exist".format(track_id))


class SingleTrack(Resource):
    def get(self, track_id):
        CheckTrackExists(track_id)
        track = (list(filter(lambda track: track['id'] == track_id, all_tracks)))
        return {'track': track}

    def post(self):
        args = parser.parse_args()
        args['task']
        return args['task'], 201

class Track(Resource):

    def get(self):
        return {'tracks': all_tracks}

    def post(self):
        args = parser.parse_args()
        return args['id'].decode, 201


class TrackList(Resource):
    def get(self):
        return {'tracks': all_tracks}

api.add_resource(Track, '/tracks')
api.add_resource(SingleTrack, '/tracks/<track_id>')
api.add_resource(TrackList, '/tracklist')

if __name__ == '__main__':

    app.run(debug=True)


