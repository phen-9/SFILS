
import mysql.connector

def print_entry(entry : str):
    print(entry)
    #implement later
    
connection = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "1738"
)
cursor = connection.cursor()
cursor.execute("USE SFILS")



while True:
    print("****  SFILS DATABASE  ****")
    print("Options:")
    print("1: Query Data")
    print("2: Add Data")
    print("3: Exit")

    option : str = ""
    num: int = 0
    while True:
        option = input()
        if option.isdigit():
            num = int(option)
            if num >= 1 and num <= 3:
                break
        print("INVALID INPUT")

    match num:
        case 1:
            #query in id range
            print("enter range to view:")
            print("first index:")
            startIndex = 0
            while True:
                option = input()
                if option.isdigit():
                    startIndex = int(option)
                    if startIndex >= 1 and startIndex <= 437116:
                        break
                print("INVALID INPUT")
            endIndex = 0
            while True:
                option = input()
                if option.isdigit():
                    endIndex = int(option)
                    if endIndex >= startIndex and endIndex <= 437116:
                        break
                print("INVALID INPUT")
            range = (startIndex, endIndex)
            cursor.execute("SELECT * FROM PATRON WHERE id BETWEEN %s AND %s" % range)
            for line in cursor.fetchall():
                print_entry(str(line))
            pass
        case 2:
            #insert
            pass
        case 3:
            #exit
            break




#connection.commit()
connection.close()