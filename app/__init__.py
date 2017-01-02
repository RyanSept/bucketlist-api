from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys
sys.path.append('..')
import config

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)
