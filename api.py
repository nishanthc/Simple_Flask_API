from collections import Counter
from datetime import datetime
from flask import Flask
from flask_restful import reqparse, Resource, Api, abort
import json

app = Flask(__name__)

# Removes buggy 404 Helper
app.config['ERROR_404_HELP'] = False
api = Api(app)

# Arguments to catch
parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('title')
parser.add_argument('artist')
parser.add_argument('duration')
parser.add_argument('last_play')

# Load JSON File
with open('tracks.json') as json_file_r:
    try:
        all_tracks = json.load(json_file_r)
    except json.decoder.JSONDecodeError:
        # If the JSON file cannot be read exit cleanly
        print("There is an issue with the JSON file. The server could not start.")
        exit()


def checkTrackExists(track_id, error_redirect=True):
    """Return True if track does not exist, if error_redirect=true and track doesn't exist then 404.
    """

    # Attempt to isolate track from the list of all tracks
    track = (list(filter(lambda track: track['id'] == track_id, all_tracks)))
    if not track and error_redirect:
        abort(404, message="track {} doesn't exist".format(track_id))

    if track and not error_redirect:
        return True


def write_to_file(data):
    """Write new data to the JSON file
    """

    # Add exception handling!
    with open('tracks.json', 'w') as json_file_w:
        json_file_w.write((json.dumps(data)))


def is_int(variable_name, variable_content):
    """Checks if a variable is an integer or not
    """
    try:
        int(variable_content)
    except ValueError:
        abort(400, message="{} {} is not an integer".format(variable_name, variable_content))


class SingleTrack(Resource):
    """Returns details of a single track using the get method

    """

    def get(self, track_id):
        checkTrackExists(track_id)
        track = (list(filter(lambda track: track['id'] == track_id, all_tracks)))
        return {'track': track}


class Track(Resource):
    """The get method returns a list of all tracks
       The post method can be used to create a new track.
    """

    def get(self):
        return {'tracks': all_tracks}

    def post(self):
        args = parser.parse_args()
        track_id = (args['id'])
        title = (args['title'])
        artist = (args['artist'])
        duration = (args['duration'])
        last_play = (args['last_play'])

        # Check if track_id and duration are integers
        is_int(variable_name="track_id", variable_content=track_id)
        is_int(variable_name="duration", variable_content=duration)

        if checkTrackExists(track_id, error_redirect=False):
            abort(409, message="track {} already exists".format(track_id))

        all_tracks.append({'id': track_id,
                           'title': title,
                           'artist': artist,
                           'duration': duration,
                           'last_play': last_play})

        all_tracks_sorted = sorted(all_tracks, key=lambda key: key['id'])
        write_to_file(all_tracks_sorted)
        return SingleTrack.get(self, track_id=track_id), 201


class LastPlayed(Resource):
    """Using the get method, this can be used to list the last 100 played tracks.
    """

    def get(self):
        all_tracks_sorted = sorted(all_tracks, key=lambda key: key['last_play'], reverse=True)[:100]
        return {'tracks': all_tracks_sorted}, 200


class FilterTracks(Resource):
    """Using the get method with an argument (filter_text) to return all tracks with a similar title as the filter_text
        """

    def get(self, filter_text):
        filtered_list = []
        for track in all_tracks:
            title = track['title'].lower()
            if filter_text.lower() in title:
                filtered_list.append(track)
        return {'tracks': filtered_list}, 200


class Artists(Resource):
    """With the GET method this will return a list of artists with their total number of tracks and most recently
        played track.
        """

    def get(self):
        list_of_artists = []
        artist_last_played_datetime = {}
        artist_last_played_track_title = {}
        artists_with_data = []

        # Loop through all tracks
        for track in all_tracks:

            list_of_artists.append((track['artist']))  # Adding artists to a list of artists
            artist = track['artist']
            title = track['title']
            datetimestamp_from_file = track['last_play']  # Date/time string from file

            # Converts string date/time into a real Datetime
            last_played_of_track_from_file = datetime.strptime(datetimestamp_from_file, '%Y-%m-%d %H:%M:%S')

            # If the artist is not yet in the list for holding artists last played datetime then put it in
            if artist not in artist_last_played_datetime:
                # Store date/time string in dictionary
                artist_last_played_datetime[artist] = datetimestamp_from_file
                # Adds title of the track to the dictionary
                artist_last_played_track_title[artist] = title

            # Converts string datetime back to a Datetime
            datetime_from_array = datetime.strptime(artist_last_played_datetime[artist], '%Y-%m-%d %H:%M:%S')

            # If the Datetime from the file is later than in the array overwrite it and add the title of the track
            if datetime_from_array < last_played_of_track_from_file:
                artist_last_played_datetime[artist] = datetimestamp_from_file
                artist_last_played_track_title[artist] = title

        # Count the tracks of each artist
        artists_track_count = dict(Counter(list_of_artists))

        # Remove duplicate artists from the list of artists
        list_of_artists = list(set(list_of_artists))

        # Loop through list of artists
        for artist in list_of_artists:
            # incase of empty artist fields, check artist
            if artist:
                # Add the artist name, number of tracks and the last played track to a dictionary
                artists_with_data.append({"artist": artist, "track_count": artists_track_count[artist],
                                          "last_played_track": str(artist_last_played_track_title[artist])})

        return {'artists': artists_with_data}, 200


api.add_resource(Track, '/tracks')
api.add_resource(SingleTrack, '/tracks/<track_id>')
api.add_resource(FilterTracks, '/tracks/filter_by_name/<filter_text>')
api.add_resource(LastPlayed, '/last_played')
api.add_resource(Artists, '/artists')

if __name__ == '__main__':
    app.run(debug=True)
