from unittest import TestCase
from app import app, models, db
from flask_sqlalchemy import SQLAlchemy
import json


class BaseTestCase(TestCase):
    def setUp(self):
        app.config.from_object('config.TestConfig')
        db.create_all()
        self.client = app.test_client()

    def login(self):
        response = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {'email': 'johndoe@gmail.com',
                                         'password': "password"}),
                                    content_type='application/json')

        data = json.loads(response.get_data(as_text=True))
        return data["access_token"]

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

    def register_second_user(self):
        '''Registers other user for testing'''
        user_data = {
            "first_name": "Ryan",
            "last_name": "Marvin",
            "email": "ryan.marvin@andela.com",
            "password": "password",
        }

        self.client.post(
            "/auth/register",
            content_type="application/json",
            data=json.dumps(user_data)
        )

    def add_bucketlist_item(self):
        '''adds a bucketlist item'''
        headers = self.get_auth_header()

        item = {"name": "Foo the bar"}
        self.client.post("/bucketlists/1/items",
                         data=json.dumps(item),
                         headers=headers
                         )
