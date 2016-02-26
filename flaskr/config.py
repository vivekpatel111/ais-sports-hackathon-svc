"""
This module acts as helper for loading values from config file
"""

#Imports
import json
import os
import logging


# path to config file
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
CONFIG_PATH = os.path.join(CURR_DIR, '..', 'config', 'config.json')

#Initialize logger
logger = logging.getLogger(__name__)


class ConfigParser(object):
    """
    Helper class for loading values from config
    """

    def __init__(self):
        """Reads the value from config and saves it """
        with open(CONFIG_PATH) as json_data_file:
            self.data = json.load(json_data_file)
        logger.info("Loaded config file successfully!")

    def get(self, key):
        """Returns the value for the given key in dictionary"""
        return self.data[key]