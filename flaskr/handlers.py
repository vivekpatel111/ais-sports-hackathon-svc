""" Handlers

  This module implements the actual handler classes.
  Implements thin wrappers over service objects

"""

# Imports
from abc import ABCMeta, abstractmethod
import logging

# Constants
LOGGER = logging.getLogger(__name__)


# Classes


class Handler():
    """Abstract base class for handlers. The children must implement get method
    """
    ___metaclass__ = ABCMeta

    @abstractmethod
    def get(self, data):
        """This method should implement the logic for the correponding endpoint
        """
        pass


class SimilarKwdsSingle(Handler, object):
    """Provides handling logic for the case of matching similar words for given
       list of words"""

    def __init__(self):
        """Expects input_data to be a map """
        LOGGER.debug("Initialized  single handler")

    def get(self, svc_obj):
        """Implements a logic wrapper for extracting tags from raw text.
           Expects a corresponding service object instance in input"""
        tag_result = svc_obj.get()
        return tag_result


class UpdateInfo(Handler, object):
    def __init__(self):
        """Expects input_data to be a map containing a particular key for text
        data"""
        LOGGER.debug("Initialized UpdateInfo handler")

    def get(self, svc_obj):
        """Implements a logic wrapper for extracting tags from raw text.
           Expects a corresponding service object instance in input"""
        result = svc_obj.get()
        return result


class HandlerFactory(object):
    """Returns appropriate handlers depending upon the endpoints"""

    def __init__(self):
        pass

    # static attributes store the actual instances of handlers
    all_handlers = {
        'update_info': UpdateInfo()
    }

    @staticmethod
    def get_handler(name):
        """Return appropriate handler instance"""
        if name == 'UpdateInfo':
            return HandlerFactory.all_handlers['update_info']
