# Python batteries included
from unittest import TestCase
from unittest.mock import Mock, patch
import os

# importing itemsAPI program that Eric made
from ItemsAPI import add_item, get_item, item_detail, item_update, item_delete
import ItemsAPI

# These are pip installs
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask, request, jsonify
import tempfile
import flask
import requests
from nose.tools import assert_true, assert_is_not_none

app = Flask(__name__)
# Binding these to the Flask
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Making a class so the unit testing can use
# http://flask.pocoo.org/docs/0.12/testing/
#   Testing Flask Applications
#   Something that is untested is broken.
class TestItemsAPI(TestCase):

    # https://stackoverflow.com/questions/24877025/runtimeerror-working-outside-of-application-context-when-unit-testing-with-py
    # def setUp(self):
    #     self.app_context = app.app_context()
    #     self.app_context.push()

    # # http://flask.pocoo.org/docs/0.12/testing/
    # def setUp(self):
    #     self.db_fd, flask.app.config['DATABASE'] = tempfile.mkstemp()
    #     flask.app.testing = True
    #     self.app = flask.app.test_client()
    #     with flask.app.app_context():
    #         flask.init_db()
    #
    # # http://flask.pocoo.org/docs/0.12/testing/
    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(flask.app.config['DATABASE'])

    # http://www.patricksoftwareblog.com/unit-testing-a-flask-application/
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        test_db_url = 'test_itemsAPI.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, test_db_url)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        # Disable sending emails during unit testing
        # mail.init_app(app)
        self.assertEqual(app.debug, False)

    # no homepage so a 404 error is expected
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 404)

    # http://flask.pocoo.org/docs/0.12/testing/
    # def test_empty_db(self):
    #     rv = self.app.get('/items')
    #     assert b'No entries here so far' in rv.data

    # def tearDown(self):
    #     os.close(self.db_fd)
    #     os.unlink(flaskr.app.config['DATABASE'])
    # https://stackoverflow.com/questions/24877025/runtimeerror-working-outside-of-application-context-when-unit-testing-with-py
    # @classmethod
    # def setUpClass(cls)
    #     app.config['SERVER_NAME'] = 'localhost:5000'
    #     cls.client = app.test_client()

    # https://stackoverflow.com/questions/24877025/runtimeerror-working-outside-of-application-context-when-unit-testing-with-py
    def tearDown(self):
        # self.app_context.pop()
        pass

    # def setUp(self):
    #     # TODO: Create temp db to use
    #     ItemsAPI.db = self.test_db_url
    #     basedir = os.path.abspath(os.path.dirname(__file__))
    #     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'items.sqlite')
    #
    #
    #     db.session.commit()

    # This test to see if sending a model give a proper response
    def test_Item_model(self):
        # http://www.patricksoftwareblog.com/unit-testing-a-flask-application/
        with app.app_context():
            # item = Item(user, itemName, location, whereBought, whenBought, cost, website, whoBarrowed, whenBarrowed, whenReturned, whereBarrowed)
            item = ItemsAPI.Item("", "", "", "", "", "", "", "", "", "", "")
            response = ItemsAPI.item_schema.jsonify(item)
            self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        # TODO: make a test and comment out pass
        pass

        # https://realpython.com/testing-third-party-apis-with-mocks/
        # Send a request to the API server and store the response.
        # response = requests.get('http://jsonplaceholder.typicode.com/todos')
        # print(response)
        # Confirm that the request-response cycle completed successfully.
        # assert_true(response.ok)

        # https://realpython.com/testing-third-party-apis-with-mocks/
    @patch('requests.get')
    def test_getting_todos(self, mock_get):
        with app.app_context():
            # Configure the mock to return a response with an OK status code.
            mock_get.return_value.ok = True

            # Call the service, which will send a request to the server.
            response = get_item()
            print(response)

            # If the request is sent successfully, then I expect a response to be returned.
            assert_is_not_none(response)

    # https://realpython.com/testing-third-party-apis-with-mocks/
    @patch('requests.get')
    def test_getting_todos_when_response_is_ok(self, mock_post):
        with app.app_context():
            # todos = [{"cost": "","itemName": "", "location": "", "user": "", "website": "", "whenBarrowed": "", "whenBought": "", "whenReturned": "", "whereBarrowed": "", "whereBought": "", "whoBarrowed": ""}]

            # Configure the mock to return a response with an OK status code. Also, the mock should have
            # a `json()` method that returns a list of todos.
            mock_post.return_value = Mock(ok=True)
            mock_post.return_value.json.return_value = todos

            # Call the service, which will send a request to the server.
            response = add_item()

            # If the request is sent successfully, then I expect a response to be returned.
            assert_list_equal(response.json(), todos)


        # def test_output(self):
        # with app.test_request_context():
        # # mock object
        #     out = output("error", "Test Error", "local_host")
        #     # Passing the mock object
        #     response = [
        #       {
        #              'type': 'error',
        #              'message': 'Test Error',
        #              'download_link': 'local_host'
        #        }
        #     ]
        #     data = json.loads(out.get_data(as_text=True)
            # Assert response
            # self.assertEqual(data[‘response’], response)

        # response = requests.get("127.0.0.1:5000/add_item")
        # response.json()

        # item = ItemsAPI.Item("", "", "", "", "", "", "", "", "", "", "")
        # conn = httplib.HTTPConnection("127.0.0.1:5000/add_item")
        # res = conn.getresponse()
        # print(res.status, res.reason)


        # https://stackoverflow.com/questions/17178483/how-do-you-send-an-http-get-web-request-in-python
        # import httplib
        # conn = httplib.HTTPConnection("www.python.org")
        # conn.request("HEAD","/index.html")
        # res = conn.getresponse()
        # print res.status, res.reason
        # # Result:
        # 200 OK
        # http://www.patricksoftwareblog.com/unit-testing-a-flask-application/
        # def test_valid_user_registration(self):
        #     response = self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')
        #     self.assertEqual(response.status_code, 200)
        #     self.assertIn(b'Thanks for registering!', response.data)


        # http://flask.pocoo.org/docs/1.0/appcontext/
        # with app.app_context():
        #     init_db()
        # https://stackoverflow.com/questions/31444036/runtimeerror-working-outside-of-application-context/31444175
        # with app.app_context():
        #     with patch('__main__.mysql.connector.connect') as  mock_mysql_connector_connect:
        #        object=TestMySQL()
        #        object.before_request() #Runtime error on calling this"""


        # r = self.post(url_for("item/add"))
        # self.assertEqual(r.status_code, 200)

        # item = ItemsAPI.Item("", "", "", "", "", "", "", "", "", "", "")
        # item = ItemsAPI.Item({"cost": "","itemName": "", "location": "", "user": "", "website": "", "whenBarrowed": "", "whenBought": "", "whenReturned": "", "whereBarrowed": "", "whereBought": "", "whoBarrowed": ""})
        # ItemsAPI.item_schema.jsonify(item)
        # expected = {"cost": "","itemName": "", "location": "", "user": "", "website": "", "whenBarrowed": "", "whenBought": "", "whenReturned": "", "whereBarrowed": "", "whereBought": "", "whoBarrowed": ""}
        # self.compare_db_expected(expected )
        # "cost": "","itemName": "", "location": "", "user": "", "website": "", "whenBarrowed": "", "whenBought": "", "whenReturned": "", "whereBarrowed": "", "whereBought": "", "whoBarrowed": ""


        # c = app.test_client()
        # rv = c.get('/mypage', query_string={"cost": "","itemName": "", "location": "", "user": "", "website": "", "whenBarrowed": "", "whenBought": "", "whenReturned": "", "whereBarrowed": "", "whereBought": "", "whoBarrowed": ""})
        # expected_data = {"cost": "","itemName": "", "location": "", "user": "", "website": "", "whenBarrowed": "", "whenBought": "", "whenReturned": "", "whereBarrowed": "", "whereBought": "", "whoBarrowed": ""}
        # assert jsonify(rv.get_data()) == expected_data

        # gets
        # RuntimeError: Working outside of application context.
        #
        # This typically means that you attempted to use functionality that needed
        # to interface with the current application object in some way. To solve
        # this, set up an application context with app.app_context().  See the
        # documentation for more information.
        # pass

    def test_get_item(self):
        # TODO: make a test and comment out pass
        pass

    def test_item_detail(self):
        # TODO: make a test and comment out pass
        pass

    def test_item_update(self):
        # TODO: make a test and comment out pass
        pass

    def test_item_delete(self):
        # TODO: make a test and comment out pass
        pass


    def changing_json_file(self,json):
        id = request.json['id']
        user =request.json['user']
        itemName = request.json['itemName']
        location = request.json['location']
        whereBought = request.json['whereBought']
        whenBought = request.json['whenBought']
        cost = request.json['cost']
        website = request.json['website']
        whoBarrowed = request.json['whoBarrowed']
        whenBarrowed = request.json['whenBarrowed']
        whenReturned = request.json['whenReturned']
        whereBarrowed = request.json['whereBarrowed']

if __name__ == '__main__':
    TestCase.main()
