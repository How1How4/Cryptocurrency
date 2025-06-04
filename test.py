<<<<<<< HEAD
import datetime
from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
import data_update as du
app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'cryptocurrency'
}

@app.route("/")
def index():
    return render_template("test.html") 

@app.route("/position")
def index1():
    return render_template("position.html") 

@app.route("/transaction")
def index2():
    return render_template("transaction.html") 

@app.route("/login")
def login():
    return render_template("login.html") 

@app.route('/api/price')
def get_price():
    du.upload()
    currency_id = request.args.get('id', default=1, type=int)
    day= request.args.get('range', default=1, type=int)
    today = datetime.datetime.now()
    rday = today - datetime.timedelta(days=day)
    today=today.strftime('%Y-%m-%d %H:%M')
    rday=rday.strftime('%Y-%m-%d %H:%M')
    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor(dictionary=True)

#    query = "SELECT price, time FROM Price_History WHERE currency_id = %s ORDER BY time ASC"
    query = "SELECT price, time FROM Price_History WHERE currency_id = %s AND time BETWEEN %s AND %s ORDER BY time ASC"
    
#    cursor.execute(query, (currency_id,))
    cursor.execute(query, (currency_id,rday,today))
    rows = cursor.fetchall()
    data = [{'timestamp': row['time'], 'price': float(row['price'])} for row in rows]

    cursor.close()
    conn.close()

    return jsonify(data)



@app.route('/api/transaction', methods=["POST"])
def trade():
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"

    )

    data = request.get_json()
    currency_id = data.get('id', 1)
    price = data.get('price', 100.0)
    print(price)
    quantity = data.get('quantity', 0.0)
    trade_type = data.get('trade', 1)
    user=data.get('user',"")

    cursor = db.cursor(buffered=True)

    time = datetime.datetime.now()
    time=time.strftime('%Y-%m-%d %H:%M')
    trade_log = f"交易紀錄: 幣種ID={currency_id}, 價格={price}, 數量={quantity}, 類型={'買進' if trade_type > 0 else '賣出'}"
    print(trade_log)
    
    if trade_type==1:
        val="SELECT quantity , price FROM position WHERE currency_id = %s  AND user=%s"
        cursor.execute(val,(currency_id,user))
        rows = cursor.fetchall()
        if len(rows)==0:
            val2="INSERT INTO position (currency_id, price , quantity ,total , user) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(val2,(currency_id,price,quantity,price*quantity,user))
        else:
            
            x=rows[0][0]
            y=rows[0][1]
            pricea=(x*y+quantity*price)/(x+quantity)
            val2="UPDATE position SET quantity=%s ,price=%s ,total=%s WHERE (currency_id=%s AND user=%s)"
            cursor.execute(val2,(x+quantity,pricea,(x+quantity)*pricea,currency_id,user))
        #val3="INSERT INTO transaction_history (currency_id, price , quantity , total ,  user , time) VALUES (%s,%s,%s,%s,%s,%s)"
        val3="INSERT INTO transaction_history (currency_id, price , quantity , total , profitloss ,  user , time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        #cursor.execute(val3,(currency_id,price,quantity,price*quantity,user,time))
        cursor.execute(val3,(currency_id,price,quantity,price*quantity, 0 ,user,time))
        db.commit()
        print(trade_log)



    if trade_type==-1:
        val="SELECT quantity , price FROM position WHERE currency_id = %s AND user =%s"
        cursor.execute(val,(currency_id,user))
        rows = cursor.fetchall()
        if len(rows)==0 or rows[0][0]<quantity:
            return jsonify({
                "message": "交易失敗 持有量不足！",
                "log": ""
            }), 400
        else:
            x=rows[0][0]
            profitloss=(price-rows[0][1])*quantity
            if x-quantity==0:
                
                val2="DELETE FROM position WHERE (currency_id=%s AND user=%s)"
                cursor.execute(val2,(currency_id,user))
            else:
                val2="UPDATE position SET quantity=%s ,total=%s WHERE (currency_id=%s AND user=%s)"
                cursor.execute(val2,(x-quantity,(x-quantity)*rows[0][1],currency_id,user))
        #val3="INSERT INTO transaction_history (currency_id, price , quantity , total ,  user , time) VALUES (%s,%s,%s,%s,%s,%s)"
        val3="INSERT INTO transaction_history (currency_id, price , quantity , total , profitloss, user , time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        #cursor.execute(val3,(currency_id,price,quantity*-1,price*quantity,user,time))
        cursor.execute(val3,(currency_id,price,quantity*-1,price*quantity,profitloss,user,time))
        db.commit()
        print(trade_log)


    return jsonify({
        "message": "交易成功！",
        "log": trade_log
    }), 200

@app.route('/api/login', methods=["POST"])
def LOGIN():
    print("ok")
    data = request.get_json()
    user = data.get('user', 1)
    password = data.get('password', 1.0)
    logintype = data.get('logintype', 1)
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"
    )
    cursor = db.cursor(buffered=True)
    val="SELECT name , password , id FROM user WHERE name = %s "
    cursor.execute(val,(user,))
    rows = cursor.fetchall()
    if logintype==1:
        cursor.close()
        db.close()
        if len(rows)==0:
            return jsonify({
                "message": "未註冊！"
            }), 400
        else:
            print()
            if str(rows[0][1])==password:
                return jsonify({
                    "message": "登入成功！",
                    "userid":rows[0][2]
                }), 200
            else:
                return jsonify({
                    "message": "密碼錯誤！"
                }), 400
    else:
        if len(rows)==0:
            val="INSERT INTO user ( name , password) VALUES (%s,%s)"
            cursor.execute(val,(user,password))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({
                "message": "新增成功,請重新登入！"
            }), 200
        else:
            return jsonify({
                "message": "使用者重複！"
            }), 400

@app.route('/api/position', methods=["POST"])
def SEARCHPOSITION():
    currency=['BTC','ETH','SOL']
    data = request.get_json()
    user = data.get('user', 1)
    id = data.get('id', 1.0)
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"
    )
    cursor = db.cursor(buffered=True)
    val="SELECT price , quantity , total FROM position WHERE user = %s AND currency_id = %s"
    cursor.execute(val,(user,id))
    rows = cursor.fetchall()
    
    if len(rows)==0:
        return jsonify({
            "message": "無持有該幣種！"
        }), 400
    else:
        return jsonify({
            "message": "查詢成功！",
            "currency":currency[int(id)-1],
            "price":rows[0][0],
            "quantity":rows[0][1],
            "total":rows[0][2]
        }), 200

@app.route('/api/search', methods=["POST"])
def SEARCH():
    currency=['BTC','ETH','SOL']
    Ttype=['買入','賣出']
    data = request.get_json()
    user = data.get('user', 1)
    id = data.get('id', 1.0)
    day = data.get('time', 1.0)
    print(data)
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"
    )
    cursor = db.cursor(buffered=True)
    now = datetime.datetime.now()
    delta=datetime.timedelta(days=int(day))
    time=now-delta
    now=now.strftime('%Y-%m-%d %H:%M')
    time=time.strftime('%Y-%m-%d %H:%M')
    #val="SELECT price , quantity , total FROM transaction_history WHERE user = %s AND currency_id = %s AND time BETWEEN %s AND %s"
    val="SELECT price , quantity , total ,profitloss FROM transaction_history WHERE user = %s AND currency_id = %s AND time BETWEEN %s AND %s"
    cursor.execute(val,(user,id,time,now))
    rows = cursor.fetchall()
    result=[]
    for i in rows:
        if float(i[1])>0:
            tt=0
            x=i[1]
        else:
            tt=1
            x=-i[1]
        #result.append({"currency": currency[int(id)-1],"price":i[0], "quantity": x, "total": i[2],"type":Ttype[tt]})
        result.append({"currency": currency[int(id)-1],"price":i[0], "quantity": x, "total": i[2],"type":Ttype[tt],"profitloss":i[3]})
    print(result)
    if len(rows)==0:
        return jsonify({
            "message": "無持有該幣種！"
        }), 400
    else:
        return jsonify({
            "message": "查詢成功！",
            "data":result
        }), 200
if __name__ == '__main__':
    app.run(debug=True)
=======
import datetime
from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_cors import CORS
import data_update as du
app = Flask(__name__)
CORS(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'database': 'cryptocurrency'
}

@app.route("/")
def index():
    return render_template("test.html") 

@app.route("/position")
def index1():
    return render_template("position.html") 

@app.route("/transaction")
def index2():
    return render_template("transaction.html") 

@app.route("/login")
def login():
    return render_template("login.html") 

@app.route('/api/price')
def get_price():
    du.upload()
    currency_id = request.args.get('id', default=1, type=int)
    day= request.args.get('range', default=1, type=int)
    today = datetime.datetime.now()
    rday = today - datetime.timedelta(days=day)
    today=today.strftime('%Y-%m-%d %H:%M')
    rday=rday.strftime('%Y-%m-%d %H:%M')
    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor(dictionary=True)

#    query = "SELECT price, time FROM Price_History WHERE currency_id = %s ORDER BY time ASC"
    query = "SELECT price, time FROM Price_History WHERE currency_id = %s AND time BETWEEN %s AND %s ORDER BY time ASC"
    
#    cursor.execute(query, (currency_id,))
    cursor.execute(query, (currency_id,rday,today))
    rows = cursor.fetchall()
    data = [{'timestamp': row['time'], 'price': float(row['price'])} for row in rows]

    cursor.close()
    conn.close()

    return jsonify(data)



@app.route('/api/transaction', methods=["POST"])
def trade():
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"

    )

    data = request.get_json()
    currency_id = data.get('id', 1)
    price = data.get('price', 100.0)
    print(price)
    quantity = data.get('quantity', 0.0)
    trade_type = data.get('trade', 1)
    user=data.get('user',"")

    cursor = db.cursor(buffered=True)

    time = datetime.datetime.now()
    time=time.strftime('%Y-%m-%d %H:%M')
    trade_log = f"交易紀錄: 幣種ID={currency_id}, 價格={price}, 數量={quantity}, 類型={'買進' if trade_type > 0 else '賣出'}"
    print(trade_log)
    
    if trade_type==1:
        val="SELECT quantity , price FROM position WHERE currency_id = %s  AND user=%s"
        cursor.execute(val,(currency_id,user))
        rows = cursor.fetchall()
        if len(rows)==0:
            val2="INSERT INTO position (currency_id, price , quantity ,total , user) VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(val2,(currency_id,price,quantity,price*quantity,user))
        else:
            
            x=rows[0][0]
            y=rows[0][1]
            pricea=(x*y+quantity*price)/(x+quantity)
            val2="UPDATE position SET quantity=%s ,price=%s ,total=%s WHERE (currency_id=%s AND user=%s)"
            cursor.execute(val2,(x+quantity,pricea,(x+quantity)*pricea,currency_id,user))
        #val3="INSERT INTO transaction_history (currency_id, price , quantity , total ,  user , time) VALUES (%s,%s,%s,%s,%s,%s)"
        val3="INSERT INTO transaction_history (currency_id, price , quantity , total , profitloss ,  user , time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        #cursor.execute(val3,(currency_id,price,quantity,price*quantity,user,time))
        cursor.execute(val3,(currency_id,price,quantity,price*quantity, 0 ,user,time))
        db.commit()
        print(trade_log)



    if trade_type==-1:
        val="SELECT quantity , price FROM position WHERE currency_id = %s AND user =%s"
        cursor.execute(val,(currency_id,user))
        rows = cursor.fetchall()
        if len(rows)==0 or rows[0][0]<quantity:
            return jsonify({
                "message": "交易失敗 持有量不足！",
                "log": ""
            }), 400
        else:
            x=rows[0][0]
            profitloss=(price-rows[0][1])*quantity
            if x-quantity==0:
                
                val2="DELETE FROM position WHERE (currency_id=%s AND user=%s)"
                cursor.execute(val2,(currency_id,user))
            else:
                val2="UPDATE position SET quantity=%s ,total=%s WHERE (currency_id=%s AND user=%s)"
                cursor.execute(val2,(x-quantity,(x-quantity)*rows[0][1],currency_id,user))
        #val3="INSERT INTO transaction_history (currency_id, price , quantity , total ,  user , time) VALUES (%s,%s,%s,%s,%s,%s)"
        val3="INSERT INTO transaction_history (currency_id, price , quantity , total , profitloss, user , time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        #cursor.execute(val3,(currency_id,price,quantity*-1,price*quantity,user,time))
        cursor.execute(val3,(currency_id,price,quantity*-1,price*quantity,profitloss,user,time))
        db.commit()
        print(trade_log)


    return jsonify({
        "message": "交易成功！",
        "log": trade_log
    }), 200

@app.route('/api/login', methods=["POST"])
def LOGIN():
    print("ok")
    data = request.get_json()
    user = data.get('user', 1)
    password = data.get('password', 1.0)
    logintype = data.get('logintype', 1)
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"
    )
    cursor = db.cursor(buffered=True)
    val="SELECT name , password , id FROM user WHERE name = %s "
    cursor.execute(val,(user,))
    rows = cursor.fetchall()
    if logintype==1:
        cursor.close()
        db.close()
        if len(rows)==0:
            return jsonify({
                "message": "未註冊！"
            }), 400
        else:
            print()
            if str(rows[0][1])==password:
                return jsonify({
                    "message": "登入成功！",
                    "userid":rows[0][2]
                }), 200
            else:
                return jsonify({
                    "message": "密碼錯誤！"
                }), 400
    else:
        if len(rows)==0:
            val="INSERT INTO user ( name , password) VALUES (%s,%s)"
            cursor.execute(val,(user,password))
            db.commit()
            cursor.close()
            db.close()
            return jsonify({
                "message": "新增成功,請重新登入！"
            }), 200
        else:
            return jsonify({
                "message": "使用者重複！"
            }), 400

@app.route('/api/position', methods=["POST"])
def SEARCHPOSITION():
    currency=['BTC','ETH','SOL']
    data = request.get_json()
    user = data.get('user', 1)
    id = data.get('id', 1.0)
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"
    )
    cursor = db.cursor(buffered=True)
    val="SELECT price , quantity , total FROM position WHERE user = %s AND currency_id = %s"
    cursor.execute(val,(user,id))
    rows = cursor.fetchall()
    
    if len(rows)==0:
        return jsonify({
            "message": "無持有該幣種！"
        }), 400
    else:
        return jsonify({
            "message": "查詢成功！",
            "currency":currency[int(id)-1],
            "price":rows[0][0],
            "quantity":rows[0][1],
            "total":rows[0][2]
        }), 200

@app.route('/api/search', methods=["POST"])
def SEARCH():
    currency=['BTC','ETH','SOL']
    Ttype=['買入','賣出']
    data = request.get_json()
    user = data.get('user', 1)
    id = data.get('id', 1.0)
    day = data.get('time', 1.0)
    print(data)
    db = mysql.connector.connect(
        host="localhost",       # 主機名稱
        user="root",            # 使用者名稱
        password="0000", # 密碼
        database="cryptocurrency"
    )
    cursor = db.cursor(buffered=True)
    now = datetime.datetime.now()
    delta=datetime.timedelta(days=int(day))
    time=now-delta
    now=now.strftime('%Y-%m-%d %H:%M')
    time=time.strftime('%Y-%m-%d %H:%M')
    #val="SELECT price , quantity , total FROM transaction_history WHERE user = %s AND currency_id = %s AND time BETWEEN %s AND %s"
    val="SELECT price , quantity , total ,profitloss FROM transaction_history WHERE user = %s AND currency_id = %s AND time BETWEEN %s AND %s"
    cursor.execute(val,(user,id,time,now))
    rows = cursor.fetchall()
    result=[]
    for i in rows:
        if float(i[1])>0:
            tt=0
            x=i[1]
        else:
            tt=1
            x=-i[1]
        #result.append({"currency": currency[int(id)-1],"price":i[0], "quantity": x, "total": i[2],"type":Ttype[tt]})
        result.append({"currency": currency[int(id)-1],"price":i[0], "quantity": x, "total": i[2],"type":Ttype[tt],"profitloss":i[3]})
    print(result)
    if len(rows)==0:
        return jsonify({
            "message": "無持有該幣種！"
        }), 400
    else:
        return jsonify({
            "message": "查詢成功！",
            "data":result
        }), 200
if __name__ == '__main__':
    app.run(debug=True)
>>>>>>> 70f05f803971e82a15c9e4159a3e59b4e65c5657
