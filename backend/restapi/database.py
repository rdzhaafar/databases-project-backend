import os
from os import path

import psycopg2

from restapi import app

"""
This file contains all the miscellaneous functions/objects
for managing and interacting with the database.
"""

CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS Branch (
  country VARCHAR PRIMARY KEY,
  branch_manager INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Employee (
  employee_id SERIAL PRIMARY KEY,
  employee_username VARCHAR UNIQUE NOT NULL,
  employee_password VARCHAR NOT NULL,
  branch VARCHAR NOT NULL,
  manager INTEGER,
  salary INTEGER NOT NULL,
  position varchar NOT NULL,
  FOREIGN KEY (manager) REFERENCES Employee (employee_id) ON UPDATE CASCADE,
  FOREIGN KEY (branch) REFERENCES Branch (country) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Account (
  account_id SERIAL PRIMARY KEY,
  first_name VARCHAR NOT NULL,
  last_name VARCHAR NOT NULL,
  email VARCHAR UNIQUE NOT NULL,
  phone VARCHAR,
  username VARCHAR UNIQUE NOT NULL,
  account_password VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS Pricing (
  pricing_id SERIAL PRIMARY KEY,
  class_name VARCHAR NOT NULL,
  host INTEGER NOT NULL,
  price FLOAT NOT NULL,
  home_type VARCHAR NOT NULL,
  rules VARCHAR,
  amenities VARCHAR,
  accomodates INTEGER NOT NULL,
  FOREIGN KEY (host) REFERENCES Account (account_id) ON UPDATE CASCADE,
  CONSTRAINT accomodates_ok CHECK (accomodates>=1)
);

CREATE TABLE IF NOT EXISTS RentalProperty (
  property_id SERIAL PRIMARY KEY,
  city VARCHAR NOT NULL,
  street VARCHAR NOT NULL,
  street_no INTEGER NOT NULL,
  unit INTEGER NOT NULL,
  zip VARCHAR NOT NULL,
  state_province VARCHAR NOT NULL,
  country VARCHAR NOT NULL,
  owner_id INTEGER NOT NULL,
  property_type VARCHAR NOT NULL,
  room_type VARCHAR NOT NULL,
  pricing_id INTEGER NOT NULL,
  bathroom INTEGER NOT NULL,
  bedroom INTEGER NOT NULL,
  bed JSON NOT NULL,
  FOREIGN KEY (country) REFERENCES Branch (country) ON UPDATE CASCADE,
  FOREIGN KEY (owner_id) REFERENCES Account (account_id) ON UPDATE CASCADE,
  FOREIGN KEY (pricing_id) REFERENCES Pricing (pricing_id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS RentalAgreement (
  agreement_id SERIAL PRIMARY KEY,
  host_id INTEGER NOT NULL,
  guest_id INTEGER NOT NULL,
  property_id INTEGER NOT NULL,
  signing_date DATE NOT NULL DEFAULT current_date,
  total_amount FLOAT NOT NULL,
  FOREIGN KEY (host_id) REFERENCES Account (account_id) ON UPDATE CASCADE,
  FOREIGN KEY (guest_id) REFERENCES Account (account_id) ON UPDATE CASCADE,
  FOREIGN KEY (property_id) REFERENCES RentalProperty (property_id) ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS RentalDate (
  rental_date DATE NOT NULL,
  property_id INTEGER NOT NULL,
  agreement_id INTEGER NOT NULL,
  FOREIGN KEY (property_id) REFERENCES RentalProperty (property_id),
  FOREIGN KEY (agreement_id) REFERENCES RentalAgreement (agreement_id),
  PRIMARY KEY (rental_date, property_id)
);

CREATE TABLE IF NOT EXISTS Review (
  review_id SERIAL PRIMARY KEY,
  reviewer INTEGER NOT NULL,
  property INTEGER NOT NULL,
  comment VARCHAR NOT NULL,
  stars INTEGER NOT NULL,
  cleanliness INTEGER NOT NULL,
  communications INTEGER NOT NULL,
  overall_value INTEGER NOT NULL,
  FOREIGN KEY (reviewer) REFERENCES Account (account_id) ON UPDATE CASCADE,
  FOREIGN KEY (property) REFERENCES RentalProperty (property_id) ON UPDATE CASCADE,
  CONSTRAINT stars_ok CHECK (stars>=1 AND stars<=5),
  CONSTRAINT cleanliness_ok CHECK (cleanliness>=1 AND cleanliness<=5),
  CONSTRAINT communications_ok CHECK (communications>=1 AND communications<=5),
  CONSTRAINT overall_value_ok CHECK (overall_value>=1 AND overall_value<=5)
);

CREATE TABLE IF NOT EXISTS Payment (
  transaction_id SERIAL PRIMARY KEY,
  paid_by INTEGER,
  paid_to INTEGER,
  agreement_id INTEGER,
  payment_type VARCHAR,
  is_complete BOOLEAN,
  amount FLOAT,
  FOREIGN KEY (paid_by) REFERENCES Account (account_id) ON UPDATE CASCADE,
  FOREIGN KEY (paid_to) REFERENCES Account (account_id) ON UPDATE CASCADE,
  FOREIGN KEY (agreement_id) REFERENCES RentalAgreement (agreement_id) ON UPDATE CASCADE
);"""


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
        except Exception as e:
            pass
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
    with Cursor(commit=True) as cursor:
        cursor.execute(CREATE_TABLES_SQL)
