CREATE TABLE IF NOT EXISTS RentalAgreement (
  agreement_id SERIAL PRIMARY KEY,
  rental_period Date[] NOT NULL,
  hostid INTEGER NOT NULL,
  guest_id INTEGER NOT NULL,
  property_id INTEGER NOT NULL,
  signing_date DATE NOT NULL,
  total_amount FLOAT NOT NULL,
  Foreign Key (hostid) references Account (account_id),
  Foreign Key (guest_id) references Account (account_id),
  Foreign Key (property_id) references RentalProperty (property_id)
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
  Foreign Key (reviewer) references Account (account_id),
  Foreign Key (property) references RentalProperty (property_id),
  CONSTRAINT stars_ok CHECK (stars>=1 AND stars<=5),
  CONSTRAINT cleanliness_ok CHECK (cleanliness>=1 AND cleanliness<=5),
  CONSTRAINT communications_ok CHECK (communications>=1 AND communications<=5),
  CONSTRAINT overall_value_ok CHECK (overall_value>=1 AND overall_value<=5)
);

CREATE TABLE IF NOT EXISTS Pricing (
  pricing_id SERIAL PRIMARY KEY,
  class_name varchar NOT NULL,
  host INTEGER NOT NULL,
  price float NOT NULL,
  home_type varchar NOT NULL,
  rules varchar,
  amenities varchar,
  accomodates Integer NOT NULL,
  Foreign Key (host) references Account (account_id),
  CONSTRAINT accomodates_ok CHECK (accomodates>=1)
);

CREATE TABLE IF NOT EXISTS Payment (
  transaction_id SERIAL PRIMARY KEY,
  paid_by INTEGER,
  paid_to INTEGER,
  agreement_id INTEGER,
  payment_type varchar,
  is_complete boolean,
  amount float,
  Foreign Key (paid_by) references Account (account_id),
  Foreign Key (paid_to) references Account (account_id),
  Foreign Key (agreement_id) references RentalAgreement (agreement_id)
);

CREATE TABLE IF NOT EXISTS Branches (
  country varchar PRIMARY KEY,
  branch_manager INTEGER NOT NULL,
  Foreign Key (branch_manager) references Employee (employee_id),
);

CREATE TABLE IF NOT EXISTS Account (
  account_id Serial PRIMARY KEY,
  first_name varchar NOT NULL,
  last_name varchar NOT NULL,
  email varchar UNIQUE NOT NULL,
  phone varchar,
  username varchar  NOT NULL,
  account_password varchar NOT NULL
);

CREATE TABLE IF NOT EXISTS RentalProperty (
  property_id SERIAL PRIMARY KEY,
  street varchar NOT NULL,
  street_no INTEGER NOT NULL,
  unit INTEGER NOT NULL,
  zip varchar NOT NULL,
  state_province varchar NOT NULL,
  country varchar NOT NULL,
  owner_id INTEGER NOT NULL,
  property_type varchar NOT NULL,
  room_type varchar NOT NULL,
  booked_dates date[] NOT NULL,
  pricing_id INTEGER NOT NULL,
  bathroom INTEGER NOT NULL,
  bedroom INTEGER NOT NULL,
  bed JSON NOT NULL,
  Foreign Key (country) references Branches (country),
  Foreign Key (owner_id) references Account (account_id),
  Foreign Key (pricing_id) references Pricing (pricing_id)
);

CREATE TABLE IF NOT EXISTS Employee (
  employee_id SERIAL PRIMARY KEY,
  employee_username UNIQUE NOT NULL,
  employee_password NOT NULL,
  branch varchar NOT NULL,
  manager INTEGER NOT NULL,
  salary INTEGER NOT NULL,
  position varchar NOT NULL,
  Foreign Key (manager) references Employee (employee_id),
  Foreign Key (branch) references Branches (country)
);

CREATE TABLE IF NOT EXISTS AllTheDates (
  a_day DATE PRIMARY KEY
);