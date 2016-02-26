RESP_APP_KEY = "application"
RESP_ERROR_MSG_KEY = "errorMsg"
RESP_ERROR_BOOL_KEY = "error"
RESP_RES_KEY = "response"
RESP_PAGE_KEY = "page"
RESP_LIM_KEY = "limit"
RESP_USER_KEY = "username"


class SvcResponseObjects(object):
    response_object = {
        RESP_APP_KEY: "Sports-Hack",
        RESP_ERROR_MSG_KEY: None,
        RESP_ERROR_BOOL_KEY: False,
        RESP_RES_KEY: {},
        RESP_PAGE_KEY: None,
        RESP_LIM_KEY: None,
        RESP_USER_KEY: None
    }

    @staticmethod
    def get_svc_resp_object():
        return SvcResponseObjects.response_object
