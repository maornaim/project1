from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# התחבר למסד הנתונים MongoDB
client = MongoClient("mongodb://mongo:27017/")
db = client.add_db
collection = db.add

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add():
    num1 = request.form['num1']
    num2 = request.form['num2']
    result = int(num1) + int(num2)
    
    # שמירת התרגיל והתוצאה במסד הנתונים MongoDB
    exercise = {
        "num1": num1,
        "num2": num2,
        "result": result
    }
    collection.insert_one(exercise)
    
    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
