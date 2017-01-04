import sys
sys.path.append('..')

from datetime import datetime
from app import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    bucketlists = db.relationship('BucketList', backref="user",
                                  cascade="all,delete-orphan", lazy='dynamic')

    def check_password(self, password):
        return password == self.password

    def __repr__(self):
        return '<User %s %s>' % (self.first_name, self.last_name)


class BucketList(db.Model):
    bucketlist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime)
    items = db.relationship('ListItem', backref="bucket_list",
                            cascade="all,delete-orphan", lazy='dynamic', passive_deletes=True)
    owner_id = db.Column(db.Integer, db.ForeignKey(
        'user.user_id', ondelete='CASCADE'))

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

    def __repr__(self):
        return '<ListItem %s>' % (self.item_name)
