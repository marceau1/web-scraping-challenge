# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     custom_cell_magics: kql
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.2
#   kernelspec:
#     display_name: pythondata
#     language: python
#     name: python3
# ---

from flask import Flask, render_template, redirect, url_for
# import pymango library
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)
# mongo = PyMongo(app, url="mongodb://localhost:27017/mars_db")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    mars_data_info= mongo.db.mars_db.find_one()

    return render_template("index.html", mars=mars_data_info)
# return render_template("index.html", mars=mars_collect)

@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data= scrape_mars.scrape_info()

# %%
# Update the Mongo database using update and upsert=True
    mongo.db.mars_db.update_one({}, {"$set": mars_data}, upsert=True)


# %%
# Redirect back to home page
    return redirect("/")


# %%
if __name__ == '__main__':
    app.run(debug=True)

