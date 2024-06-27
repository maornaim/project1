from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient("mongodb://mongo:27017/")
db = client.prodb
collection = db.stok

@app.route('/')
def index():
    stocks = list(collection.find())
    for stock in stocks:
        stock["_id"] = str(stock["_id"])
        stock["changes"] = calculate_changes_for_stock(stock["monthly_prices"]) #פמעיל את פונקציה לכל מניה 

    return render_template('index.html', stocks=stocks) 

@app.route('/add_stock', methods=['POST'])
def add_stock():   #מוסיף את ממניה לדטא בייס
    try:
        stock_name = request.form.get("name")
        monthly_prices = [int(price) for price in request.form.get("monthly_prices").split(',')]

        if not stock_name or len(monthly_prices) < 3: #בודק שיש שם ו3 חודשים למניה
            return jsonify({"error": "Invalid input. Name and at least 3 monthly prices are required."}), 400 #מספר הארור

        stock_id = collection.insert_one({ #מוסיף את המניה לשטא בייס
            "name": stock_name,
            "monthly_prices": monthly_prices
        }).inserted_id #מוסיף ID למניה 

        return redirect(url_for('index')) #נעדכן לדף הראשי
    except Exception as e:
        return jsonify({"error": str(e)}), 500   # מראה התראה שיש תקלה וממשיך את האפליקציה (לשים לב שיש טריי לפני )

@app.route('/calculate_changes/<stock_id>', methods=['GET'])
def calculate_changes(stock_id):
    stock = collection.find_one({"_id": ObjectId(stock_id)})# מחפש את המניה על ידי האיי דיי

    if not stock:
        return jsonify({"error": "Stock not found"}), 404

    monthly_prices = stock['monthly_prices']
    changes = calculate_changes_for_stock(monthly_prices)

    stocks = list(collection.find())
    for s in stocks:
        s["_id"] = str(s["_id"])
        if s["_id"] == stock_id:
            s["changes"] = changes
        else:
            s["changes"] = None   #לעובר על כל ה איי דייז שיש בדטא בייס ומראה את השינויים באתר

    return render_template('index.html', stocks=stocks) #מדפיס את זה באתר

def calculate_changes_for_stock(monthly_prices):
    changes = []
    for i in range(1, len(monthly_prices)):  #מעלים אותו האחד כדי שנוכל להעשות את ה אי ופחות אחד שלפניו
        change = monthly_prices[i] - monthly_prices[i - 1]
        percentage_change = (change / monthly_prices[i - 1]) * 100 #לוקח את השינוי הכספי מחלק בחודש שלו ומכפיל ב100 
        changes.append({
            "month": i,
            "change": change,
            "percentage_change": percentage_change
        })
    return changes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
