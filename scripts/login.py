import mysql.connector

def getConnection():
    connection = mysql.connector.connect(
        host = "localhost",
        user = "phen",
        passwd = "0618"
    )
    return connection
