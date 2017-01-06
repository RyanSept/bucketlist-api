import sys
sys.path.append('..')

from unittest import TestCase
from app import app
import json


class BaseTestCase(TestCase):
    def setUp(self):
        app.config['DATABASE'] = "test.db"
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        self.client = app.test_client()

    def login(self):
        response = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {'email': 'johndoe@gmail.com',
                                         'password': "password"}),
                                    content_type='application/json')

        data = json.loads(response.get_data(as_text=True))
        return data['access_token']

    def get_auth_header(self):
        token = self.login()
        return {'Authorization': 'JWT %s' % token,
                'Content-type': 'application/json'
                }
