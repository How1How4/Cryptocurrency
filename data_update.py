import mysql.connector
import requests
from pycoingecko import CoinGeckoAPI
from datetime import datetime
import data_gethistory as dgh
def upload():
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '0000',
        'database': 'cryptocurrency'
    }
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    currency_id =1
    q=1
    query = "SELECT time FROM currency  ORDER BY time ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    data = [{ 'time': row['time']} for row in rows]
    last=data[0]['time']
    cursor.close()
    conn.close()
    now=datetime.now()
    times=now-last
    if(times.days>=1 or times.seconds>43200):
        ltime=int(last.timestamp())
        dgh.add_history_priceDATE(ltime)
        #ltime=times.days+(times.seconds)/86400
        #print(ltime)
        #dgh.add_history_price(ltime)

