from flask import Flask, render_template, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB connection setup (replace <connection_string> with actual string)
client = MongoClient("<your_mongodb_connection_string>")
db = client['commodity_prices']  # Database name
collection = db['crops']         # Collection storing crop data

@app.route('/')
def index():
    # This route renders the main portal (index.html)
    return render_template('index.html')

@app.route('/api/get_crop_data')
def get_crop_data():
    # This route fetches crop data from MongoDB and returns it as JSON for the chart
    crop_data = list(collection.find({}, {"_id": 0, "date": 1, "price": 1}).limit(30))
    return jsonify(crop_data)

if __name__ == "__main__":
    app.run(debug=True)
