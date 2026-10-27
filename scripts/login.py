import mysql.connector

def getConnection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "root",
        passwd = "1738"
    )
    return connection
