"""Models and database functions for Hiking Trail  project."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

# Here's where we create the idea of our database. We're getting this through
# the Flask-SQLAlchemy library. On db, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


class User(db.Model):
    """User model."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(50), nullable=False)

    friends = db.relationship("User",
                              secondary="friendships",
                              primaryjoin="User.user_id==Friendship.user1_id",
                              secondaryjoin="User.user_id==Friendship.user2_id")

    def __repr__(self):
        """Provide helpful representation about a user when printed."""

        return "<User user_id={} email={}>".format(self.user_id,
                                                   self.email)


class Trail(db.Model):
    """Trail model."""

    __tablename__ = "trails"

    trail_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    #condition = db.Column(db.String(200), nullable=True)
    length = db.Column(db.Float, nullable=True)
    trail_type = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provide helpful representation about a Trail when printed."""

        return "<Trail trail_id={} name={}>".format(self.trail_id, self.name)


class UserTrail(db.Model):
    """UserTrail model."""

    __tablename__ = "usertrails"

    usertrail_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"), nullable=False)
    rating = db.Column(db.Float, nullable=True)

    user = db.relationship("User", backref=db.backref("usertrails", order_by=usertrail_id))
    trail = db.relationship("Trail", backref=db.backref("usertrails", order_by=usertrail_id))

    def __repr__(self):
        """Provide helpful representation about a UserTrail for User when printed."""

        return "<UserTrails user_trail_id={}  rating={}>".format(self.usertrail_id, self.rating)


class Hike(db.Model):
    """Hike Model."""

    __tablename__ = "hikes"

    hike_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    usertrail_id = db.Column(db.Integer, db.ForeignKey("usertrails.usertrail_id"), nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    comments = db.Column(db.String(500), nullable=True)
    u_rating = db.Column(db.Float, nullable=True)

    usertrail = db.relationship("UserTrail", backref=db.backref("hikes", order_by=hike_id))

    def __repr__(self):
        """Provide helpful representation about a hike when printed."""

        return "<Hikes hike_id={} comments={}>".format(self.hike_id, self.comments)


class Attr(db.Model):
    """ Attr Model. """

    __tablename__ = "attrs"

    attr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        """Provide helpful representation about an attr for a trail when printed."""

        return "<Attr attr_id={} name={}>".format(self.attr_id, self.name)


class TrailAttr(db.Model):
    """TrailAttr Model. """

    __tablename__ = "trailattrs"

    trailattr_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"), nullable=False)
    attr_id = db.Column(db.Integer, db.ForeignKey("attrs.attr_id"), nullable=False)

    trail = db.relationship("Trail", backref=db.backref("trailattrs", order_by=trailattr_id))
    attr = db.relationship("Attr", backref=db.backref("trailattrs", order_by=trailattr_id))

    def __repr__(self):
        """Provide helpful representation about a TrailAttr for trail when printed."""

        return "<TrailAttr trailattr_id={}>".format(self.trailattr_id)


class Friendship(db.Model):
    """Friend Model."""

    __tablename__ = "friendships"

    friend_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    user2_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

    def __repr__(self):
        """Provide helpful representation about a friend when printed."""

        return "<Friend friend_id={}>".format(self.friend_id)


class Recommendation(db.Model):
    """Recommendation Model."""

    __tablename__ = "recommendations"

    recommendation_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    friend_id = db.Column(db.Integer, db.ForeignKey("friendships.friend_id"), nullable=False)
    comments = db.Column(db.String(500), nullable=False)

    friend = db.relationship("Friendship", backref=db.backref("recommendations", order_by=recommendation_id))

    def __repr__(self):
        """Provide helpful representation about a recommendation for trail when printed."""

        return "<Recommendation frecommendation_id={}>".format(self.recommendation_id)


def connect_to_db(app, dbname):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///' + dbname
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates a user and adds it to the database.
    u1 = User(name="Test", email="fun@hb.com", zipcode=12345, password=1234)
    u2 = User(name="Test1", email="exciting@hb.com", zipcode=12345, password=1234)
    t1 = Trail(name="test trail", url="www.testtrail.com")
    ut1 = UserTrail(user_id=1, trail_id=1)
    h1 = Hike(usertrail_id=1, date="2018-12-02")
    db.session.add_all([u1, u2, t1, ut1, h1])
    db.session.commit()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from flask import Flask
    app = Flask(__name__)
    connect_to_db(app, "hiking")
    db.create_all()
    print "Connected to DB."
