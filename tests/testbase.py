import sys
sys.path.append('..')

from unittest import TestCase
from app import app


class BaseTestCase(TestCase):
    def setUp(self):
        app.config['DATABASE'] = "test.db"
        app.config['TESTING'] = True
        self.client = app.test_client()
