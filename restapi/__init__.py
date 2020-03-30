from flask import Flask
from restapi.config import Config


restapi = Flask(__name__)
restapi.config.from_object(Config)

from restapi.database import initialize_database
initialize_database()
from restapi import routes
