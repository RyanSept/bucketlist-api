from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append('..')
import config

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

from app import models

db.create_all()

#item = models.ListItem(item_name="Make tea")
#blist = models.BucketList(name='My Todo List', items=[item])
#user = models.User(first_name="John", last_name="Doe", email="johndoe@gmail.com", password="password", bucketlists=[blist])

#db.session.add_all([item, blist, user])
db.session.commit()