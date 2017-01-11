from datetime import datetime
from app import app, db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    bucketlists = db.relationship('BucketList', backref="user",
                                  cascade="all,delete-orphan", lazy='dynamic')

    @property
    def id(self):
        return self.user_id

    def check_password(self, password):
        return password == self.password

    def get_bucketlists_as_json(self, limit, offset):
        '''returns list of bucketlists owned by the user'''
        if limit is None:
            limit = 20
        if offset is None:
            offset = 0

        limit = int(limit)
        offset = int(offset)

        list_bucketlists = []
        for bucketlist in self.bucketlists:
            list_bucketlists.append(bucketlist.to_json())

        return list_bucketlists[offset:limit + offset]


class BucketList(db.Model):
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    items = db.relationship('ListItem', backref="bucket_list",
                            cascade="all,delete-orphan", lazy='select')
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'))

    def to_json(self):
        return {
            "id": self.bucketlist_id,
            "name": self.name,
            "items": self.items_to_json(),
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "created_by": self.owner_id
        }

    def from_json(self, json):
        self.name = json['name']
        self.date_modified = datetime.utcnow()

    def items_to_json(self):
        '''returns list of items in bucketlist'''
        list_items = []
        for item in self.items:
            list_items.append(item.to_json())
        return list_items

    def get_item(self, item_id):
        for item in self.items:
            if item.item_id == item_id:
                return item

    def __repr__(self):
        return '<BucketList %s>' % (self.name)


class ListItem(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey('bucket_list.bucketlist_id', ondelete='CASCADE'))

    def to_json(self):
        return {
            "id": self.item_id,
            "name": self.item_name,
            "date_created": self.date_created,
            "date_modified": self.date_modified,
            "done": self.done
        }

    def from_json(self, json):
        self.item_name = json['name']
        self.date_modified = datetime.utcnow()

    def __repr__(self):
        return '<ListItem %s>' % (self.item_name)
