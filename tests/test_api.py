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

    def test_lists_bucketlists(self):
        # create bucketlist
        headers = self.get_auth_header()
        bucketlist = {
            "name": "BucketList1",
        }
        self.client.post('/bucketlists',
                         data=json.dumps(bucketlist),
                         headers=headers
                         )

        # request for bucketlists
        response = self.client.get('/bucketlists', headers=headers)
        assert response.status_code == 200

        data = response.get_data(as_text=True)
        self.assertIn(bucketlist["name"], data)

    def test_list_bucketlists_when_no_bucketlists_exist(self):
        headers = self.get_auth_header()
        response = self.client.get('/bucketlists', headers=headers)
        assert response.status_code == 404

        data = json.loads(response.get_data(as_text=True))
        bucketlists = data["bucketlists"]

        self.assertTrue(len(bucketlists) < 1)

    def test_updates_bucketlist(self):
        headers = self.get_auth_header()
        # create bucketlist
        self.create_bucketlist()

        # update bucketlist
        bucketlist2 = {"name": "Aruarian Dream"}
        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(bucketlist2),
                                   headers=headers
                                   )

        assert response.status_code == 200
        changed = BucketList.query.filter(
            bucketlist2['name'] == BucketList.name).first()

        self.assertIsNotNone(changed)

    def test_does_not_update_bucketlist_if_no_data_given(self):
        headers = self.get_auth_header()
        self.create_bucketlist()

        bucketlist = {}
        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(bucketlist),
                                   headers=headers
                                   )
        assert response.status_code == 400

    def test_handles_update_to_non_existent_bucketlist(self):
        headers = self.get_auth_header()
        bucketlist = {}
        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(bucketlist),
                                   headers=headers
                                   )

        assert response.status_code == 409
        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "The requested bucketlist does not exist."

    def test_deletes(self):
        self.create_bucketlist()
        headers = self.get_auth_header()

        response = self.client.delete('/bucketlists/1', headers=headers)

        assert response.status_code == 200

        bucketlist = BucketList.query.get(1)
        self.assertIsNone(bucketlist)

    def test_delete_when_bucketlist_doesnt_exist(self):
        headers = self.get_auth_header()

        response = self.client.delete('/bucketlists/1', headers=headers)

        assert response.status_code == 404

    def test_cannot_delete_other_users_bucketlist(self):
        pass

    def test_delete_bucketlist_deletes_bucketlist_items(self):
        pass


class TestItemsApi(BaseTestCase):
    def test_create_bucketlist_item(self):
        self.create_bucketlist()
        headers = self.get_auth_header()

        item = {"name": "Foo the bar"}
        response = self.client.post("/bucketlists/1/items",
                                    data=json.dumps(item),
                                    headers=headers
                                    )
        assert response.status_code == 201

        exists = ListItem.query.filter(
            item['name'] == ListItem.item_name).first()

        self.assertIsNotNone(exists)
        # assert exists.bucketlist_id == 1

    def test_does_not_create_bucketlist_item_with_invalid_data(self):
        self.create_bucketlist()
        headers = self.get_auth_header()

        item = json.dumps({})
        response = self.client.post("/bucketlists/1/items",
                                    data=item, headers=headers
                                    )
        assert response.status_code == 400

        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "You did not include the item name."

    def test_doesnt_create_bucketlist_item_if_non_existent_bucketlist_id(self):
        headers = self.get_auth_header()

        item = json.dumps({"name": "Foo the bar"})
        response = self.client.post("/bucketlists/1/items",
                                    data=item, headers=headers
                                    )

        assert response.status_code == 404

        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "The requested bucketlist does not exist."

    def test_cannot_add_items_in_other_users_bucketlists(self):
        pass
