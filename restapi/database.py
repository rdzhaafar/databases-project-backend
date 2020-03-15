from restapi import restapi
import psycopg2


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
        self.url = restapi.config["DATABASE_URL"]

    def __enter__(self):
        """
        Called before the beginning of "with" block.
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
        Called after the "with" block.
        """
        if self.commit:
            try:
                self.conn.commit()
            except:
                pass

        self.cur.close()
        self.conn.close()


