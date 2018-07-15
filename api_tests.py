import api
import json
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):

        api.app.testing = True
        with open('tracks.json') as json_file:
            self.all_tracks = json.load(json_file)
        self.app = api.app.test_client()


    def test_get_single_track_status(self):
        client = self.app.get('/track/4444')
        assert "404 NOT FOUND" == client.status

        client = self.app.get('/track/%@^@^@£^^£')
        assert "404 NOT FOUND" == client.status

        client = self.app.get('/track/1')
        assert "200 OK" == client.status

        client = self.app.get('/track/200')
        assert "200 OK" == client.status

    def test_get_single_track_message(self):


        rv = self.app.get('/track/-1')
        assert '{\"message\": \"track -1 doesn\'t exist\"}' in rv.data.decode()

        client = self.app.get('/track/4444')
        assert '{\"message\": \"track 4444 doesn\'t exist\"}' in client.data.decode()

        client = self.app.get('/track/N0TANINT')
        assert '{"message": "track N0TANINT doesn\'t exist"}' in client.data.decode()


        client = self.app.get('/track/5')
        assert '{"track": [{"id": "5", "title": "Paparazzi", "artist": "Lady GaGa", "duration": "199", "last_play": ' \
               '"2016-02-23 08:24:37"}]}' in client.data.decode()


        client = self.app.get('/track/100')
        assert '{"track": [{"id": "100", "title": "Addicted To Love", "artist": "Robert Palmer", "duration": "188", ' \
               '"last_play": "2017-03-14 09:33:16"}]}' in client.data.decode()


if __name__ == '__main__':
    unittest.main()