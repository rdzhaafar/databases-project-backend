# Various db utilities

import psycopg2
import os
import logging

# create logger
logger = logging.getLogger("app_logger")
file_handler = logging.FileHandler("app.log")
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# TODO - remove. For testing only!
# Set the DATABASE_URL accordingly for local testing
os.environ["DATABASE_URL"] = "postgres://postgres:postgres@localhost:5433/databases-project-backend-dev-local"

# gets the database url from heroku dyno env
DATABASE_URL = os.environ["DATABASE_URL"]


class Cursor:
    """
    Cursor convenience class. Supports "with" context. 
    """

    def __init__(self, commit=True):
        """
        :param: commit indicates whether the changes need to be committed
        after the query is executed.
        """
        self.commit = commit
        self.url = DATABASE_URL

    def __enter__(self):
        """
        Called before the beginning of "with" block.
        """
        try:
            # TODO! -> add sslmode='require' param
            self.conn = psycopg2.connect(DATABASE_URL)
            self.cur = self.conn.cursor()
            logger.info("Connected to database at '{}'".format(self.url))
        except:
            logger.error("Could not connect to database at '{}'".format(self.url))
            return None
        finally:
            return self.cur

    def __exit__(self, err_type, value, traceback):
        """
        Called after the "with" block.
        """
        if self.commit:
            try:
                self.conn.commit()
            except:
                logger.error("Could not commit changes to the database.")

        self.cur.close()
        self.conn.close()


def get_table_columns(tname):
    """
    Gets column names for a given table
    """
    columns = []
    with Cursor(commit=False) as cursor:
        cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME=%s;", (tname,))
        res = cursor.fetchall()
    for r in res:
        columns.append(r[0])
    return columns

