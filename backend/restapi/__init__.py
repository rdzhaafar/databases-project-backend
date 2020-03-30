from flask import Flask
from backend.restapi.config import Config


restapi = Flask(__name__)
restapi.config.from_object(Config)

from backend.restapi.database import initialize_database
initialize_database()
from backend.restapi import routes
