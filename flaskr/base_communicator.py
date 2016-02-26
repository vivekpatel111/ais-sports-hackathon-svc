"""Base implementation for talking through REST. It expects the input
   data to be json serialized"""

# imports

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
        """Common functionality of getting ip address from request.
           Ignoring any security implications this might have for
           ip address spoofing etc.
           Note: Current method works when Gunicorn+Flask is used
           without any reverse proxy. Different method might be
           needed when reverse proxy is used"""
        return req.access_route[0]

    @abstractmethod
    def check_auth(self, input_data, req):
        """Common functionality of auth checking needed for all servlets"""
        if AUTH_ENABLED:
            if APP_NAME in input_data:
                app_name = input_data[APP_NAME]
            else:
                logger.error("Application name must be present")
                raise errors.IncorrectRequestData()
            ip_adr = self.get_ip(req)
            logger.debug("The application name is %s", app_name)
            logger.debug("The IP address of client is %s", ip_adr)
            auth_res = self.auth.check_auth(app_name, ip_adr)
            if not auth_res:
                logger.warn("Attempted unauthenticated call from %s", ip_adr)
            return auth_res
        else:
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
        """Common functionality of marshalling and creating response"""
        return Response(json.dumps(response),
                        status=OK_RESPONSE,
                        mimetype='application/json')

    @abstractmethod
    def invoke_fetch(self, request):
        """Concrete classes should provide invoke_fetch method"""
        pass

    @abstractmethod
    def invoke_insert(self, request):
        "Concrete classes should provide invoke_insert method"""
        pass
