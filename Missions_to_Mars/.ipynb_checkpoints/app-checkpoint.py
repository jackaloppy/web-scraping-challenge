from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
client = PyMongo(app, uri="mongodb://localhost:27017/")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = client.mars_db.scrape_data.find_one()
    
    # Return template and data
    return render_template("index.html", mars_data=mars_data)