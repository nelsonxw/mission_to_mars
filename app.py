# import dependencies
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

# set up Flask
app = Flask(__name__)

# connect to Pymongo
mongo = PyMongo(app)

# define routes
@app.route("/")
def index():
    # read scraped data from mongo database 
    scraped_data = mongo.db.data.find_one()
    # render template to index html and pass scraped data
    return render_template("index.html", render_data=scraped_data)


@app.route("/scrape")
def scrape():
    # create mongo database and data collection
    collection = mongo.db.data
    # scrape data and save to variables then update to mongo database
    mars_data = scrape_mars.scrape()
    collection.update(
        {},
        mars_data,
        upsert=True
    )
    # return to index page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)