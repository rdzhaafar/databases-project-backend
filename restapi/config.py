import os


class Config(object):
    DATABASE_URL = os.environ.get("DATABASE_URL")
