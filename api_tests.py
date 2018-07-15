import api
import json
import unittest


class APITestCase(unittest.TestCase):
    def reset_file(self):
        with open('tracks_backup.json') as json_file:
            self.all_tracks = json.load(json_file)

        with open('tracks.json', 'w') as json_file_w:
            json_file_w.write(json.dumps(self.all_tracks))

    def setUp(self):
        api.app.testing = True
        APITestCase.reset_file(self)
        self.app = api.app.test_client()

    def tearDown(self):
        APITestCase.reset_file(self)

    def newTrack(self, id, title, artist, duration, last_play):
        client = self.app.post('/tracks', data=dict(
            id=id,
            title=title,
            artist=artist,
            duration=duration,
            last_play=last_play
        ))
        return client

    def test_getSingleTrackStatus(self):
        client = self.app.get('/tracks/4444')
        assert "404 NOT FOUND" == client.status

        client = self.app.get('/tracks/%@^@^@£^^£')
        assert "404 NOT FOUND" == client.status

        client = self.app.get('/tracks/1')
        assert "200 OK" == client.status

        client = self.app.get('/tracks/200')
        assert "200 OK" == client.status

    def test_getSingleTrackMessage(self):
        client = self.app.get('/tracks/-1')
        assert '{\"message\": \"track -1 doesn\'t exist\"}' in client.data.decode()

        client = self.app.get('/tracks/4444')
        assert '{\"message\": \"track 4444 doesn\'t exist\"}' in client.data.decode()

        client = self.app.get('/tracks/N0TANINT')
        assert '{"message": "track N0TANINT doesn\'t exist"}' in client.data.decode()

        client = self.app.get('/tracks/5')
        assert '{"track": [{"id": "5", "title": "Paparazzi", "artist": "Lady GaGa", "duration": "199", "last_play": ' \
               '"2016-02-23 08:24:37"}]}' in client.data.decode()

        client = self.app.get('/tracks/100')
        assert '{"track": [{"id": "100", "title": "Addicted To Love", "artist": "Robert Palmer", "duration": "188", ' \
               '"last_play": "2017-03-14 09:33:16"}]}' in client.data.decode()

    def test_addNewTrackStatusMessage(self):
        client = APITestCase.newTrack(self, id=1, title="a title of a song", artist="An artists name", duration=532,
                                      last_play="2017-03-14 09:33:16")
        assert "409 CONFLICT" == client.status
        assert '{"message": "track 1 already exists"}' in client.data.decode()

        client = APITestCase.newTrack(self, id=900000, title="a title of a song", artist="An artists name",
                                      duration=532, last_play="2017-03-14 09:33:16")
        assert "201 CREATED" == client.status

        assert '{"track": [{"id": "900000", "title": "a title of a song", "artist": "An artists name",' \
               ' "duration": "532", "last_play": "2017-03-14 09:33:16"}]}' in client.data.decode()

        client = APITestCase.newTrack(self, id=900000, title="a title of a different song",
                                      artist="An different artists name", duration=22, last_play="2017-03-14 09:33:16")
        assert "409 CONFLICT" == client.status

        assert '{"message": "track 900000 already exists"}' in client.data.decode()

        client = APITestCase.newTrack(self, id=600000, title="a title of a different song",
                                      artist="An different artists name", duration=232, last_play="2017-03-14 09:33:16")
        assert "201 CREATED" == client.status

        assert '{"track": [{"id": "600000", "title": "a title of a different song",' \
               ' "artist": "An different artists name", "duration": "232",' \
               ' "last_play": "2017-03-14 09:33:16"}]}' in client.data.decode()

        client = APITestCase.newTrack(self, id="non numerical input", title="a title of a different song",
                                      artist="an artists name", duration=232, last_play="2017-03-14 09:33:16")
        assert "400 BAD REQUEST" == client.status
        assert '{"message": "track_id non numerical input is not an integer"}' in client.data.decode()

        client = APITestCase.newTrack(self, id=25352, title="a title of a different song",
                                      artist="an artists name", duration="a random set of letters",
                                      last_play="2017-03-14 09:33:16")
        assert "400 BAD REQUEST" == client.status
        assert '{"message": "duration a random set of letters is not an integer"}' in client.data.decode()

    def test_LastPlayed(self):
        client = self.app.get('/last_played')

        assert "200 OK" == client.status

        client = APITestCase.newTrack(self, id=1234567, title="a recently played song",
                                      artist="an artists name", duration=232,
                                      last_play="2020-03-14 10:23:26")

        assert "201 CREATED" == client.status

        client = self.app.get('/last_played')
        last_played = json.loads(client.data.decode())
        id_of_last_played = last_played['tracks'][0]['id']

        assert int(id_of_last_played) == int(1234567)

    def test_FilterbyName(self):
        test_title = "a unique name"
        client = APITestCase.newTrack(self, id=1234568, title=test_title,
                                      artist="an artists name", duration=232,
                                      last_play="2010-03-14 10:23:26")
        assert "201 CREATED" == client.status

        client = self.app.get('/tracks/filter_by_name/' + test_title)
        filtered_tracks = json.loads(client.data.decode())

        closest_match = filtered_tracks['tracks'][0]['title']
        assert str(closest_match) == str(test_title)

    def test_artists(self):
        test_title_fail = "not the title with the latest play"
        test_title = "The title with the latest play"
        client = APITestCase.newTrack(self, id=2525, title=test_title_fail,
                                      artist="an artist with 5 songs", duration=232,
                                      last_play="2000-03-14 10:23:26")
        assert "201 CREATED" == client.status
        client = APITestCase.newTrack(self, id=2526, title=test_title_fail,
                                      artist="an artist with 5 songs", duration=232,
                                      last_play="2010-03-14 10:23:26")
        assert "201 CREATED" == client.status
        client = APITestCase.newTrack(self, id=2528, title=test_title,
                                      artist="an artist with 5 songs", duration=232,
                                      last_play="2030-03-14 10:23:26")
        assert "201 CREATED" == client.status
        client = APITestCase.newTrack(self, id=2527, title=test_title_fail,
                                      artist="an artist with 5 songs", duration=232,
                                      last_play="2020-03-14 10:23:26")
        assert "201 CREATED" == client.status

        client = self.app.get('/artists')
        artists = json.loads(client.data.decode())
        artists = artists['artists']

        test_artist = next((artist for artist in artists if artist["artist"] == "an artist with 5 songs"))
        assert str(test_artist['artist']) == "an artist with 5 songs"
        assert str(test_artist['last_played_track']) == "The title with the latest play"


if __name__ == '__main__':
    unittest.main()
