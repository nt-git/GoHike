"""Hiking Trails"""

import requests
from pprint import pprint
import json

from model import User, Trail, UserTrails, connect_to_db, db

#r = requests.get("https://www.hikingproject.com/data/get-trails?lat=37.3382&lon=-121.8863&maxDistance=10&key=200214091-fba4863b8895606501a2dbecc5aea6b9")
#r1 = requests.get("https://www.hikingproject.com/data/get-conditions?ids=7000108,7002175,7005207,7001726,7005428&key=20021")
#trail  = r1.json()
#pprint(trail)

def add_user():
    """ Add a user to db"""

    name ="Nirav"
    email = "test@hb.com"
    password = "123456"
    zipcode = "94702"

    new_user = User(name=name, email=email, password=password, zipcode=zipcode)
    db.session.add(new_user)
    db.session.commit()


#Get Trail Data by making a call to API and add one Trail to DB from the returned data

def find_and_add_trail():
    """Get Trail Data by making a call to API and add one Trail to Trail Table -  from the returned data"""

    r = requests.get("https://www.hikingproject.com/data/get-trails?lat=37.3382&lon=-121.8863&maxDistance=10&key=200214091-fba4863b8895606501a2dbecc5aea6b9")
    trail = r.json()

    num_results = trail['trails']

    url = num_results[2]['url']
    name = num_results[2]['name']
    trail_id = 7024835

    new_trail = Trail(trail_id=trail_id, name=name, url=url)
    db.session.add(new_trail)
    db.session.commit()


def add_user_trail():
    """ Just a place holder usertrail entry to test out /user page """
    trail_id = 7024835
    user_id = 1
    rating = 5

    new_user_trail = UserTrails(trail_id=trail_id, user_id=user_id, rating=rating)
    db.session.add(new_user_trail)
    db.session.commit()




if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app)
    print "Connected to DB."
