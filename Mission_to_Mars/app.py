from flask import Flask, render_template, redirect
from numpy import record
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__) 

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    # Find one record of data from the mongo database
    record = mongo.db.mars_list.find_one()
    
    # Return template and data
    return render_template("index.html", mars = record)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_dict = scrape_mars.scrape_web()

    # Update the Mongo database using update and upsert=True
    mongo.db.mars_list.update({}, mars_dict, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
  