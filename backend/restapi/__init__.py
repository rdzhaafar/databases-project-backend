from flask import Flask
from backend.restapi.config import Config
import logging

# Setup logging for this module
logger = logging.getLogger(__name__)
filehandler = logging.FileHandler("backend.log")
formatter = logging.Formatter(
    "%(funcName)s:%(lineno)s:%(levelname) - %(message)s"
)
filehandler.setFormatter(formatter)
logger.addHandler(filehandler)

# configure Flask
restapi = Flask(__name__)
restapi.config.from_object(Config)

# This needs to be here to avoid circular imports
from backend.restapi.database import initialize_database

initialize_database()
from backend.restapi import routes
