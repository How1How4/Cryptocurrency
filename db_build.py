<<<<<<< HEAD
import mysql.connector
def dbuild():
    mydb = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000" # 密碼
    )

    mycursor = mydb.cursor()

    # 建立資料庫
    mycursor.execute("CREATE DATABASE cryptocurrency") #資料庫建立完成
    print("db建立完成")
=======
import mysql.connector
def dbuild():
    mydb = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000" # 密碼
    )

    mycursor = mydb.cursor()

    # 建立資料庫
    mycursor.execute("CREATE DATABASE cryptocurrency") #資料庫建立完成
    print("db建立完成")
>>>>>>> 70f05f803971e82a15c9e4159a3e59b4e65c5657
