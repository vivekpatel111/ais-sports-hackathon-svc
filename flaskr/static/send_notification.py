import requests
import json
import logging
import time

logger = logging.getLogger(__name__)


class GCMessage(object):
    def __init__(self):
        self.URL = "https://gcm-http.googleapis.com/gcm/send"
        self.auth_key = ""
        self.headers = {'content-type': 'application/json',
                        'Authorization': 'key=' + self.auth_key}

    def post_request(self, payload):
        return True
        # retry_count = 0
        # while retry_count < 3:
        #     try:
        #         resp = requests.post(self.URL, data=json.dumps(payload),
        #                              headers=headers)
        #         if resp.status_code == 200:
        #             logger.info("Notification posted successfully to GMC")
        #             return True
        #         else:
        #             retry_count += 1
        #             time.sleep(2)
        #             logger.error("Error while posting notification to GMC")
        #     except Exception as e:
        #         retry_count += 1
        #         time.sleep(2)
        #         logger.error("Error while posting notification to GMC")
        # return False
