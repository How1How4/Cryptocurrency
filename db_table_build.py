import mysql.connector

def dtbuild():
    mydb = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency" #資料庫名稱
    )

    mycursor = mydb.cursor()

    mycursor.execute("""
    CREATE TABLE `currency` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `price` float NOT NULL,
      `time` datetime NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """)

    mycursor.execute("""
    CREATE TABLE `price_history` (
      `id` int NOT NULL AUTO_INCREMENT,
      `currency_id` int NOT NULL,
      `name` varchar(50) NOT NULL,
      `price` float NOT NULL,
      `time` datetime NOT NULL,
      PRIMARY KEY (`id`),
      KEY `currency_id` (`currency_id`),
      CONSTRAINT `price_history_ibfk_1` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """)

    mycursor.execute("""
    CREATE TABLE `user` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `password` int NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """)

    mycursor.execute("""
    CREATE TABLE `position` (
      `id` int NOT NULL AUTO_INCREMENT,
      `currency_id` int NOT NULL,
      `price` float NOT NULL,
      `quantity` float NOT NULL,
      `total` float NOT NULL,
      `user` int NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """)



    mycursor.execute("""
    CREATE TABLE `transaction_history` (
      `id` int NOT NULL AUTO_INCREMENT,
      `currency_id` int NOT NULL,
      `price` float NOT NULL,
      `quantity` float NOT NULL,
      `total` float NOT NULL,
      `profitloss` float NOT NULL,
      `user` int NOT NULL,
      `time` datetime NOT NULL,
      PRIMARY KEY (`id`),
      KEY `currency_id` (`currency_id`),
      KEY `user` (`user`),
      CONSTRAINT `transaction_history_ibfk_1` FOREIGN KEY (`currency_id`) REFERENCES `currency` (`id`),
      CONSTRAINT `transaction_history_ibfk_2` FOREIGN KEY (`user`) REFERENCES `user` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
    """)




    print("table建立完成")





























































''' 同以下程式
CREATE TABLE currency (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(10) NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    time datetime NOT NULL
)
CREATE TABLE IF NOT EXISTS Price_History (
    id INT AUTO_INCREMENT PRIMARY KEY,
    currency_id INT NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    time DATETIME NOT NULL,
    FOREIGN KEY (currency_id) REFERENCES Currency(id)
)
'''

'''
CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    password INT NOT NULL
)

CREATE TABLE position (
    id INT AUTO_INCREMENT PRIMARY KEY,
    currency_id INT NOT NULL,
    price FLOAT NOT NULL,
    count FLOAT NOT NULL,
    name VARCHAR(50) NOT NULL
)

CREATE TABLE transaction_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    currency_id INT NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    count FLOAT NOT NULL,
    total FLOAT NOT NULL,
    user INT NOT NULL,transaction_history
    time DATETIME NOT NULL,
    FOREIGN KEY (currency_id) REFERENCES Currency(id),
    FOREIGN KEY (user) REFERENCES User(id)
)



'''
