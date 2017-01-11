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

    def test_create_bucketlist_without_name(self):
        headers = self.get_auth_header()
        bucketlist = {}
        response = self.client.post('/bucketlists',
                                    data=json.dumps(bucketlist),
                                    headers=headers
                                    )

        assert response.status_code == 400

    def test_create_bucketlist_with_empty_name_string(self):
        headers = self.get_auth_header()
        bucketlist = {'name': ''}
        response = self.client.post('/bucketlists',
                                    data=json.dumps(bucketlist),
                                    headers=headers
                                    )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["message"], "The bucketlist name is too short.")

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

    def test_list_bucketlists_when_no_bucketlists_exist(self):
        headers = self.get_auth_header()
        response = self.client.get('/bucketlists', headers=headers)

        data = json.loads(response.get_data(as_text=True))
        bucketlists = data["bucketlists"]
        self.assertTrue(len(bucketlists) < 1)

    def test_lists_single_bucketlist(self):
        headers = self.get_auth_header()
        self.create_bucketlist()

        response = self.client.get('/bucketlists/1', headers=headers)

        data = json.loads(response.get_data(as_text=True))
        assert len(data["bucketlist"]) > 0

    def test_list_single_bucketlist_when_id_non_existent(self):
        headers = self.get_auth_header()
        response = self.client.get('/bucketlists/1', headers=headers)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data["bucketlist"]) < 1)

    def test_updates_bucketlist(self):
        headers = self.get_auth_header()
        # create bucketlist
        self.create_bucketlist()

        # update bucketlist
        bucketlist_update = {"name": "Aruarian Dream"}
        response = self.client.put('/bucketlists/1',
                                   data=json.dumps(bucketlist_update),
                                   headers=headers
                                   )

        assert response.status_code == 200

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

        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "The requested bucketlist does not exist."

    def test_deletes(self):
        self.create_bucketlist()
        headers = self.get_auth_header()

        response = self.client.delete('/bucketlists/1', headers=headers)

        assert response.status_code == 200

    def test_delete_when_bucketlist_doesnt_exist(self):
        headers = self.get_auth_header()

        response = self.client.delete('/bucketlists/1', headers=headers)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["message"], "The bucketlist does not exist.")

    def test_search_bucketlist_by_name(self):
        headers = self.get_auth_header()
        self.create_bucketlist()

        response = self.client.get('/bucketlists?q=bucketlist1',
                                   headers=headers)

        data = json.loads(response.get_data(as_text=True))
        assert len(data["bucketlists"]) == 1

    def test_search_nonexistent_bucketlist_by_name(self):
        headers = self.get_auth_header()
        response = self.client.get('/bucketlists?q=bucketlist1',
                                   headers=headers)

        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "No bucketlists by that name found."

    def test_limit_get_bucketlist_list(self):
        headers = self.get_auth_header()
        bucketlist = {"name": "BucketList"}
        # add 21 bucketlists
        for n in range(1, 22):
            name = bucketlist["name"] + str(n)
            bucketlist = {"name": name}
            self.client.post('/bucketlists',
                             data=json.dumps(bucketlist),
                             headers=headers
                             )

        # get bucketlists with limit
        response = self.client.get('/bucketlists?limit=20&offset=15',
                                   headers=headers)

        data = json.loads(response.get_data(as_text=True))
        assert len(data["bucketlists"]) <= 20

    def test_limit_get_bucketlist_list_handles_non_int_as_query_string(self):
        headers = self.get_auth_header()
        self.create_bucketlist()
        # get bucketlists with limit
        response = self.client.get('/bucketlists?limit=foo&offset=10',
                                   headers=headers)
        assert response.status_code == 400


class TestItemsApi(BaseTestCase):
    def test_add_bucketlist_item(self):
        self.create_bucketlist()
        headers = self.get_auth_header()

        item = {"name": "Foo the bar"}
        response = self.client.post("/bucketlists/1/items",
                                    data=json.dumps(item),
                                    headers=headers
                                    )
        assert response.status_code == 201

    def test_does_not_add_bucketlist_item_with_invalid_data(self):
        self.create_bucketlist()
        headers = self.get_auth_header()

        item = json.dumps({})
        response = self.client.post("/bucketlists/1/items",
                                    data=item, headers=headers
                                    )
        assert response.status_code == 400

    def test_does_not_add_bucketlist_item_with_empty_string_name(self):
        self.create_bucketlist()
        headers = self.get_auth_header()

        item = json.dumps({"name": ''})
        response = self.client.post("/bucketlists/1/items",
                                    data=item, headers=headers
                                    )

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data["message"], "The item name is too short.")

    def test_doesnt_add_bucketlist_item_if_non_existent_bucketlist_id(self):
        headers = self.get_auth_header()

        item = json.dumps({"name": "Foo the bar"})
        response = self.client.post("/bucketlists/1/items",
                                    data=item, headers=headers
                                    )

        data = json.loads(response.get_data(as_text=True))
        assert data["message"] == "The requested bucketlist does not exist."

    def test_can_update_bucketlist_item(self):
        headers = self.get_auth_header()

        self.create_bucketlist()
        self.add_bucketlist_item()

        item_update = {"name": "Gospod da pridet tvoyo tsartsova"}
        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps(item_update),
                                   headers=headers
                                   )
        assert response.status_code == 200

    def test_doesnt_update_bucketlist_item_if_invalid_data(self):
        headers = self.get_auth_header()

        self.create_bucketlist()
        self.add_bucketlist_item()

        item_update = {}
        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps(item_update),
                                   headers=headers
                                   )
        assert response.status_code == 400

    def test_update_to_non_existent_bucketlist_item(self):
        headers = self.get_auth_header()

        self.create_bucketlist()

        item_update = {"name": "Gospod da pridet tvoyo tsartsova"}
        response = self.client.put("/bucketlists/1/items/1",
                                   data=json.dumps(item_update),
                                   headers=headers
                                   )

        data = json.loads(response.get_data(as_text=True))
        assert data[
            "message"] == "The requested bucketlist or bucketlist item does not exist."

    def test_can_delete_bucketlist_item(self):
        headers = self.get_auth_header()
        self.create_bucketlist()
        self.add_bucketlist_item()

        response = self.client.delete('/bucketlists/1/items/1',
                                      headers=headers
                                      )

        assert response.status_code == 200

    def test_delete_when_bucketlist_item_doesnt_exist(self):
        headers = self.get_auth_header()

        response = self.client.delete('/bucketlists/1/items/1',
                                      headers=headers)

        data = json.loads(response.get_data(as_text=True))
        assert data[
            "message"] == "The bucketlist or bucketlist item does not exist."
