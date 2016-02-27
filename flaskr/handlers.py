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


class UpdateInfo(Handler, object):
    def __init__(self):
        LOGGER.debug("Initialized UpdateInfo handler")

    def get(self, svc_obj):
        result = svc_obj.get()
        return result


class AddFriend(Handler, object):
    def __init__(self):
        LOGGER.debug("Initialized UpdateInfo handler")

    def get(self, svc_obj):
        result = svc_obj.get()
        return result


class FriendRequestAction(Handler, object):
    def __init__(self):
        LOGGER.debug("Initialized UpdateInfo handler")

    def get(self, svc_obj):
        result = svc_obj.get()
        return result


class HandlerFactory(object):
    def __init__(self):
        pass

    # static attributes store the actual instances of handlers
    all_handlers = {
        'update_info': UpdateInfo(),
        'add_friend': AddFriend(),
        'friend_request_action': FriendRequestAction()
    }

    @staticmethod
    def get_handler(name):
        if name == 'UpdateInfo':
            return HandlerFactory.all_handlers['update_info']
        elif name == 'AddFriend':
            return HandlerFactory.all_handlers['add_friend']
        elif name == 'FriendRequestAction':
            return HandlerFactory.all_handlers['friend_request_action']
