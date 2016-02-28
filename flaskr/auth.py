import json
import logging

GLOBAL_APP_IP_MAPPING = [{'application' : 'sports', 'ip' : 'localhost'}]

logger = logging.getLogger(__name__)

# Classes


class AuthHelper:
    def __init__(self):
        pass

    def get_data(self, app, ip_add):
        """Converts the app and ip data into a json object to be sent to
        validator URL"""
        return json.dumps({'application': app, 'ipAddress': ip_add})

    def check_auth(self, app_name, ip_add):
        data = self.get_data(app_name, ip_add)
        logger.debug("The data for app-ip authentication is : %s", data)
        for apps_ips in GLOBAL_APP_IP_MAPPING:
            if apps_ips['application'] == app_name and apps_ips['ip'] == ip_add:
                return True
        logger.debug("App-IP authentication failed for : %s", data)
        return False