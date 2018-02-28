import unittest
from server import app
from model import db, example_data, connect_to_db
import json


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

    
    def test_signin_yet(self):
        result = self.client.get("/SignIn")
        self.assertIn("SignIn", result.data)
        self.assertNotIn("Logout", result.data)


    def test_no_signup_yet(self):
        result = self.client.get("/SignUp")
        self.assertIn("SignUp", result.data)
        self.assertNotIn("Logout", result.data)


class HikeTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "testdb")

        with self.client as c:
                with c.session_transaction() as sess:
                    sess['id'] = 1

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        # (uncomment when testing database)
        db.session.close()
        db.drop_all()

    def test_search(self):
        #search without signin in
        result = self.client.get("/search")
        self.assertIn("Enter", result.data)
        self.assertNotIn("Signed In", result.data)


    def test_user_profile(self):
        #FIXME: test that the user page displays the user from example_data()
        result = self.client.get("/users/1")
        self.assertIn("Test", result.data)
        self.assertNotIn("Test3", result.data)

    def test_signin(self):
        result = self.client.post("/SignIn",
                                data={"email": "fun@hb.com",
                                      "password": "1234"},
                                follow_redirects=True)
        self.assertIn("Hike List", result.data)
        self.assertIn("Test", result.data)

    def test_signup(self):
        result = self.client.post("/SignUp",
                              data={"name": "unittest",
                                    "email": "unittest@hb.com",
                                    "zip": "11111",
                                    "password": "1234"
                                    },
                              follow_redirects=True)
        self.assertIn("Registered successfully", result.data)
        self.assertIn("Search", result.data)

    def test_search_zipcode(self):
        result = self.client.post("/search",
                              data={"zipcode": "94102"
                                    },
                              follow_redirects=True)
        self.assertIn("Land", result.data)
        self.assertIn("URL", result.data)

    def test_search_location(self):
        result = self.client.post("/search",
                              data={"location": "Fremont"
                                    },
                              follow_redirects=True)
        self.assertIn("Mission", result.data)
        self.assertIn("URL", result.data)


    def test_get_trail_info(self):
        result = self.client.post("/get-trails-info",
                                data={"trail_id": "1",
                                      "date": "2018-02-24",
                                      "user_id": "1",
                                      "name": "name",
                                      "url": "url",
                                      "length": "2.5",
                                      "rating": "1.5"},
                                      follow_redirects=True)

        result_json_data = json.loads(result.data)
        self.assertEqual(result_json_data['trail_id'],"1")

    def test_get_comment_info(self):
        result = self.client.post("/add-trails-comment",
                                data={"trail_id": "1",
                                      "comments": "abcd",
                                      "hike_id": "1"},
                                      follow_redirects=True)

        result_json_data = json.loads(result.data)
        self.assertEqual(result_json_data['trail_id'],"1")


    def test_get_rating_info(self):
        result = self.client.post("/add-rating",
                                data={"hike_id": "1",
                                      "u_rating": "2.5"
                                      },
                                      follow_redirects=True)

        result_json_data = json.loads(result.data)
        self.assertEqual(result_json_data['hike_id'],"1")

    def test_send_email(self):
        result = self.client.post("/send-email",
                                data={"trail_name": "test trail",
                                    "trail_url": "test trail",
                                    "hike_id": "1",
                                    "trail_length": "test trail",
                                    "T_email": "niravtrivedi03@gmail.com",
                                    "F_email": "niravtrivedi03@gmail.com",
                                    "message": "recommending ",
                                    "user_name": "user_name"},
                                    follow_redirects=True)
        result_json_data = json.loads(result.data)
        self.assertEqual(result_json_data['trail_name'],"test trail")


if __name__ == "__main__":
    unittest.main()
