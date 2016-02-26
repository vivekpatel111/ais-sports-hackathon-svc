#!/usr/bin/env python

"""This module provides common errors that might be raised while calling
   tagging service. The module helps in providing better error messages
   to the user"""
# Imports


# Constants

SERVER_ERROR = 500
NOT_IMPLEMENTED_ERROR = 501
INITIALIZATION_ERROR = 502
AUTH_ERROR = 401

# Classes and Functions
class IncorrectRequestData(Exception):
    """This error gets raised when, for example, required keys are not present
    in the data sent on a post call to tagging service"""
    def __init__(self):
        self.message = 'Incorrect request data'
        self.solution = 'Validate your actual input against the schema of data'
        self.status_code = SERVER_ERROR

class CouldNotAuthenticate(Exception):
    """This error gets raised when the authentication of the request could not
       be performed"""
    def __init__(self):
        self.message = 'The request could not be authenticated'
        self.solution = 'Please contact service administrator'
        self.status_code = AUTH_ERROR

class FunctionalityNotImplemented(Exception):
    """This is a catch all exception for opaque API end points, where actual
    handling logic is not yet implemented"""
    def __init__(self):
        self.message = """This functionality is not yet implemented by the
                          service"""
        self.solution = 'Please contact service administrator'
        self.status_code = NOT_IMPLEMENTED_ERROR

class InitError(Exception):
    """This is a catch all exception for opaque API end points, where actual
    handling logic is not yet implemented"""
    def __init__(self, message):
        self.message = 'Unable to initialize model, the problem seems to be with:' + message
        self.solution = 'Good luck!'
        self.status_code = INITIALIZATION_ERROR

class UsernameAlreadyExists(Exception):
    def __init__(self, message):
        self.message = "username already exists. Please try another username"
        self.solution = "Try other username"
        self.status_code = None

class RegistrationError(Exception):
    def __init__(self, err_message):
        self.message = "Internal Error while registering the user. Please try again"
        self.error_message = err_message
        self.solution = "Please try again"
        self.status_code = None