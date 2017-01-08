import sys
sys.path.append('..')

from unittest import TestCase
from app import app, models, db
from flask_sqlalchemy import SQLAlchemy
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

    def tearDown(self):
        models.User.query.delete()
        models.BucketList.query.delete()
        models.ListItem.query.delete()

        user = models.User(
            first_name="John",
            last_name="Doe",
            email="johndoe@gmail.com",
            password="password"
        )

        db.session.add_all([user])
        db.session.commit()

    def create_bucketlist(self):
        headers = self.get_auth_header()
        bucketlist = {
            "name": "BucketList1",
        }
        self.client.post('/bucketlists',
                         data=json.dumps(bucketlist),
                         headers=headers
                         )
