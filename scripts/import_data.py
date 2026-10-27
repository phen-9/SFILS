from login import getConnection
from enum import Enum

dataBase = getConnection()
cursor = dataBase.cursor()

#create and use SFILS database
print("Rebuilding SFILS database...")
cursor.execute("DROP DATABASE SFILS")
cursor.execute("CREATE DATABASE IF NOT EXISTS SFILS")
cursor.execute("USE SFILS")
print("SFILS database rebuilt!")

print("Creating Tables:")
print("Creating Library table...")
createLibraryTable = """
CREATE TABLE LIBRARY (
    name CHAR(20) NOT NULL PRIMARY KEY
);
"""
cursor.execute(createLibraryTable)

print("Creating PatronType table...")
createPatronTypeTable = """
CREATE TABLE PATRONTYPE(
    name CHAR(15) NOT NULL PRIMARY KEY
)
"""
cursor.execute(createPatronTypeTable)

print("Creating Patron Table...")
createPatronTable = """
CREATE TABLE PATRON (
id INT NOT NULL AUTO_INCREMENT,
patron_type CHAR(15) NOT NULL,
total_checkouts INT NOT NULL,
total_renewals INT NOT NULL,
age_range VARCHAR(15) NOT NULL,
home_library CHAR(20) NOT NULL,
circulation_active_month CHAR(3),
circulation_active_year YEAR,
notice_preference CHAR(10) NOT NULL,
email_provided BOOL NOT NULL,
year_registered YEAR NOT NULL,
within_sf_county BOOL,

PRIMARY KEY (id),

CONSTRAINT fk_library
FOREIGN KEY (home_library)
REFERENCES LIBRARY(name),

CONSTRAINT fk_patrontype
FOREIGN KEY (patron_type)
REFERENCES PATRONTYPE(name)
);
"""
cursor.execute(createPatronTable)
print("Tables created!")

class Columns(Enum):
    PATRON_TYPE = 0
    TOTAL_CHECKOUTS = 1
    TOTAL_RENEWALS = 2
    AGE_RANGE = 3
    HOME_LIBRARY = 4
    ACTIVE_MONTH = 5
    ACTIVE_YEAR = 6
    NOTICE_PREFERENCE = 7
    PROVIDED_EMAIL = 8
    YEAR_REGISTERED = 9
    WITHIN_SF = 10
    
    
i = 0
with open("Library_Usage_20261025.csv", "r") as file:
    #read each row of the data
    file.readline()
    for line in file:
        #split into columns
        columns = line.split(",")
        
        #add patron type to PATRONTYPE table if not already in
        insertPatronType = "INSERT IGNORE INTO PATRONTYPE VALUES(" + columns[0] + ");"
        cursor.execute(insertPatronType)
        
        insertLibrary = "INSERT IGNORE INTO LIBRARY VALUES"
        
        
        i += 1
        if i > 10000:
            break
        



dataBase.close()