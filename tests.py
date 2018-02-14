import unittest
from server import app
from model import db, example_data, connect_to_db


class HikeTests(unittest.TestCase):
    """Tests for my Hike site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("nearby Trails", result.data)

    def test_no_signin_yet(self):
        result = self.client.get("/")
        self.assertIn("SignIn", result.data)
        self.assertNotIn("Logout", result.data)

    def test_search(self):
        #search without signin in
        result = self.client.get("/search")
        self.assertNotIn("Select", result.data)
        self.assertIn("Signed In", result.data)

    def test_signin_yet(self):
        result = self.client.get("/SignIn")
        self.assertIn("SignIn", result.data)
        self.assertNotIn("Logout", result.data)

    def test_signup_yet(self):
        result = self.client.get("/SignUp")
        self.assertIn("SignUp", result.data)
        self.assertNotIn("Logout", result.data)


class HikeTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "testdb")

        with self.client as c:
                with c.session_transaction() as sess:
                    sess['id'] = True

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_games(self):
        #FIXME: test that the user page displays the user from example_data()
        result = self.client.get("/users/1")
        self.assertIn("Test", result.data)
        self.assertNotIn("Test3", result.data)


if __name__ == "__main__":
    unittest.main()