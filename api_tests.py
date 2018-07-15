import api
from flask_restful import Resource, Api, abort
import unittest


class FlaskrTestCase(unittest.TestCase):

    def setUp(self):

        api.app.testing = True
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
        assert b'{\"message\": \"track -1 doesn\'t exist\"}' in rv.data

        client = self.app.get('/track/4444')
        assert b'{\"message\": \"track 4444 doesn\'t exist\"}' in client.data

        client = self.app.get('/track/N0TANINT')
        assert b'{\"message\": \"track N0TANINT doesn\'t exist\"}' in client.data



if __name__ == '__main__':
    unittest.main()