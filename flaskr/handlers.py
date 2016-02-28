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


class UsersList(Handler, object):
    def __init__(self):
        LOGGER.debug("Initialized UsersList handler")

    def get(self, svc_obj):
        result = svc_obj.get()
        return result

class UserFeed(Handler, object):
    def __init__(self):
        LOGGER.debug("Initialized UserFeed handler")

    def get(self, svc_obj):
        result = svc_obj.get()
        return result


class ComparisonWithFriends(Handler, object):
    def __init__(self):
        LOGGER.debug("Initialized UsersList handler")

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
        'friend_request_action': FriendRequestAction(),
        'get_users_list': UsersList(),
        'comparison_with_friends': ComparisonWithFriends(),
        'user_feed':UserFeed()
    }

    @staticmethod
    def get_handler(name):
        if name == 'UpdateInfo':
            return HandlerFactory.all_handlers['update_info']
        elif name == 'AddFriend':
            return HandlerFactory.all_handlers['add_friend']
        elif name == 'FriendRequestAction':
            return HandlerFactory.all_handlers['friend_request_action']
        elif name == 'UsersList':
            return HandlerFactory.all_handlers['get_users_list']
        elif name == 'ComparisonWithFriends':
            return HandlerFactory.all_handlers['comparison_with_friends']
        elif name == 'UserFeed':
            return HandlerFactory.all_handlers['user_feed']
