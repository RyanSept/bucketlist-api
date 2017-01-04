from testbase import BaseTestCase
import json


class TestAuthentication(BaseTestCase):

    def test_user_can_login(self):
        response = self.client.post('/auth/login',
                                    data=json.dumps(
                                        {'email': 'johndoe@gmail.com',
                                         'password': "password"}),
                                    content_type='application/json')

        assert response.status_code == 200

        data = json.loads(response.get_data(as_text=True))
        assert data['email'] == "johndoe@gmail.com"

    def test_user_cannot_login_twice(self):
        pass
