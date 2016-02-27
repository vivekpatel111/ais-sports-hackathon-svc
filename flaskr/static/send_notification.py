import requests
import json
import logging
import time

logger = logging.getLogger(__name__)


class GCMessage(object):
    def __init__(self):
        self.URL = "https://gcm-http.googleapis.com/gcm/send"
        self.auth_key = "AIzaSyCK63WUA6Pq_j2QfXyjKHp5k46ZceFmufM"
        self.headers = {'content-type': 'application/json',
                        'Authorization': 'key=' + self.auth_key}

    def post_request(self, payload):
        retry_count = 0
        while retry_count < 3:
            try:
                resp = requests.post(self.URL, data=json.dumps(payload),
                                     headers=self.headers)
                if resp.status_code == 200:
                    logger.info("Notification posted successfully to GMC")
                    return True
                else:
                    retry_count += 1
                    time.sleep(2)
                    logger.error("Error while posting notification to GMC")
            except Exception as e:
                retry_count += 1
                time.sleep(2)
                logger.error("Error while posting notification to GMC")
        return False


if __name__ == '__main__':
    test = GCMessage()
    data = {
        "to": "f8YS9MCITw0:APA91bF1FchjeEKVmk3-fwFf6b0U1V6-1rFb4ZBHPFcQjc6Y0Ny2S1fYKh23RAbP7hTAKujya60_DfE_jb63y_" +
              "-qIRhxsdf6owSv7MwVH6zz8PFsJmqCX6xr7vAWh4apv6E9eeYEszc6",
        "notification": {
            "title": "Friend request",
            "body": str("sample_user") + " sent you a friend request",
            "sound": "default"
        }
    }
    print test.post_request(data)
