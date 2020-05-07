# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs.

from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# create route that renders index.html template using data from Mongo
@app.route('/')
def index():
    # Find a data point from mars collection and save in mars variable
    mars_info = mongo.db.mars.find_one()
     # Return template and data (mars_info- in index.html)
    return render_template("index.html", mars=mars_info)


# define route to trigger scrape function
@app.route("/scrape")
def scrape(mars):
    #collection is called mars
    mars = mongo.mars_app.mars

    #create variable to hold data form scrape_mars.py with scrape_sites function applied 
    mars_data = scrape_mars.scrape_sites()
    #update db with dictionary holding the mars_data
    mars.update(
        {}, 
        mars_data, 
        upsert=True)
    
    # Redirect to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)