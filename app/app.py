
import mysql.connector


connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "1738"
)
cursor = connection.cursor

print("****  SFILS DATABASE  ****")
print("")


#connection.commit()
connection.close()