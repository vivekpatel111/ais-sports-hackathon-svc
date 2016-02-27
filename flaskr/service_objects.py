"""This module defines service objects for various API endpoints for tagging
   service"""

# Imports

# from model import Detector
import pymongo
from flask_login import current_user
from pymongo import MongoClient

import errors
import logging
from models import computation

# Globals
import svc_utils
from static.send_notification import GCMessage
from models import user_info
import re

WORD = 'word'
RAW_DATA = 'raw_data'
URL = 'url'
BATCH_LIST = 'data'
ID = 'id'
USERNAME = 'username'
DATABASE = 'sports_hack'
COLLECTION = 'users'
client = MongoClient('localhost', 27017)
db = client[DATABASE]
collection = db[COLLECTION]

ACTION = ['ACCEPT', 'REJECT']

logger = logging.getLogger(__name__)


class ComparisonWithFriends(object):
    def __init__(self, input_data):
        self.input_data = input_data

    def get(self):
        user_doc = collection.findOne({'username': current_user.get_id()})
        goal = user_doc['goal']
        if not goal:
            return svc_utils.get_response_from_dict(svc_utils.get_sample_response(False,
                                                                                  None,
                                                                                  [],
                                                                                  current_user.get_id()))
        friends = user_doc['friends']
        friends_with_same_goal = []
        for friend in friends:
            friend_doc = collection.findOne({'username': friend})
            if not friend_doc or friend_doc.get('goal', None) != goal:
                continue
            friends_with_same_goal.append(friend_doc['username'])
        response_data = computation.compare_friends(current_user.get_id(),
                                                    friends_with_same_goal)



class UsersList(object):
    def __init__(self, input_data):
        try:
            self.regex_str = input_data['regex_str']
        except KeyError as e:
            raise errors.IncorrectRequestData

    def get(self):
        try:
            users_list = []
            regx = re.compile(self.regex_str)
            users_list_doc = collection.find({'username': {"$regex": regx}})
            for doc in users_list_doc:
                user_inf = {'username': doc.get('username', None),
                            'date_of_birth': doc.get('date_of_birth'),
                            'location': doc.get('location', None),
                            'name': doc.get('name', None),
                            'weight': doc.get('weight', None),
                            'height': doc.get('height', None)}
                users_list.append(user_inf)
            return svc_utils.get_sample_response(False,
                                                 None,
                                                 {'usersList': users_list},
                                                 current_user.get_id()
                                                 )
        except Exception as e:
            return svc_utils.get_sample_response(True,
                                                 "Error while fetching users",
                                                 {'usersList': None},
                                                 current_user.get_id()
                                                 )

class FriendRequestAction(object):
    def __init__(self, inputData):
        try:
            self.action = inputData['action']
            if self.action not in ACTION:
                raise errors.IncorrectRequestData
            self.add_friend = inputData['friend_username']
        except KeyError as e:
            raise errors.IncorrectRequestData

    def get(self):
        try:
            friend_request_sendor = collection.find_one({'username': self.add_friend})
            print self.action == 'ACCEPT', current_user.get_id()
            if None == friend_request_sendor:
                logger.error("Given username doesn't exist")
                return svc_utils.get_sample_response(True,
                                                     "Given username doesn't exist",
                                                     "No such user found",
                                                     current_user.get_id())
            elif self.action == "ACCEPT":
                sent_friend_request = friend_request_sendor['sent_friend_request']
                if current_user.get_id() in sent_friend_request:
                    collection.update_one({'username': self.add_friend},
                                          {'$pull': {'sent_friend_request': current_user.get_id()},
                                           '$push': {'friends': current_user.get_id()}})
                    collection.update_one({'username': current_user.get_id()},
                                          {'$push': {'friends': self.add_friend}})
                    logger.info("Friend request accepted successfully")
                    gmc_auth = friend_request_sendor['credentials']['gmc']['auth_key']
                    data = {
                        "to": gmc_auth,
                        "notification": {
                            "title": "Friend request accepted",
                            "username": str(current_user.get_id()),
                            "message": str(current_user.get_id()) + "accepted your friend request",
                            "sound": ""
                        }
                    }
                    gcmessenger = GCMessage()
                    if not gcmessenger.post_request(data):
                        logger.error("Friend request notification not sent")
                    return svc_utils.get_sample_response(False,
                                                         None,
                                                         "Added to friends",
                                                         current_user.get_id())
                else:
                    print "testing checkpoint"
                    logger.error("Invalid username passed")
                    return svc_utils.get_sample_response(True,
                                                         "Request not found",
                                                         "Request not found",
                                                         current_user.get_id())
            elif self.action == "REJECT":
                collection.update_one({'username': self.add_friend},
                                      {'$pull': {'sent_friend_request': current_user.get_id()}})
                return svc_utils.get_sample_response(False,
                                                     None,
                                                     "Request deleted!")
        except Exception as e:
            logger.error("Error while responding to friend request")
            return svc_utils.get_sample_response(True,
                                                 "Failed",
                                                 "Failed",
                                                 current_user.get_id())
        return svc_utils.get_sample_response(True,
                                             "Failed",
                                             "Failed",
                                             current_user.get_id())

class AddFriend(object):
    def __init__(self, inputData):
        try:
            self.add_friend = inputData['data']['friend_username']
        except KeyError as e:
            raise errors.IncorrectRequestData

    def get(self):
        try:
            friend_to_add = collection.find_one({"username": self.add_friend})
            if None == friend_to_add:
                logger.error("Username to be added doesn't exist")
                return svc_utils.get_sample_response(True,
                                                     "Username to be added doesn't exist",
                                                     "Username to be added doesn't exist",
                                                     current_user.get_id())
            else:
                friend_gmc_auth = friend_to_add['credentials']['gmc']['auth_key']
            data = {
                "to": friend_gmc_auth,
                "notification": {
                    "title": "Friend request",
                    "message": str(current_user.get_id()) + " sent you a friend request",
                    "sound": ""
                }
            }
            gcmessenger = GCMessage()
            if gcmessenger.post_request(data):
                collection.update_one({'username': current_user.get_id()},
                                      {'$addToSet': {'sent_friend_request': self.add_friend}})
                return svc_utils.get_sample_response(False,
                                                     None,
                                                     "Friend request sent successfully!",
                                                     current_user.get_id())
            else:
                return svc_utils.get_sample_response(True,
                                                     "Error while sending friend request",
                                                     "Error while sending friend request",
                                                     current_user.get_id())
        except Exception as e:
            logger.error("Error while sending friend request")
            return svc_utils.get_sample_response(True,
                                                 "Error while sending friend request",
                                                 "Error while sending friend request",
                                                 current_user.get_id())

class FriendsFeed(object):
    def __init__(self, inputData):
        """Expects input_data to be a map containing required keys."""
        self.info_dict = None
        try:
            data = inputData["data"]
            updated_info = data["friend_list"]
            updated_info = dict((k, v) for k, v in updated_info.iteritems() if v)
            # Validate info keys in request
            self.validate_updated_info(updated_info)
            self.info_dict = updated_info
        except errors.IncorrectRequestData, err:
            logger.error("Input data does not have correct attributes")
            logger.error("%s", err)
            raise errors.IncorrectRequestData()

class UpdateInfo(object):
    def __init__(self, inputData):
        """Expects input_data to be a map containing required keys."""
        self.info_dict = None
        try:
            data = inputData["data"]
            updated_info = data["user_info"]
            updated_info = dict((k, v) for k, v in updated_info.iteritems() if v)
            # Validate info keys in request
            self.validate_updated_info(updated_info)
            self.info_dict = updated_info
        except errors.IncorrectRequestData, err:
            logger.error("Input data does not have correct attributes")
            logger.error("%s", err)
            raise errors.IncorrectRequestData()

    def validate_updated_info(self, dic):
        print "check"
        for key in dic:
            if key not in user_info.user_info_structure:
                raise errors.IncorrectRequestData()
            if key in user_info.USER_INFO_VAL_OBJECT_KEYS:
                for nested_key in dic[key]:
                    if nested_key not in user_info.value_object:
                        logger.error("Incorrect update info request data.")
                        logger.error("Invalid key : %s", nested_key)
                        raise errors.IncorrectRequestData()
        logger.info("Update info object validated for user %s", current_user.get_id())
        return

    def get(self):
        """Implements a logic wrapper for extracting tags from raw text"""
        return self.update_user_info()

    def update_user_info(self):
        username = current_user.get_id()
        try:
            collection.update_one({'username': username},
                                  {"$set": self.info_dict},
                                  upsert=False)
            return svc_utils.get_sample_response(False,
                                                 None,
                                                 None,
                                                 current_user.get_id())
        except pymongo.errors.PyMongoError as e:
            logger.error("Error while updating the user info")
            return svc_utils.get_sample_response(True,
                                                 "User info update failed",
                                                 "Update failed",
                                                 current_user.get_id())
