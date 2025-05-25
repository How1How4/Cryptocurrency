import mysql.connector
import requests
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import data_getnow as dgn
def add_history_price(x):
    dgn.update_price()
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"

    )
    cg = CoinGeckoAPI()
    cursor = db.cursor(buffered=True)
    coins = ['bitcoin', 'ethereum', 'solana']
    name=['BTC','ETH','SOL']
    print("start2")
    print(x)
    for i in range(3):
        data = cg.get_coin_market_chart_by_id(id=coins[i], vs_currency='usd', days=x)
        prices = data['prices']  # [[timestamp, price], ...]
        # 整理資料
        price_values = []
        for p in prices:
            t=p[0]
            t=datetime.fromtimestamp(p[0]/1000).strftime("%Y-%m-%d %H:%M")
            price=p[1]
            cursor.execute(
                "INSERT INTO price_history (currency_id, name, price, time) VALUES (%s, %s, %s ,%s)",
                (i+1 ,name[i], price , t)
            )
            db.commit()
            print("✅ 資料已成功存入 MySQL")
        print(name[i],"插入完成")
    cursor.close()
    db.close()
    

def add_history_priceDATE(x):
    print("up1")
    dgn.update_price()
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000" # 密碼
    )
    cg = CoinGeckoAPI()
    cursor = db.cursor(buffered=True)
    coins = ['bitcoin', 'ethereum', 'solana']
    name=['BTC','ETH','SOL']
    today = datetime.now()
    now=int(today.timestamp())
    for i in range(3):
        data = cg.get_coin_market_chart_range_by_id(id=coins[i], vs_currency='usd',from_timestamp=x, to_timestamp=now  )
        prices = data['prices']  # [[timestamp, price], ...]
        # 整理資料
        price_values = []
        for p in prices:
            t=p[0]
            t=datetime.fromtimestamp(p[0]/1000).strftime("%Y-%m-%d %H:%M")
            price=p[1]
            cursor.execute(
                "INSERT INTO cryptocurrency.price_history (currency_id, name, price, time) VALUES (%s, %s, %s ,%s)",
                (i+1 ,name[i], price , t)
            )
            db.commit()
            print("✅ 資料已成功存入 MySQL")
        print(name[i],"插入完成")
    cursor.close()
    db.close()





    


