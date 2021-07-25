# MongoDB and Flask Application
# let s set our dependencies 
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

# let's set Flask
app = Flask(__name__)

# Let's set PyMongo Connection 
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# let's set Flask Routes

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Import scraper_mars.py Script 
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

# Define Main Behavior
if __name__ == "__main__":
    app.run()