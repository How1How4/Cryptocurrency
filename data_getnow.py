import mysql.connector
import requests
from pycoingecko import CoinGeckoAPI
from datetime import datetime

def update_price():
    print("up2")
    cg = CoinGeckoAPI()
    # 建立連線
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"
    )
    cursor = db.cursor(buffered=True)
    coins = ['bitcoin', 'ethereum', 'solana']
    name=['BTC','ETH','SOL']
    i=0
    # === 3. 抓資料 + 插入 Currency 與 Price_History ===
    for coin_id in coins:
        # 抓該幣種的市價
        coin_data = cg.get_price(ids=coin_id, vs_currencies='usd')
        price = coin_data[coin_id]['usd']
        time=datetime.now()
        time=time.strftime('%Y-%m-%d %H:%M')
        cursor.execute(
            "SELECT price, time FROM currency WHERE id = %s ",(i+1,)
        )
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(1)
            cursor.execute(
                "INSERT INTO currency (name, price, time) VALUES (%s, %s ,%s)",
                (name[i], price , time)
            )
        else:
            cursor.execute(
                "UPDATE currency SET price=%s,time=%s WHERE (name=%s)" ,
                (price,time,name[i])
            )
        i=i+1
        print("✅ 資料已成功存入 MySQL")
        db.commit()
    cursor.close()
    db.close()


