import psycopg2
import os
import logging
import json

# logger for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

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
        logger.debug("url {}".format(self.url))

    def __enter__(self):
        """
        Called before the beginning of "with" block.
        """
        try:
            # TODO! -> add sslmode='require' param
            self.conn = psycopg2.connect(DATABASE_URL)
            self.cur = self.conn.cursor()
            logger.info("Connected to the db")
        except:
            logger.error("Could not connect to the db")
        finally:
            return self.cur

    def __exit__(self, err_type, value, traceback):
        """
        Called after the "with" block.
        """
        if err_type is not None or \
                value is not None or \
                traceback is not None:
            # if an error is raised during "with" block execution, log it.
            logger.error("Could not execute query.\"{}\" Traceback: \n{}\n".format(
                err_type,
                traceback
            ))
        if self.commit:
            try:
                self.conn.commit()
                logger.info("commited changes to db")
            except:
                logger.error("could not commit changes to db")

        self.cur.close()
        self.conn.close()
        logger.info("closed connection to db")


class DBTable:
    """
    Yet another convenience class because I like OOP and really hate doing
    silly stuff like hardcoding column names for my db tables.
    """

    def __init__(self, tname):
        self.__cur = Cursor
        self.__tname = tname
        self.columns = self.__get_columns()

    def __get_columns(self):
        """
        retreives the column names for this table.
        """
        columns = []
        with self.__cur(commit=False) as cursor:
            cursor.execute("SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME =%s;", (self.__tname,))
            res = cursor.fetchall()
        for r in res:
            columns.append(r[0])
        return columns

    def execute(self, commit=True):
        with self.__cur(commit) as cursor:
            yield cursor


def single_to_json(query_res, columns):
    """
    Converts a single db row to a json object
    :param: query_res - result of the query AS A TUPLE
    :param: columns - column names of the table
    """
    row = {}
    counter = 0
    for c in columns:
        row[c] = query_res[counter]
        counter += 1
    return json.dumps(row)


def many_to_json(query_res, columns):
    """
    Converts multiple db rows into an array of jsons
    :param: query_res - result of a query as A LIST OF TUPLES
    :param: columns - column names of the table
    """
    array = []
    for res in query_res:
        row = {}
        counter = 0
        for c in columns:
            row[c] = res[counter]
            counter += 1
        array.append(row)
    return json.dumps(array)
