#Rebuilds database from scratch, then imports data from 'Library_Usage_Data.csv'

from login import getConnection
from enum import Enum

connection = getConnection()
cursor = connection.cursor()

#create and use SFILS database
print("Rebuilding SFILS database...")
cursor.execute("DROP DATABASE SFILS")
cursor.execute("CREATE DATABASE IF NOT EXISTS SFILS")
cursor.execute("USE SFILS")
print("SFILS database rebuilt!")

print("Creating Tables:")
print("Creating Patron Type table...")
createPatronTypeTable = """
CREATE TABLE PATRON_TYPE(
    type_id INT NOT NULL PRIMARY KEY,
    type_def CHAR(25)
)
"""
cursor.execute(createPatronTypeTable)

print("Creating Library table...")
createLibraryTable = """
CREATE TABLE LIBRARY (
    library_code CHAR(5) NOT NULL PRIMARY KEY,
    library_def CHAR(25)
);
"""
cursor.execute(createLibraryTable)

print("Creating Notification Preference Code")
createNotificationPreferenceTable = """
CREATE TABLE NOTIFICATION_PREFERENCE (
    notification_type_code CHAR(2) NOT NULL PRIMARY KEY,
    notification_type_def CHAR(10)
);
"""
cursor.execute(createNotificationPreferenceTable)

print("Creating Patron Table...")
createPatronTable = """
CREATE TABLE PATRON (
id INT NOT NULL AUTO_INCREMENT,
patron_type INT NOT NULL,
total_checkouts INT NOT NULL,
total_renewals INT NOT NULL,
age_range VARCHAR(20),
home_library CHAR(5) NOT NULL,
circulation_active_month CHAR(20),
circulation_active_year INT,
notification_preference CHAR(2) NOT NULL,
email_provided BOOL NOT NULL,
within_sf_county BOOL,
year_registered INT NOT NULL,


PRIMARY KEY (id),

CONSTRAINT fk_library
FOREIGN KEY (home_library)
REFERENCES LIBRARY(library_code),

CONSTRAINT fk_patron_type
FOREIGN KEY (patron_type)
REFERENCES PATRON_TYPE(type_id),

CONSTRAINT fk_notification_preference
FOREIGN KEY (notification_preference)
REFERENCES NOTIFICATION_PREFERENCE(notification_type_code)
);
"""
cursor.execute(createPatronTable)
print("Tables created!")

class Column(Enum):
    PATRON_TYPE_CODE        = 0
    PATRON_TYPE_DEF         = 1
    TOTAL_CHECKOUTS         = 2
    TOTAL_RENEWALS          = 3
    AGE_RANGE               = 4
    HOME_LIBRARY_CODE       = 5
    HOME_LIBRARY_DEF        = 6
    ACTIVE_MONTH            = 7
    ACTIVE_YEAR             = 8
    NOTICE_PREFERENCE_CODE  = 9
    NOTICE_PREFERENCE_DEF   = 10
    PROVIDED_EMAIL          = 11
    WITHIN_SF               = 12
    YEAR_REGISTERED         = 13
    

i = 0
with open("Library_Usage_Data.csv", "r") as file:
    #read each row of the data
    file.readline()
    for line in file:
        #split into columns
        columns = line.split(",")

        #add patron type to PATRON_TYPE table if not already in
        insertPatronType = "INSERT IGNORE INTO PATRON_TYPE (type_id, type_def) VALUES (%s, %s);"
        val = (columns[Column.PATRON_TYPE_CODE.value], columns[Column.PATRON_TYPE_DEF.value])
        cursor.execute(insertPatronType, val)    

        #add library to LIBRARY table if not already in
        insertLibrary = "INSERT IGNORE INTO LIBRARY (library_code, library_def) VALUES (%s, %s);"
        val = (columns[Column.HOME_LIBRARY_CODE.value], columns[Column.HOME_LIBRARY_DEF.value])
        cursor.execute(insertLibrary, val)

        #add notification preference to NOTIFICATION_PREFERENCE table if not already in
        insertNotifPreference = "INSERT IGNORE INTO NOTIFICATION_PREFERENCE (notification_type_code, notification_type_def) VALUES (%s, %s);"
        val = (columns[Column.NOTICE_PREFERENCE_CODE.value], columns[Column.NOTICE_PREFERENCE_DEF.value])
        cursor.execute(insertNotifPreference, val)

        patronType = columns[Column.PATRON_TYPE_CODE.value]
        totalCheckouts = columns[Column.TOTAL_CHECKOUTS.value]
        ageRange = "'" + columns[Column.AGE_RANGE.value] + "'"
        homeLibraryCode = "'" + columns[Column.HOME_LIBRARY_CODE.value] + "'"

        activeMonth = "'" + columns[Column.ACTIVE_MONTH.value] + "'"

        activeYear = str("NULL")
        if columns[Column.ACTIVE_YEAR.value].isdigit():
            activeYear = columns[Column.ACTIVE_YEAR.value]

        noticePreference = "'" + columns[Column.NOTICE_PREFERENCE_CODE.value] + "'"
        totalRenewals = columns[Column.TOTAL_RENEWALS.value]

        emailProvided = 0
        if columns[Column.PROVIDED_EMAIL.value] == "True":
            emailProvided = 1

        yearRegistered = columns[Column.YEAR_REGISTERED.value].rstrip('\n')


        #add entry to patrons table
        insertPatron = """
        INSERT INTO PATRON
        VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        val = (
            patronType,
            totalCheckouts,
            totalRenewals,
            ageRange,
            homeLibraryCode,
            activeMonth,
            activeYear,
            noticePreference,
            emailProvided,
            0,
            yearRegistered
        )
        cursor.execute(insertPatron % val)

        i += 1
        if i %10000 == 0: 
            print("Importing Data: " + str(i))

        #limit number of entries to import?
        # if i > 100000:
        #     break
        

connection.commit()
connection.close()