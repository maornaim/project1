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
        stock["changes"] = calculate_changes_for_stock(stock["monthly_prices"])

    return render_template('index.html', stocks=stocks)

@app.route('/add_stock', methods=['POST'])
def add_stock():
    try:
        stock_name = request.form.get("name")
        monthly_prices = [int(price) for price in request.form.get("monthly_prices").split(',')]

        if not stock_name or len(monthly_prices) < 3:
            return jsonify({"error": "Invalid input. Name and at least 3 monthly prices are required."}), 400

        stock_id = collection.insert_one({
            "name": stock_name,
            "monthly_prices": monthly_prices
        }).inserted_id

        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calculate_changes/<stock_id>', methods=['GET'])
def calculate_changes(stock_id):
    stock = collection.find_one({"_id": ObjectId(stock_id)})

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
            s["changes"] = None

    return render_template('index.html', stocks=stocks)

def calculate_changes_for_stock(monthly_prices):
    changes = []
    for i in range(1, len(monthly_prices)):
        change = monthly_prices[i] - monthly_prices[i - 1]
        percentage_change = (change / monthly_prices[i - 1]) * 100
        changes.append({
            "month": i,
            "change": change,
            "percentage_change": percentage_change
        })
    return changes

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)
