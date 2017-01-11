from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)

app.config.from_object('config.Config')
app.url_map.strict_slashes = False

db = SQLAlchemy(app)

from app import models, views

db.create_all()
db.session.commit()
