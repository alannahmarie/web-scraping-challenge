from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape 

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Set up root route
@app.route("/")
def index():
    mars = mongo.db.mars_info.find_one()
    return render_template("index.html", info = mars)

@app.route("/scrape")
def scraper():
    mars_data = scrape.scrape()
    mongo.db.mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)
    

if __name__ == "__main__":
    app.run(debug=True)