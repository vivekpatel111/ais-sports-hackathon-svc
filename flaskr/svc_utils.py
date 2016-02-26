import copy
import json
from flask import Response

from constants import response_objects
from constants.response_objects import SvcResponseObjects

OK_RESPONSE = 200


def get_response_from_dict(response):
    """Common functionality of marshalling and creating response"""
    return Response(json.dumps(response),
                    status=OK_RESPONSE,
                    mimetype='application/json')


def get_sample_response(err_b, err_m, response, username=None):
    resp = copy.deepcopy(SvcResponseObjects.get_svc_resp_object())
    resp[response_objects.RESP_ERROR_BOOL_KEY] = err_b
    resp[response_objects.RESP_ERROR_MSG_KEY] = err_m
    resp[response_objects.RESP_RES_KEY] = response
    resp[response_objects.RESP_USER_KEY] = username
    return resp
