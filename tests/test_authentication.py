from testbase import BaseTestCase
from app.models import User, BucketList, ListItem
import json


class TestAuthentication(BaseTestCase):

    def test_user_can_login(self):
        response = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {"email": "johndoe@gmail.com",
                                         "password": "password"}),
                                    content_type='application/json'
                                    )

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('access_token', data)

    def test_login_with_wrong_credentials(self):
        response = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {"email": "wrongcredential@gmail.com",
                                         "password": "password"}),
                                    content_type='application/json'
                                    )
        assert response.status_code == 401

    def test_access_with_token_works(self):
        token = self.login()
        headers = {'Authorization': 'JWT %s' % token}
        response = self.client.post('/resource',
                                    content_type="application/json",
                                    headers=headers
                                    )
        assert response.status_code == 200

    def test_access_with_wrong_token(self):
        headers = {'Authorization': "abc"}
        response = self.client.post('/resource',
                                    content_type="application/json",
                                    headers=headers
                                    )
        assert response.status_code == 401

    def test_cannot_post_to_bucketlists_if_not_authenticated(self):
        response = self.client.post('/bucketlists',
                                    content_type="application/json",)
        assert response.status_code == 401

    def test_cannot_get_bucketlists_if_not_authenticated(self):
        response = self.client.get('/bucketlists')
        assert response.status_code == 401

    def test_cannot_get_single_bucketlist_if_not_authenticated(self):
        response = self.client.get('/bucketlists/1')
        assert response.status_code == 401

    def test_cannot_update_single_bucketlist_if_not_authenticated(self):
        response = self.client.put('/bucketlists/1')
        assert response.status_code == 401

    def test_cannot_delete_single_bucketlist_if_not_authenticated(self):
        response = self.client.delete('/bucketlists/1')
        assert response.status_code == 401

    def test_cannot_create_bucketlist_item_if_not_authenticated(self):
        response = self.client.post('/bucketlists/1/items')
        assert response.status_code == 401

    def test_can_register(self):
        user_data = {
            "first_name": "Ryan",
            "last_name": "Marvin",
            "email": "ryan.marvin@andela.com",
            "password": "password",
        }

        response = self.client.post(
            "/auth/register",
            content_type="application/json",
            data=json.dumps(user_data)
        )
        assert response.status_code == 201

        new_user = User.query.filter(user_data['email'] == User.email).first()

        self.assertIsNotNone(new_user)

    def test_does_not_register_with_missing_fields(self):
        user_data = {
            "email": "ryan.marvin@andela.com",
        }

        response = self.client.post(
            "/auth/register",
            content_type="application/json",
            data=json.dumps(user_data)
        )
        assert response.status_code == 400

        new_user = User.query.filter(user_data['email'] == User.email).first()
        self.assertIsNone(new_user)

    def test_register_validates_email(self):
        user_data = {
            "first_name": "Ryan",
            "last_name": "Marvin",
            "email": "wrongemail",
            "password": "password",
        }

        response = self.client.post(
            "/auth/register",
            content_type="application/json",
            data=json.dumps(user_data)
        )

        assert response.status_code == 400

    def test_cannot_register_twice(self):
        user_data = {
            "first_name": "Ryan",
            "last_name": "Marvin",
            "email": "ryan.marvin@andela.com",
            "password": "password",
        }

        response = self.client.post(
            "/auth/register",
            content_type="application/json",
            data=json.dumps(user_data)
        )

        assert response.status_code == 201

        response2 = self.client.post(
            "/auth/register",
            content_type="application/json",
            data=json.dumps(user_data)
        )

        assert response2.status_code == 409
