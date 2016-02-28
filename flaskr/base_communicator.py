import auth
import json
from flask import Response
import logging
from abc import ABCMeta, abstractmethod
import errors
import urllib
import config

# globals
AUTH_CONFIG = 'auth-enabled'
APP_NAME = 'application'
CONFIG = config.ConfigParser()
AUTH_ENABLED = CONFIG.get(AUTH_CONFIG)
logger = logging.getLogger(__name__)
OK_RESPONSE = 200


# classes


class BaseCommunicator:
    ___metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        """On init, simply initialize auth flow"""
        self.auth = auth.AuthHelper()

    @abstractmethod
    def get_ip(self, req):
        return req.access_route[0]

    @abstractmethod
    def check_auth(self, input_data, req):
        # TODO
        return True

    @abstractmethod
    def get_request_data(self, req):
        """Common functionality of unmarshalling input data needed for all"""
        raw_data = req.get_data()
        try:
            str_data = urllib.unquote_plus(raw_data).decode('utf-8')
        except Exception, decode_err:
            logger.error("Error in decoding request data %s", str(decode_err))
            raise errors.IncorrectRequestData()
        # Convert the data to json.
        try:
            input_data = json.loads(str_data)
        except ValueError, json_err:
            logger.error("Error in converting input data to json %s",
                         str(json_err))
            raise errors.IncorrectRequestData()
        return input_data

    @abstractmethod
    def get_response(self, response):
        return Response(json.dumps(response),
                        status=OK_RESPONSE,
                        mimetype='application/json')

    @abstractmethod
    def invoke_fetch(self, request):
        pass

    @abstractmethod
    def invoke_insert(self, request):
        pass
