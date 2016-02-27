# imports
import copy
import json
import logging
import os
import urllib

import time
from pymongo import MongoClient
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Response, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required
import communicators
from errors import UsernameAlreadyExists
from models.user import User
import svc_utils
from constants.response_objects import SvcResponseObjects
from constants import response_objects
from flask_login import current_user

# configuration


DEBUG = True
SECRET_KEY = 'development key'

OK_RESPONSE = 200
DATABASE = "sports_hack"
USER_COLLECTION = "users"
client = MongoClient('localhost', 27017)
db = client[DATABASE]
collection = db[USER_COLLECTION]

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
logger = logging.getLogger(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def get_sample_response(err_b, err_m, response, username=None):
    resp = copy.deepcopy(SvcResponseObjects.get_svc_resp_object())
    resp[response_objects.RESP_ERROR_BOOL_KEY] = err_b
    resp[response_objects.RESP_ERROR_MSG_KEY] = err_m
    resp[response_objects.RESP_RES_KEY] = response
    resp[response_objects.RESP_USER_KEY] = username
    return resp


@app.route('/')
@login_required
def home():
    return svc_utils.get_response_from_dict(get_sample_response(None, None, None, None))


@app.route('/register', methods=['GET', 'POST'])
def register():
    str_data = urllib.unquote_plus(request.get_data()).decode('utf-8')
    input_data = json.loads(str_data)
    username = input_data.get('username', None)
    try:
        user_obj = User.register(input_data, collection)
    except UsernameAlreadyExists as e:
        return svc_utils.get_response_from_dict(get_sample_response(True, e.message, {}, username))
    login_user(user_obj)
    return svc_utils.get_response_from_dict(get_sample_response(False,
                                                                None,
                                                                "Logged in successfully",
                                                                username))


@app.route('/login', methods=['POST'])
def login():
    str_data = urllib.unquote_plus(request.get_data()).decode('utf-8')
    input_data = json.loads(str_data)
    if request.method == 'POST':
        user = User.get(input_data['username'], collection)
        if user and User.validate_login(user['password'], input_data['password']):
            user_obj = User(user['username'])
            login_user(user_obj)
            return svc_utils.get_response_from_dict(get_sample_response(False,
                                                                        None,
                                                                        "Successfully logged in!!",
                                                                        user['username']))
        else:
            return svc_utils.get_response_from_dict(get_sample_response(True,
                                                                        "Login failed",
                                                                        "Login failed!",
                                                                        user['username']))
    else:
        return svc_utils.get_response_from_dict(get_sample_response(True,
                                                                    "Please provide Username and password to login",
                                                                    "Please provide Username and password to login",
                                                                    input_data['username']))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return svc_utils.get_response_from_dict(get_sample_response(False,
                                                                None,
                                                                "Successfully logged out!",
                                                                None))


@login_manager.unauthorized_handler
def unauthorized():
    return svc_utils.get_response_from_dict(get_sample_response(True,
                                                                "Login required",
                                                                None,
                                                                None))


@login_manager.user_loader
def load_user(userid):
    user_doc = User.get(userid, collection)
    return User(user_doc['username'])


@app.route('/personal/updateInfo', methods=['POST'])
@login_required
def update_user_info():
    logger.info("Recieved request for updating user's info by user- %s", current_user.get_id())
    start = time.time()
    try:
        response = UPDATE_INFO_SERV.invoke_insert(request)
    except Exception as e:
        return svc_utils.get_response_from_dict(svc_utils.get_sample_response(True,
                                                                              e.message,
                                                                              "Error while updating info",
                                                                              current_user.get_id()))
    logger.info("Request evaluation time in seconds: %s",
                str(time.time() - start))
    logger.info("Sending a reponse for single request for raw text")
    return response


@app.route('/personal/activity', methods=['POST'])
@login_required
def handle_activities():
    logger.info("Recieved request for fetching activities %s", current_user.get_id())
    try:
        response = GET_USER_FEED.invoke_insert(request)
    except Exception as e:
        return svc_utils.get_response_from_dict(svc_utils.get_sample_response(True,
                                                                              e.message,
                                                                              "Error while fetching activities",
                                                                              current_user.get_id()))
    return response

@app.route('/personal/FriendRequestAction', methods=['POST'])
@login_required
def take_action_friend_request():
    logger.info("Received request for taking action on a friend request. request-%s", request)

    try:
        response = FRIEND_REQUEST_ACTION.invoke_insert(request)
    except Exception as e:
        return svc_utils.get_response_from_dict(
                svc_utils.get_sample_response(True,
                                              e.message,
                                              "Error while acting on friend request",
                                              current_user.get_id())
        )
    return response


@app.route('/personal/GetUsersList', methods=['POST', 'GET'])
@login_required
def get_users_list():
    logger.info("received request")

    try:
        response = GET_USERS_LIST.invoke_insert(request)
    except Exception as e:
        return svc_utils.get_response_from_dict(
                svc_utils.get_sample_response(True,
                                              e.message,
                                              "Error while fetching users list",
                                              current_user.get_id())
        )
    return response


@app.route('/friend/add', methods=['POST'])
@login_required
def add_friend():
    logger.info("Add friend request")
    try:
        response = ADD_FRIEND.invoke_insert(request)
    except Exception as e:
        return svc_utils.get_response_from_dict(svc_utils.get_sample_response(True,
                                                                              e.message,
                                                                              "Error while sending friend request",
                                                                              current_user.get_id()))
    return response


@app.route('/friend/compareWithFriend', methods=['POST', "GET"])
@login_required
def get_comparison_with_firends():
    logger.info("Received request")
    try:
        response = FRIEND_COMPARISON.invoke_insert(request)
    except Exception as e:
        return svc_utils.get_response_from_dict(svc_utils.get_sample_response(True,
                                                                              "Failed",
                                                                              "Failed",
                                                                              current_user.get_id())
                                                )
    return response


def configure_logging():
    """Sets up logging configuration. It is assumed that the logging
    configuration is provided in configuration file. If the logging config file
    is not provided, it creates a basic logging configuration"""

    curr_dir = os.path.dirname(os.path.realpath(__file__))
    logging_config_path = os.path.join(curr_dir, '..', 'config',
                                       'log_config.json')
    if os.path.exists(logging_config_path):
        with open(logging_config_path, 'r') as log_file:
            config = json.load(log_file)
        logging.config.dictConfig(config)
    else:
        default_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=default_format)


def register_servlets():
    """Creates instances of different servlet objects"""
    global UPDATE_INFO_SERV
    global GET_FRIENDS_FEED
    global ADD_FRIEND
    global FRIEND_REQUEST_ACTION
    global GET_USERS_LIST
    global FRIEND_COMPARISON
    global GET_USER_FEED

    UPDATE_INFO_SERV = communicators.UpdateInfoServlet()
    GET_FRIENDS_FEED = communicators.FriendsFeedServlet()
    ADD_FRIEND = communicators.AddFriendServlet()
    FRIEND_REQUEST_ACTION = communicators.FriendRequestActionServlet()
    GET_USERS_LIST = communicators.UsersListServlet()
    FRIEND_COMPARISON = communicators.ComparisonWithFriendsServlet()
    GET_USER_FEED = communicators.UserFeedServlet()


@app.before_first_request
def configure_everything():
    """Global, service level configurations"""
    configure_logging()
    register_servlets()


if __name__ == '__main__':
    app.run(debug=True)
