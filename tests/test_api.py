from testbase import BaseTestCase
from app.models import User, BucketList, ListItem
import json


class TestApi(BaseTestCase):
    def test_can_create_bucketlist(self):
        headers = self.get_auth_header()
        bucketlist = {
            "name": "BucketList1",
        }
        response = self.client.post('/bucketlists',
                                    data=json.dumps(bucketlist),
                                    headers=headers
                                    )
        assert response.status_code == 201

        exists = BucketList.query.filter(
            bucketlist['name'] == BucketList.name).first()

        self.assertIsNotNone(exists)

    def test_does_not_create_bucketlist_without_name(self):
        headers = self.get_auth_header()
        bucketlist = {}
        response = self.client.post('/bucketlists',
                                    data=json.dumps(bucketlist),
                                    headers=headers
                                    )

        assert response.status_code == 400

