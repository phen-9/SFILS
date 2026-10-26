import mysql.connector
import csv

dataBase = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "1738"
)

cursor = dataBase.cursor()

#create and use SFILS database
cursor.execute("DROP DATABASE SFILS")
cursor.execute("CREATE DATABASE IF NOT EXISTS SFILS")
cursor.execute("USE SFILS")

createPatronTable = """
CREATE TABLE PATRON (
id INT NOT NULL AUTO_INCREMENT,
patron_type CHAR(15) NOT NULL,
total_checkouts INT NOT NULL,
total_renewals INT NOT NULL,
age_range VARCHAR(15) NOT NULL,
home_library VARCHAR(20) NOT NULL,
circulation_active_month CHAR(3),
circulation_active_year YEAR,
notice_preference CHAR(10) NOT NULL,
email_provided BOOL NOT NULL,
year_registered YEAR NOT NULL,
within_sf_county BOOL,

PRIMARY KEY (id)
);
"""
cursor.execute(createPatronTable)


file = open("Library_Usage_20261025.csv", "r")

    


dataBase.close()