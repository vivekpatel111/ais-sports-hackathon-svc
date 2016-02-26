"""This module defines service objects for various API endpoints for tagging
   service"""

# Imports

# from model import Detector
import pymongo
from flask_login import current_user
from pymongo import MongoClient

import errors
import logging
from flaskr.static import send_notification

# Globals
import svc_utils
from flaskr.static.send_notification import GCMessage
from models import user_info

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

# MODEL = Detector()
logger = logging.getLogger(__name__)


class FriendRequestAction(object):
    def __init__(self, inputData):
        try:
            self.action = inputData['action']
            self.add_friend = inputData['friend_username']
        except KeyError as e:
            raise errors.IncorrectRequestData

    def get(self):
        try:
            friend_request_sendor = collection.find_one({'username': self.add_friend})
            if None == friend_request_sendor:
                logger.error("Given username doesn't exist")
                raise errors.IncorrectRequestData("Username doesn't exist")
            else:
                sent_friend_request = friend_request_sendor['sent_friend_request']
                if current_user.get_id() in sent_friend_request:
                    collection.update_one({'username': self.add_friend},
                                          {'$pull': {'sent_friend_request': current_user.get_id()},
                                           '$push': {'friends': current_user.get_id()}})
                    collection.update_one({'username': current_user.get_id()},
                                          {'$push': {'friends': current_user.get_id()}})
                    logger.info("Friend request accepted successfully")
                    doc = collection.find_one({'username': self.add_friend})
                    if None == doc:
                        raise errors.IncorrectRequestData
                    else:
                        gmc_auth = doc['credentials']['gmc_auth']
                    data = {
                        "to": self.add_friend,
                        "data": {
                            "message": str(current_user.get_id()) + " accepted your friend request",
                        }
                    }
                    gcmessenger = GCMessage(gmc_auth)
                    if not gcmessenger.post_request(data):
                        logger.error("Friend request notification not sent")
                    return svc_utils.get_response_from_dict(svc_utils.get_sample_response(False,
                                                                                          None,
                                                                                          "Added to friends",
                                                                                          current_user.get_id()))
                else:
                    logger.error("Invalid username passed")
                    return svc_utils.get_response_from_dict(svc_utils.get_sample_response(True,
                                                                                          "Request not found",
                                                                                          "Request not found",
                                                                                          current_user.get_id()))
        except Exception as e:
            logger.error("Error while responding to friend request")
            return errors.SERVER_ERROR


class AddFriend(object):
    def __init__(self, inputData):
        try:
            self.add_friend = inputData['friend_username']
        except KeyError as e:
            raise errors.IncorrectRequestData

    def get(self):
        try:
            friend_to_add = collection.find_one({"username": self.add_friend})
            if None == friend_to_add:
                logger.error("Username to be added doesn't exist")
                raise errors.IncorrectRequestData("Username to be added doesn't exist")
            else:
                friend_gmc_auth = friend_to_add['credentials']['gmc_auth']
            data = {
                "to": self.add_friend,
                "data": {
                    "message": str(current_user.get_id()) + " sent you a friend request",
                }
            }
            gcmessenger = GCMessage(friend_gmc_auth)
            if gcmessenger.post_request(data):
                collection.update_one({'username': current_user.get_id()},
                                      {'$addToSet': {'sent_friend_request': self.add_friend}})
                return True
            else:
                raise errors.SERVER_ERROR("Error in sending friend request")
        except Exception as e:
            logger.error("Error while sending friend request")
            raise errors.SERVER_ERROR("Error while sending friend request")


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
