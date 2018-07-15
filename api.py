from flask import Flask
from flask_restful import Resource, Api, abort
import json

app = Flask(__name__)

# Removes buggy 404 Helper
app.config['ERROR_404_HELP'] = False
api = Api(app)

with open('tracks.json') as json_file:
    all_tracks = json.load(json_file)


def CheckTrackExists(track_id):
    track = (list(filter(lambda track: track['id'] == track_id, all_tracks)))

    if not track:
        abort(404, message="track {} doesn't exist".format(track_id))


class Track(Resource):
    def get(self, track_id):
        CheckTrackExists(track_id)
        track = (list(filter(lambda track: track['id'] == track_id, all_tracks)))
        return {'track': track}

class TrackList(Resource):
    def get(self):
        return {'tracks': all_tracks}


api.add_resource(Track, '/track/<track_id>')
api.add_resource(TrackList, '/tracklist')

if __name__ == '__main__':

    app.run(debug=True)


