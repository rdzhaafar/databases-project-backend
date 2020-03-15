CREATE TABLE "RentalAgreement" (
  "AgreementID" UUID,
  "RentalPeriod" daterange,
  "Host" UUID,
  "Guest" UUID,
  "Property" UUID,
  "SigningDate" date,
  "TotalAmount" float,
  PRIMARY KEY ("AgreementID")
);

CREATE INDEX "FK" ON  "RentalAgreement" ("Host", "Guest", "Property");

CREATE TABLE "Review" (
  "ReviewID" UUID,
  "Reviewer" UUID,
  "Property" UUID,
  "Comment" varchar,
  "Stars" int,
  "Cleanliness" int,
  "Communications" int,
  "Value" int,
  PRIMARY KEY ("ReviewID")
);

CREATE INDEX "FK" ON  "Review" ("Reviewer", "Property");

CREATE TABLE "Pricing" (
  "Class" varchar,
  "Host" UUID,
  "Price" float,
  "HomeType" varchar,
  "Rules" varchar,
  "Amenities" varchar,
  "AllowedNoGuests" int,
  PRIMARY KEY ("Class")
);

CREATE INDEX "FK" ON  "Pricing" ("Host");

CREATE TABLE "Payment" (
  "TransactionID" UUID,
  "PaidBy" UUID,
  "PaidTo" UUID,
  "PaidFor" UUID,
  "Type" varchar,
  "IsComplete" boolean,
  "Amount" float,
  PRIMARY KEY ("TransactionID")
);

CREATE INDEX "FK" ON  "Payment" ("PaidBy", "PaidTo", "PaidFor");

CREATE TABLE "Branches" (
  "Country" varchar,
  "BranchManager" UUID,
  PRIMARY KEY ("Country")
);

CREATE INDEX "FK" ON  "Branches" ("BranchManager");

CREATE TABLE "User" (
  "UserID" UUID,
  "FirstName" varchar,
  "LastName" varchar,
  "Email" varchar,
  "Phone" varchar,
  "Username" varchar,
  "Password" varchar,
  PRIMARY KEY ("UserID")
);

CREATE TABLE "RentalProperty" (
  "PropertyID" UUID,
  "Street" varchar,
  "StreetNo" int,
  "Unit" int,
  "Zip" varchar,
  "State" varchar,
  "Country" varchar,
  "Owner" UUID,
  "Type" varchar,
  "RoomType" varchar,
  "AvailableDates()" daterange,
  "Class" varchar,
  "Bathroom" int,
  "Bedroom" int,
  "Bed" JSON,
  PRIMARY KEY ("PropertyID")
);

CREATE INDEX "FK" ON  "RentalProperty" ("Country", "Owner", "Class");

CREATE TABLE "Employee" (
  "EmployeeID" UUID,
  "Branch" varchar,
  "Manager" UUID,
  "Salary" int,
  "Position" varchar,
  PRIMARY KEY ("EmployeeID")
);

CREATE INDEX "FK" ON  "Employee" ("Branch", "Manager");

