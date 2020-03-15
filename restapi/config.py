import os


class Config(object):
    DATABASE_URL = os.environ.get("DATABASE_URL") or "postgres://postgres:postgres@localhost:5433/databases-project" \
                                                     "-backend-dev-local "
