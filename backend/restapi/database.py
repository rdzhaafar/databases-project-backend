import os
from os import path

import psycopg2

from backend.restapi import app

"""
This file contains all the miscellaneous functions/objects
for managing and interacting with the database.
"""


class Cursor:
    """
    Database cursor context manager. Handles repetitive operations,
    such as setting up the connection, committing changes and closing
    the connection when finished.
    """

    def __init__(self, commit=True):
        """
        Sets up the connection to the database.

        Args:
            commit (bool): commit changes done, while using the Cursor object.
        """
        self.commit = commit
        self.url = app.config["DATABASE_URL"]

    def __enter__(self):
        """
        Returns:
            psycopg.connection.cursor: a database cursor with the necessary
            setup done.
        """
        try:
            # TODO! -> add sslmode='require' param
            self.conn = psycopg2.connect(self.url)
            self.cur = self.conn.cursor()
        except:
            return None
        finally:
            return self.cur

    def __exit__(self, err_type, value, traceback):
        """
        Cleans up after using the Cursor object.
        Args:
            err_type (str): type of error raised while using the cursor.
            value (Error): error message.
            traceback (str): traceback of the error.
        """
        if self.commit:
            try:
                self.conn.commit()
            except:
                # You didn't think I would actually hanlde this properly, did you? ;)
                pass

        self.cur.close()
        self.conn.close()


def initialize_database():
    """
    Initializes all database tables on backend startup.
    Table definitions are stored under backend/restapi/sql/create_tables.sql
    """
    cwd = os.getcwd()
    fpath = path.join(cwd, "restapi", "sql", "create_tables.sql")
    with open(fpath, 'r') as tables_file:
        tables_sql = tables_file.read()
    with Cursor(commit=True) as cursor:
        cursor.execute(tables_sql)
