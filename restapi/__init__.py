from flask import Flask
from restapi.config import Config

restapi = Flask(__name__)
restapi.config.from_object(Config)

from restapi import routes