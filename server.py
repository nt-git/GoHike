"""Hiking Trails"""


from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Trail, connect_to_db, db

import geocoder
import requests
import os


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

hiking_consumer_key = os.environ['HIKING_CONSUMER_KEY']


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/SignIn', methods=["GET"])
def sign_in():
    """Login page."""
    return render_template("login_form.html")


@app.route("/SignIn", methods=["POST"])
def user_sign_in():
    """ Validate User Login """

    email = request.form.get("email")
    password = request.form.get("password")
    query_user = User.query.filter_by(email=email).first()

    if not query_user:
        flash("That email isn't in our system.  It looks like you need to sign up!")
        return redirect("/sign-up")

    if query_user.password != password:
        flash("Incorrect password, please try signing in again")
        return redirect("/SignIn")
    else:
        session['id'] = query_user.user_id
        flash("Login successful!")
        return redirect("/user")


@app.route('/SignUp', methods=["GET"])
def sign_up():
    """Sign Up page"""
    return render_template("signup_form.html")


@app.route("/SignUp", methods=["POST"])
def user_sign_up():
    """ Get User's email and password and adds user to the DB"""

    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    zipcode = request.form.get("zip")
    query = db.session.query('User')
    users_emails = query.filter(User.email == email).all()

    if users_emails:
        flash("User already exists!")
        return redirect('/sign-up')
    else:
        new_user = User(email=email, password=password, zipcode=zipcode, name=name)
        db.session.add(new_user)
        db.session.commit()

        flash("Registered successfully!")
        return redirect('/user')


@app.route("/users/<u_id>")
def user_profile(u_id):
    """Shows details about a specific user."""

    user = User.query.options(db.joinedload('usertrails','trail')).get(u_id)

    return render_template("user_detail.html", user=user)


@app.route("/search", methods=["GET"])
def search_trails():
    """Search form"""
    return render_template("search_form.html")


@app.route("/search", methods=["POST"])
def user_search_trails():
    """Display search results"""

    zipcode = request.form.get("zipcode")
    g = geocoder.google(str(zipcode))
    url_lat = str(g.lat)
    url_lng = str(g.lng)

    url_maxDistance = request.form.get("trail_num")
    print url_maxDistance
    #send request with above lat and long
    r = requests.get("https://www.hikingproject.com/data/get-trails?lat="+url_lat+"&lon="+url_lng+"&maxDistance="+url_maxDistance+"&key="+hiking_consumer_key)
    trail = r.json()
    print trail
    num_results = trail['trails']
    number = len(num_results)
    #print num_results

    return render_template("search_results.html", dict=trail, num_results=num_results, number=number)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    app.run(port=5000, host='0.0.0.0')
