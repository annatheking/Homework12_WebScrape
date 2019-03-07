from flask import Flask, render_template, redirect
import scrape_mars
from flask_pymongo import PyMongo

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.mars_db

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route('/')
def index():
    mars_dictionary = mongo.db.mars.find_one()
    return render_template("index.html", dict=mars_dictionary)

# Set route
@app.route('/scrape')
def scrape():
    # Drops collection if available to remove duplicates
    db.mars.drop()

    # Creates a collection in the database and inserts two documents
    # Return the template with the teams list passed in
    db.mars.insert(scrape_mars.scrape())
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run(debug=True)
