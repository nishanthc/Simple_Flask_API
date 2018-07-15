import api
import json
import unittest


class APITestCase(unittest.TestCase):

    def setUp(self):

        api.app.testing = True
        with open('tracks_backup.json') as json_file:
            self.all_tracks = json.load(json_file)

        with open('tracks.json', 'w') as json_file_w:
            json_file_w.write(json.dumps(self.all_tracks))
        self.app = api.app.test_client()

    def new_track(self,id,title,artist,duration,last_play):
        client = self.app.post('/tracks', data=dict(
            id=id,
            title=title,
            artist=artist,
            duration=duration,
            last_play=last_play
        ))
        return client


    def test_get_single_track_status(self):

        client = self.app.get('/tracks/4444')
        assert "404 NOT FOUND" == client.status

        client = self.app.get('/tracks/%@^@^@£^^£')
        assert "404 NOT FOUND" == client.status

        client = self.app.get('/tracks/1')
        assert "200 OK" == client.status

        client = self.app.get('/tracks/200')
        assert "200 OK" == client.status

    def test_get_single_track_message(self):

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




    def test_add_new_track_status_message(self):


        client = APITestCase.new_track(self, id=1, title="a title of a song", artist="An artists name", duration=532,
                                       last_play="2017-03-14 09:33:16")
        assert "409 CONFLICT" == client.status
        assert '{"message": "track 1 already exists"}' in client.data.decode()

        client = APITestCase.new_track(self, id=900000, title="a title of a song", artist="An artists name",
                                       duration=532, last_play="2017-03-14 09:33:16")
        assert "201 CREATED" == client.status
        assert '{"track": [{"id": "900000", "title": "a title of a song", "artist": "An artists name",' \
               ' "duration": "532", "last_play": "2017-03-14 09:33:16"}]}' in client.data.decode()


        client = APITestCase.new_track(self, id=900000, title="a title of a different song",
                                       artist="An different artists name", duration=22, last_play="2017-03-14 09:33:16")
        assert "409 CONFLICT" == client.status

        assert '{"message": "track 900000 already exists"}' in client.data.decode()

        client = APITestCase.new_track(self, id=600000, title="a title of a different song",
                                       artist="An different artists name", duration=232, last_play="2017-03-14 09:33:16")
        assert "201 CREATED" == client.status

        assert '{"track": [{"id": "600000", "title": "a title of a different song",' \
               ' "artist": "An different artists name", "duration": "232",' \
               ' "last_play": "2017-03-14 09:33:16"}]}' in client.data.decode()




        client = APITestCase.new_track(self, id="non numerical input", title="a title of a different song",
                                       artist="An different artists name", duration=232, last_play="2017-03-14 09:33:16")
        assert "400 BAD REQUEST" == client.status
        assert '{"message": "track_id non numerical input is not an integer"}' in client.data.decode()


        client = APITestCase.new_track(self, id=25352, title="a title of a different song",
                                       artist="An different artists name", duration="a random set of letters",
                                       last_play="2017-03-14 09:33:16")
        assert "400 BAD REQUEST" == client.status
        assert '{"message": "duration a random set of letters is not an integer"}' in client.data.decode()




if __name__ == '__main__':
    unittest.main()