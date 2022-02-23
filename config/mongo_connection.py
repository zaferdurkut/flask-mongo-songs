from flask_pymongo import PyMongo

from run import app

MONGO_CLIENT = PyMongo(app)
