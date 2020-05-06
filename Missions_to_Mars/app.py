# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs.

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_craigslist

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")

# define route for scrape to import scrape_mars.py
@app.route("scrape/")
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_sites()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)