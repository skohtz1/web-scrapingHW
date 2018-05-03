from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app)


@app.route("/")
def index():
    listings = mongo.db.listings_mars.find()
    return render_template("index.html", listings=listings)


@app.route("/clear")
def clear_listings():
   # mongo.db.listings_mars.drop()
    return redirect("http://127.0.0.1:5000/", code=302)


@app.route("/scrape")
def scrape():
    listings = mongo.db.listings_mars
    mars_data_dict = scrape_mars.scrape()
  #  for listing in mars_data_dict:
   #     listings.update({'weather':listing['weather'], 'hemisphere':listing['hemisphere'],'feature_image':listing['feature_image'],'title_feature':listing['title_feature']}, listing, upsert=True)
    listings.insert_one(mars_data_dict)
    return redirect("http://127.0.0.1:5000/", code=302)




if __name__ == "__main__":
    app.run(debug=True)