from testbase import BaseTestCase
import json


class TestAuthentication(BaseTestCase):

    def test_user_can_login(self):
        response = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {"email": "johndoe@gmail.com",
                                         "password": "password"}),
                                    content_type='application/json')

        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        self.assertIn('access_token', data)

    def test_login_with_wrong_credentials(self):
        response = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {"email": "wrongcredential@gmail.com",
                                         "password": "password"}),
                                    content_type='application/json')
        assert response.status_code == 401

    def test_access_with_token_works(self):
        token = self.login()
        headers = {'Authorization': 'JWT %s' % token}
        response = self.client.post('/resource',
                                    content_type="application/json",
                                    headers=headers)
        assert response.status_code == 200

    def test_access_with_wrong_token(self):
        headers = {'Authorization': "abc"}
        response = self.client.post('/resource',
                                    content_type="application/json",
                                    headers=headers)
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
        pass

    def test_register_missing_fields_raises_error(self):
        pass
