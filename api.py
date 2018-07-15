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

with open('tracks.json') as json_file_r:
    try:
        all_tracks = json.load(json_file_r)
    except json.decoder.JSONDecodeError:
        print("There is an issue with the JSON file. The server could not start.")
        exit()


def CheckTrackExists(track_id,error_redirect=True):
    track = (list(filter(lambda track: track['id'] == track_id, all_tracks)))

    if not track and error_redirect:
        abort(404, message="track {} doesn't exist".format(track_id))

    if track and not error_redirect:
        return True

def write_to_file(data):
    with open('tracks.json','w') as json_file_w:
        json_file_w.write((json.dumps(data)))

def is_int(variable_name,variable_content):
    try:
        val = int(variable_content)
    except ValueError:
        abort(400, message="{} {} is not an integer".format(variable_name,variable_content))

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
        track_id = (args['id'])
        title = (args['title'])
        artist = (args['artist'])
        duration = (args['duration'])
        last_play = (args['last_play'])

        is_int(variable_name="track_id", variable_content=track_id)
        is_int(variable_name="duration", variable_content=duration)


        if CheckTrackExists(track_id,error_redirect=False) == True:
            abort(409, message="track {} already exists".format(track_id))

        all_tracks.append({'id':track_id,
                           'title':title,
                           'artist':artist,
                           'duration':duration,
                           'last_play':last_play})

        all_tracks_sorted = sorted(all_tracks, key=lambda key: key['id'])
        write_to_file(all_tracks_sorted)
        return SingleTrack.get(self,track_id=track_id), 201


class LastPlayed(Resource):
    def get(self):
        all_tracks_sorted = sorted(all_tracks, key=lambda key: key['last_play'],reverse=True)[:100]
        return {'tracks': all_tracks_sorted}


class FilterTracks(Resource):
    def get(self,filter_text):
        filtered_list = []
        for track in all_tracks:
            title = track['title'].lower()
            if filter_text.lower() in title:
                filtered_list.append(track)
        return {'tracks': filtered_list}

api.add_resource(Track, '/tracks')
api.add_resource(SingleTrack, '/tracks/<track_id>')
api.add_resource(FilterTracks, '/tracks/filter_by_name/<filter_text>')
api.add_resource(LastPlayed, '/last_played')

if __name__ == '__main__':

    app.run(debug=True)


