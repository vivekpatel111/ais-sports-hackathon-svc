"""This module defines service objects for various API endpoints for tagging
   service"""

# Imports

# from model import Detector
import pymongo
from flask_login import current_user
from pymongo import MongoClient

import errors
import logging

# Globals
import svc_utils

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


class UpdateInfo(object):
    """Service object for implementing keyword similarity in a single
       application mode. For a single pair of a keyword and a list of
       words"""

    def __init__(self, inputData):
        """Expects input_data to be a map containing required keys."""
        self.info_dict = None
        try:
            data = inputData["data"]
            user_weight = data.get('weight', None)
            user_height = data.get('height', None)
            user_age = data.get('age', None)
            info_dict = {}
            if user_weight: info_dict['weight'] = user_weight
            if user_height: info_dict['height'] = user_height
            if user_age: info_dict['age'] = user_age
            self.info_dict = info_dict
        except KeyError, err:
            logger.error("Input data does not have correct attributes")
            logger.error("%s", err)
            raise errors.IncorrectRequestData()

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
