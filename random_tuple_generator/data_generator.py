import random
import json
import datetime
import requests
import sys

"""
This script generates some random data and populates the database
upon starting the application, then exits.


My software engineering professor would refer to the following as
"Spaghetti code". He's Right.
"""


def new_branch():
    countryList = ["Switzerland", "Canada", "Japan", "Germany", "Australia", "United Kingdom", "United States",
                   "Sweden", "Netherlands", "Norway", "New Zealand", "France", "Denmark", "Finland", "China",
                   "Singapore", "Austria", "Spain", "South Korea", "Russia", "Portugal", "United Arab Emirates",
                   "India"]
    for country in countryList:
        branch = {
            "country": country,
            "branch_manager": None
        }
        post_data("http://database-backend:5000/branch/new", branch)


def get_branches():
    response = requests.get("http://database-backend:5000/branch/get")
    branches = json.loads(response.content)
    return branches


def update_managers():
    managers = get_employee()
    for manager in managers:
        update = {
            "country": manager["branch"],
            "branch_manager": manager["employee_id"]
        }
        post_data("http://database-backend:5000/branch/manager", update)


def new_employee(managers=False):
    firstNameString = "James,John,Robert,Michael,William,David,Richard,Joseph,Thomas,Charles,Christopher,Daniel,Matthew,Anthony,Donald,Mark,Paul,Steven,Andrew,Kenneth,Joshua,George,Kevin,Brian,Edward,Ronald,Timothy,Jason,Jeffrey,Ryan,Jacob,Gary,Nicholas,Eric,Stephen,Jonathan,Larry,Justin,Scott,Brandon,Frank,Benjamin,Gregory,Samuel,Raymond,Patrick,Alexander,Jack,Dennis,Jerry,Tyler,Aaron,Jose,Henry,Douglas,Adam,Peter,Nathan,Zachary,Walter,Kyle,Harold,Carl,Jeremy,Keith,Roger,Gerald,Ethan,Arthur,Terry,Christian,Sean,Lawrence,Austin,Joe,Noah,Jesse,Albert,Bryan,Billy,Bruce,Willie,Jordan,Dylan,Alan,Ralph,Gabriel,Roy,Juan,Wayne,Eugene,Logan,Randy,Louis,Russell,Vincent,Philip,Bobby,Johnny,Bradley,Mary,Patricia,Jennifer,Linda,Elizabeth,Barbara,Susan,Jessica,Sarah,Karen,Nancy,Margaret,Lisa,Betty,Dorothy,Sandra,Ashley,Kimberly,Donna,Emily,Michelle,Carol,Amanda,Melissa,Deborah,Stephanie,Rebecca,Laura,Sharon,Cynthia,Kathleen,Helen,Amy,Shirley,Angela,Anna,Brenda,Pamela,Nicole,Ruth,Katherine,Samantha,Christine,Emma,Catherine,Debra,Virginia,Rachel,Carolyn,Janet,Maria,Heather,Diane,Julie,Joyce,Victoria,Kelly,Christina,Joan,Evelyn,Lauren,Judith,Olivia,Frances,Martha,Cheryl,Megan,Andrea,Hannah,Jacqueline,Ann,Jean,Alice,Kathryn,Gloria,Teresa,Doris,Sara,Janice,Julia,Marie,Madison,Grace,Judy,Theresa,Beverly,Denise,Marilyn,Amber,Danielle,Abigail,Brittany,Rose,Diana,Natalie,Sophia,Alexis,Lori,Kayla,Jane"
    firstNameList = firstNameString.split(",")
    lastNameString = "Smith,Johnson,Williams,Jones,Brown,Davis,Miller,Wilson,Moore,Taylor,Anderson,Thomas,Jackson,White,Harris,Martin,Thompson,Garcia,Martinez,Robinson,Clark,Rodriguez,Lewis,Lee,Walker,Hall,Allen,Young,Hernandez,King,Wright,Lopez,Hill,Scott,Green,Adams,Baker,Gonzalez,Nelson,Carter,Mitchell,Perez,Roberts,Turner,Philips,Campbell,Parker,Evans,Edwards,Collins,Stewart,Sanchez,Morris,Rogers,Reed,Cook,Morgan,Bell,Murphy,Bailey,Rivera,Cooper,Richardson,Cox,Howard,Ward,Torres,Peterson,Gray,Ramirez,James,Watson,Brooks,Kelly,Sanders,Price,Bennett,Wood,Barnes,Ross,Henderson,Coleman,Jenkins,Perry,Powell,Long,Patterson,Hughes,Flores,Washington,Butler,Simmons,Foster,Bryant,Alexander,Russell,Griffin,Diaz,Hayes,Myers,Ford,Hamilton,Graham,Sullivan,Wallace,Woods,Cole,West,Jordan,Owens,Reynolds,Fisher,Ellis,Harrison,Gibson,Mcdonald,Cruz,Marshall,Ortiz,Gomez,Murray,Freeman,Wells,Webb,Simpson,Stevens,Tucker,Porter,Hunter,Hicks,Crawford,Henry,Boyd,Mason,Morales,Kennedy,Warren,Dixon,Ramos,Reyes,Burns,Gordon,Shaw,Holmes,Rice,Robertson,Hunt,Black,Daniels"
    lastNameList = lastNameString.split(",")
    positionList = ["Associate", "Superviser", "Broker", "Property Manager", "General Manager", "Branch Manager",
                    "Listing Management Officer"]
    if managers:
        branches = get_branches()
        for branch in branches:
            tempFirstName = random.choice(firstNameList)
            tempLastName = random.choice(lastNameList)
            tempSalary = random.randint(10000, 40000)

            tempDict = {
                "employee_username": branch["country"] + tempFirstName + tempLastName,
                "employee_password": "password",
                "first_name": tempFirstName,
                "last_name": tempLastName,
                "branch": branch["country"],
                "manager": None,
                "salary": tempSalary,
                "position": "branch director"
            }
            post_data("http://database-backend:5000/employee/new", tempDict)
        return
    managers = get_employee()
    for manager in managers:
        branch = manager["branch"]
        manager_id = manager["employee_id"]
        for i in range(random.randint(2, 10)):
            tempFirstName = random.choice(firstNameList)
            tempLastName = random.choice(lastNameList)
            tempSalary = random.randint(10000, 40000)
            tempPosition = random.choice(positionList)
            tempDict = {
                "employee_username": str(i) + tempFirstName + tempLastName,
                "employee_password": "password",
                "first_name": tempFirstName,
                "last_name": tempLastName,
                "branch": branch,
                "manager": manager_id,
                "salary": tempSalary,
                "position": tempPosition
            }
            post_data("http://database-backend:5000/employee/new", tempDict)


def get_employee():
    response = requests.get("http://database-backend:5000/employee/get")
    employees = json.loads(response.content)
    return employees


def post_data(endpoint, row):
    resp = requests.post(endpoint, json=row)


def new_account(n):
    firstNameString = "James,John,Robert,Michael,William,David,Richard,Joseph,Thomas,Charles,Christopher,Daniel,Matthew,Anthony,Donald,Mark,Paul,Steven,Andrew,Kenneth,Joshua,George,Kevin,Brian,Edward,Ronald,Timothy,Jason,Jeffrey,Ryan,Jacob,Gary,Nicholas,Eric,Stephen,Jonathan,Larry,Justin,Scott,Brandon,Frank,Benjamin,Gregory,Samuel,Raymond,Patrick,Alexander,Jack,Dennis,Jerry,Tyler,Aaron,Jose,Henry,Douglas,Adam,Peter,Nathan,Zachary,Walter,Kyle,Harold,Carl,Jeremy,Keith,Roger,Gerald,Ethan,Arthur,Terry,Christian,Sean,Lawrence,Austin,Joe,Noah,Jesse,Albert,Bryan,Billy,Bruce,Willie,Jordan,Dylan,Alan,Ralph,Gabriel,Roy,Juan,Wayne,Eugene,Logan,Randy,Louis,Russell,Vincent,Philip,Bobby,Johnny,Bradley,Mary,Patricia,Jennifer,Linda,Elizabeth,Barbara,Susan,Jessica,Sarah,Karen,Nancy,Margaret,Lisa,Betty,Dorothy,Sandra,Ashley,Kimberly,Donna,Emily,Michelle,Carol,Amanda,Melissa,Deborah,Stephanie,Rebecca,Laura,Sharon,Cynthia,Kathleen,Helen,Amy,Shirley,Angela,Anna,Brenda,Pamela,Nicole,Ruth,Katherine,Samantha,Christine,Emma,Catherine,Debra,Virginia,Rachel,Carolyn,Janet,Maria,Heather,Diane,Julie,Joyce,Victoria,Kelly,Christina,Joan,Evelyn,Lauren,Judith,Olivia,Frances,Martha,Cheryl,Megan,Andrea,Hannah,Jacqueline,Ann,Jean,Alice,Kathryn,Gloria,Teresa,Doris,Sara,Janice,Julia,Marie,Madison,Grace,Judy,Theresa,Beverly,Denise,Marilyn,Amber,Danielle,Abigail,Brittany,Rose,Diana,Natalie,Sophia,Alexis,Lori,Kayla,Jane"
    firstNameList = firstNameString.split(",")
    lastNameString = "Smith,Johnson,Williams,Jones,Brown,Davis,Miller,Wilson,Moore,Taylor,Anderson,Thomas,Jackson,White,Harris,Martin,Thompson,Garcia,Martinez,Robinson,Clark,Rodriguez,Lewis,Lee,Walker,Hall,Allen,Young,Hernandez,King,Wright,Lopez,Hill,Scott,Green,Adams,Baker,Gonzalez,Nelson,Carter,Mitchell,Perez,Roberts,Turner,Philips,Campbell,Parker,Evans,Edwards,Collins,Stewart,Sanchez,Morris,Rogers,Reed,Cook,Morgan,Bell,Murphy,Bailey,Rivera,Cooper,Richardson,Cox,Howard,Ward,Torres,Peterson,Gray,Ramirez,James,Watson,Brooks,Kelly,Sanders,Price,Bennett,Wood,Barnes,Ross,Henderson,Coleman,Jenkins,Perry,Powell,Long,Patterson,Hughes,Flores,Washington,Butler,Simmons,Foster,Bryant,Alexander,Russell,Griffin,Diaz,Hayes,Myers,Ford,Hamilton,Graham,Sullivan,Wallace,Woods,Cole,West,Jordan,Owens,Reynolds,Fisher,Ellis,Harrison,Gibson,Mcdonald,Cruz,Marshall,Ortiz,Gomez,Murray,Freeman,Wells,Webb,Simpson,Stevens,Tucker,Porter,Hunter,Hicks,Crawford,Henry,Boyd,Mason,Morales,Kennedy,Warren,Dixon,Ramos,Reyes,Burns,Gordon,Shaw,Holmes,Rice,Robertson,Hunt,Black,Daniels"
    lastNameList = lastNameString.split(",")
    countryList = ["Switzerland", "Canada", "Japan", "Germany", "Australia", "United Kingdom", "United States",
                   "Sweden", "Netherlands", "Norway", "New Zealand", "France", "Denmark", "Finland", "China",
                   "Singapore", "Austria", "Spain", "South Korea", "Russia", "Portugal", "United Arab Emirates",
                   "India"]
    for x in range(n):
        tempFirstName = random.choice(firstNameList)
        tempLastName = random.choice(lastNameList)
        tempCountry = random.choice(countryList)
        tempDict = {
            "country": tempCountry,
            "first_name": tempFirstName,
            "last_name": tempLastName,
            "email": tempFirstName + "." + tempLastName + str(x) + "@uottawa.ca",
            "phone": "555-555-5555",
            "username": tempFirstName + tempLastName + str(x),
            "account_password": "password"}
        post_data("http://database-backend:5000/account/new", tempDict)


def get_accounts():
    response = requests.get("http://database-backend:5000/account/get")
    accounts = json.loads(response.content)
    return accounts


def select_hosts(accounts):
    num_hosts = len(accounts) // 2
    hosts = []
    for i in range(num_hosts):
        hosts.append(accounts[i])
    return hosts


def new_pricing(hosts):
    classNameList = ["Luxury", "Budget", "Economy", "Basic"]
    homeTypeList = ["Apartment", "Bungalow", "Townhouse", "Cottage", "Cabin", "Mansion", "Mobile Home", "Castle"]
    rulesList = ["No Pets", "No Parties", "No Events", "No Unregistered Guests", "No Eating or Drinking in Bedrooms",
                 "No Smoking", "No Children"]
    amenitiesList = ["Wifi", "TV", "Air Conditioning", "Heating", "Kitchen", "Free Parking", "Swimming Pool", "Sauna"]

    for h in hosts:
        host_id = h["account_id"]
        for i in range(random.randint(1, 5)):
            tempClassName = random.choice(classNameList)
            tempPrice = round(random.uniform(10, 500), 2)
            tempHomeType = random.choice(homeTypeList)
            tempBedroom = random.randint(1, 5)

            i = 0
            tempRulesList = []
            while i < 3:
                tempRule = random.choice(rulesList)
                if tempRule not in tempRulesList:
                    tempRulesList.append(tempRule)
                    i += 1
            tempRulesString = " , ".join(tempRulesList)

            i = 0
            tempAmenitiesList = []
            while i < 3:
                tempAmenity = random.choice(amenitiesList)
                if tempAmenity not in tempAmenitiesList:
                    tempAmenitiesList.append(tempAmenity)
                    i += 1
            tempAmenitiesString = " , ".join(tempAmenitiesList)

            tempDict = {
                "class_name": tempClassName,
                "host": host_id,
                "price": tempPrice,
                "home_type": tempHomeType,
                "rules": tempRulesString,
                "amenities": tempAmenitiesString,
                "accomodates": tempBedroom
            }
            post_data("http://database-backend:5000/pricing/new", tempDict)


def get_pricing():
    response = requests.get("http://database-backend:5000/pricing/get")
    pricing = json.loads(response.content)
    return pricing


def new_rentalproperty(pricings):
    streetList = ["Dogwood Lane", "Second Street", "First Avenue", "Pine Drive", "Oak Road", "Park Lane",
                  "Jackson Street", "Airport Avenue", "Spruce Crescent", "Birch Way", "Main Street", "Willow Avenue",
                  "Apache Drive", "Palo Verde Way", "Mesquite Drive", "Sunset Road", "Navajo Crescent", "Quail Road",
                  "Cedar Street", "Elm Avenue", "Maple Lane", "Cypress Drive", "Redwood Avenue", "Aspen Street",
                  "Columbine Road", "Laurel Lane", "Lake Road", "Meadow Way", "West Avenue", "Hillside Lane",
                  "Evergreen Drive", "Ridge Road", "Holly Lane", "Church Road", "Delaware Street", "Bay Street",
                  "Williams Drive", "Magnolia Avenue", "Lakeview Lane", "Lehua Street", "Kukui Way", "Kahili Drive",
                  "Aloha Crescent", "Malulani Avenue", "Lincoln Street", "Hickory Road", "Walnut Street",
                  "Washington Street", "County Line Way", "Sycamore Road", "Johnson Street", "Smith Avenue",
                  "Wilson Lane", "Shore Drive", "Hemlock Way", "Highland Road", "Pleasant Drive", "Canyon Road",
                  "Cottonwood Lane", "Pioneer Road", "River Street", "Mountain View Road", "Pinon Way", "Juniper Drive",
                  "North Street", "Broadway Road", "Cherry Street", "Narragansett Avenue", "Wood Lane",
                  "Hampton Street", "Pecan Road", "Center Street", "Hill Road", "Lee Street", "Orchard Road"]
    countryList = ["Switzerland", "Canada", "Japan", "Germany", "Australia", "United Kingdom", "United States",
                   "Sweden", "Netherlands", "Norway", "New Zealand", "France", "Denmark", "Finland", "China",
                   "Singapore", "Austria", "Spain", "South Korea", "Russia", "Portugal", "United Arab Emirates",
                   "India"]
    cityList = ["Kingston", "Oakland", "Washingston", "Waverly", "Dayton", "Burlington", "Milford", "Newport",
                "Chester", "Riverside", "Oxford", "Ashland", "Milton", "Springfield", "Manchester", "Clayton",
                "Georgetown", "Arlington", "Salem", "Marion", "Madison", "Greenville", "Clinton", "Fairview",
                "Franklin"]
    roomTypeList = ["Entire Apartment", "Entire Loft", "Private Room", "Hotel Room", "Shared Room"]
    for p in pricings:
        pricing_id = p["pricing_id"]
        host_id = p["host"]
        accomodates = p["accomodates"]
        numRentalProperty = random.randint(1, 5)
        # generate tuple and post
        for x in range(numRentalProperty):
            tempStreet = random.choice(streetList)
            tempStreetNo = random.randint(1000, 9999)
            tempUnit = random.randint(100, 999)
            tempZip = random.randint(10000, 99999)
            tempCity = random.choice(cityList)
            tempCountry = random.choice(countryList)
            tempRoomType = random.choice(roomTypeList)
            tempBathroom = random.randint(1, accomodates)

            tempDict = {
                "city": tempCity,
                "street": tempStreet,
                "street_no": tempStreetNo,
                "unit": tempUnit,
                "zip": tempZip,
                "state_province": "Ontario",
                "country": tempCountry,
                "owner_id": host_id,
                "property_type": "Residential",
                "room_type": tempRoomType,
                "pricing_id": pricing_id,
                "bathroom": tempBathroom,
                "bedroom": accomodates,
                "bed": json.dumps({"twin": accomodates,
                                   "double": 0,
                                   "queen": 0,
                                   "king": 0})
            }
            post_data("http://database-backend:5000/rentalproperty/new", tempDict)


def get_rentalproperty():
    response = requests.get("http://database-backend:5000/rentalproperty/get")
    rentalproperty = json.loads(response.content)
    return rentalproperty


def get_rentalagreement():
    response = requests.get("http://database-backend:5000/rentalagreement/get")
    rentalproperty = json.loads(response.content)
    return rentalproperty


def new_rentalagreement():
    rentalproperties = get_rentalproperty()
    guests = get_accounts()
    pricings = get_pricing()
    rental_agreements = []
    for prop in rentalproperties:
        # datesBooked = []
        host = prop["owner_id"]
        for _ in range(random.randint(0, 5)):
            guest = random.choice(guests)
            while guest["account_id"] == host:
                guest = random.choice(guests)
            tempDict = {
                "host_id": host,
                "guest_id": guest["account_id"],
                "property_id": prop["property_id"],
                "duration": random.randint(1, 30)
            }
            rental_agreements.append(tempDict)
    for rental in rental_agreements:
        rental_i = 0
        pricing_i = 0
        while rental["property_id"] != rentalproperties[rental_i]["property_id"]:
            rental_i += 1
        while rentalproperties[rental_i]["pricing_id"] != pricings[pricing_i]["pricing_id"]:
            pricing_i += 1
        rental["total_amount"] = round(pricings[pricing_i]["price"] * rental["duration"], 2)

    # half for before today
    for rental in range(len(rental_agreements) // 2):
        rental_agreements[rental]["signing_date"] = datetime.date.isoformat(
            datetime.date.today() - datetime.timedelta(days=random.randint(30, 1800)))

    # half for after today
    for rental in range(len(rental_agreements) // 2, len(rental_agreements)):
        rental_agreements[rental]["signing_date"] = datetime.date.isoformat(
            datetime.date.today() + datetime.timedelta(days=random.randint(30, 1800)))

    # insert rental agreements
    for rental in rental_agreements:
        post_data("http://database-backend:5000/rentalagreement/new", rental)

    # get rental agreements (for the ids)
    rentalwithIDs = get_rentalagreement()

    # add rentaldates tuples to table
    rentaldates = []
    for i in range(len(rentalwithIDs)):
        for x in range(rental_agreements[i]["duration"]):
            tempSigningdate = rental_agreements[i]["signing_date"]
            convertedSigningdate = datetime.date.fromisoformat(tempSigningdate)
            tempTimeDelta = datetime.timedelta(days=x + 1)
            tempFinalDate = datetime.date.isoformat(convertedSigningdate + tempTimeDelta)

            rentaldates.append({"rental_date": tempFinalDate,
                                "property_id": rentalwithIDs[i]["property_id"],
                                "agreement_id": rentalwithIDs[i]["agreement_id"]})

    for rental_date in rentaldates:
        post_data("http://database-backend:5000/rentaldate/new", rental_date)


def new_payment():
    paymentTypeList = ["Credit Card", "Debit", "Check", "Cash", "Mobile Payment", "Bitcoin"]

    rentalagreements = get_rentalagreement()

    # generate tuple and post
    for rental in rentalagreements:
        tempAgreementID = rental["agreement_id"]
        tempPaymentType = random.choice(paymentTypeList)
        tempAmount = rental["total_amount"]

        # construct payment tuple
        tempDict = {
            "paid_by": rental["guest_id"],
            "paid_to": rental["host_id"],
            "agreement_id": tempAgreementID,
            "payment_type": tempPaymentType,
            "is_complete": True,
            "amount": tempAmount
        }
        post_data("http://database-backend:5000/payment/new", tempDict)


def new_review(n):
    # generate tuple and post data
    rentalproperty = get_rentalproperty()
    accounts = get_accounts()

    for _ in range(n):
        tempReviewer = random.choice(accounts)["account_id"]
        tempProperty = random.choice(rentalproperty)["property_id"]
        tempStars = random.randint(1, 5)
        tempCleanliness = random.randint(1, 5)
        tempCommunications = random.randint(1, 5)
        tempOverallValue = random.randint(1, 5)
        tempCommentList = []

        if tempCleanliness == 1:
            tempCommentList.append("Extremely Dirty")
        elif tempCleanliness == 2:
            tempCommentList.append("Very Dirty")
        elif tempCleanliness == 3:
            tempCommentList.append("Acceptably Clean")
        elif tempCleanliness == 4:
            tempCommentList.append("Very Clean")
        elif tempCleanliness == 5:
            tempCommentList.append("Extremely Clean")

        if tempCommunications == 1:
            tempCommentList.append("Communications are Very Slow and Confusing")
        elif tempCommunications == 2:
            tempCommentList.append("Communications are Slow and Unclear")
        elif tempCommunications == 3:
            tempCommentList.append("Communications are Quick but Rude")
        elif tempCommunications == 4:
            tempCommentList.append("Quick Responses")
        elif tempCommunications == 5:
            tempCommentList.append("Communications are Fast and Friendly")

        if tempOverallValue == 1:
            tempCommentList.append("Very Expensive")
        elif tempOverallValue == 2:
            tempCommentList.append("Pricey")
        elif tempOverallValue == 3:
            tempCommentList.append("Worth the price")
        elif tempOverallValue == 4:
            tempCommentList.append("Good Deal")
        elif tempOverallValue == 5:
            tempCommentList.append("Very Cheap")

        tempComment = ". ".join(tempCommentList)

        tempDict = {
            "reviewer": tempReviewer,
            "property": tempProperty,
            "comment": tempComment,
            "stars": tempStars,
            "cleanliness": tempCleanliness,
            "communications": tempCommunications,
            "overall_value": tempOverallValue
        }
        post_data("http://database-backend:5000/review/new", tempDict)


def generate_random_data():
    session = requests.Session()
    session.trust_env = False
    # retry connecting to the backend container until success, then break
    while True:
        try:
            response = requests.get("http://database-backend:5000/")
            if response.status_code == 200:
                break
        except:
            continue
    new_branch()
    new_employee(managers=True)
    update_managers()
    new_employee()
    new_account(15)
    accounts = get_accounts()
    hosts = select_hosts(accounts)
    new_pricing(hosts)
    pricing = get_pricing()
    new_rentalproperty(pricing)
    rentalproperty = get_rentalproperty()
    new_rentalagreement()
    new_payment()
    new_review(20)
    print("done!")

if __name__=="__main__":
    generate_random_data()
    sys.exit(0)