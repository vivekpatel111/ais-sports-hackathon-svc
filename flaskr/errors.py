#!/usr/bin/env python

SERVER_ERROR = 500
NOT_IMPLEMENTED_ERROR = 501
INITIALIZATION_ERROR = 502
AUTH_ERROR = 401

# Classes and Functions
class IncorrectRequestData(Exception):
    def __init__(self):
        self.message = 'Incorrect request data'
        self.solution = 'Validate your actual input against the schema of data'
        self.status_code = SERVER_ERROR

class CouldNotAuthenticate(Exception):
    def __init__(self):
        self.message = 'The request could not be authenticated'
        self.solution = 'Please contact service administrator'
        self.status_code = AUTH_ERROR

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