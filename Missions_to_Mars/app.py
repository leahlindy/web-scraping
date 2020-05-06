# Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs.

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create route that renders index.html template
@app.route("/")
def index():
    # Find a data point from mars collection and save in mars variable
    mars = mongo.db.mars.find_one()
     # Return template and data (mars- in index.html)
    return render_template("index.html", mars=mars)


# define route for scrape to import scrape_mars.py
@app.route("/scrape")
def scraper():
    #db is called mars
    mars = mongo.db.mars

    #create variable to hold data form scrape_mars.py with scrape_sites function applied 
    mars_data = scrape_mars.scrape_sites()
    #update db with dictionary holding the mars_data
    mars.update(
        {}, 
        mars_data, 
        upsert=True)
    
    # Redirect to home page
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)