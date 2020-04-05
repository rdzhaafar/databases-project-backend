--1. Give the details of all the guests who rented properties. Please display the columns as guest
--name, rental type, rental price , signing date , branch, payment type and payment status . Sort by
--the payment type in ascending order and signing date in descending order .

select account.first_name as guest_name, rentalproperty.property_type as rental_type, rentalagreement.total_amount as rental_price, rentalagreement.signing_date as signing_date, rentalproperty.country as branch, payment.payment_type as payment_type, payment.is_complete as payment_status from (((rentalagreement join account on guest_id=account_id) join rentalproperty on rentalagreement.property_id=rentalproperty.property_id) join payment on payment.agreement_id=rentalagreement.agreement_id) order by payment_type asc, signing_date desc;

-- 2. Create a view named GuestListView that gives the details of all the guests. Please, sort the guests by the branch id and then by guest id .

Create view GuestListView as select * from account where account_id not in (select owner_id from rentalproperty) order by country ,account_id;

--3. Display the details of the cheapest (completed) rental.

Select * From RentalProperty inner join Pricing on RentalProperty.pricing_id = Pricing.pricing_id and RentalProperty.owner_id = Pricing.host where property_id in (Select property_id from RentalAgreement where total_amount in (Select min(Total_Amount) from RentalAgreement where agreement_id NOT IN (Select agreement_id from RentalDate where rental_date > current_date)));

--4. List all the properties rented and sort based on the branch id and review rating

Select RentalAgreement.property_id, country As branch_id, stars As review_rating From RentalProperty, RentalAgreement, Review where RentalProperty.property_id = RentalAgreement.property_id and Review.property = RentalProperty.property_id Order By branch_id, review_rating;

--5. Find the properties that are already listed but not yet rented. Please, avoid duplications.

Select distinct property_id from RentalProperty where property_id not in (Select property_id from RentalAgreement);

--6. List all the details of all properties rented on the 10 th day of any month. Ensure to insert dates in your table that correspond in order to run your query.

Select * from RentalProperty where property_id in (Select property_id from RentalDate where Extract(DAY FROM rental_date) = 10)

--7. List all the managers and the employees with salary greater than or equal to $ 15000 by their ids, names, branch ids , branch names and salary . Sort by manager id and then by employee id .

Select * from Employee where salary >= 15000 order by manager, employee_id;

--8. Consider creating a simple bill for a guest stating the property type , host, address, amount paid and payment type .

Select property_type, host_id, street, street_no, unit, zip, state_province, country, total_amount, payment_type from RentalProperty, RentalAgreement, Payment where paid_by = <guest_id_goes_here> and RentalAgreement.agreement_id = Payment.agreement_id and RentalProperty.property_id = RentalAgreement.property_id;

--9. Update the phone number of a guest.

Update Account set phone = <new_phone_number_goes_here> where account_id = <guest_id_goes_here>;

--10.Create and test a user-defined function named FirstNameFirst that combines two attributes of the guest named firstName and lastName into a concatenated value named fullName [e.g., James and Brown will be combined to read James Brown ].

CREATE FUNCTION FirstNameFirst (first_name VARCHAR, last_name VARCHAR)
RETURNS VARCHAR as $$
    BEGIN 
       RETURN (SELECT  first_Name || ' ' || last_Name );
    END $$  LANGUAGE plpgsql STRICT IMMUTABLE;