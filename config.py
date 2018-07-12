#!/usr/bin/python3

import json
import logging

from common import *

'''
Load configuration in json format
{
    "console" : {
        "type": "serial" | "ssh",
        "path": "/dev/ttyUSB0",
        "login": "root",
        "password": "pwd"
    }
    # Data refresh interval in sec
    "interval": 15
    # TODO: Graphing config
}
'''

class ConsoleConfig:
    def __init__(self):
        self.type = 'serial'
        self.path = '/dev/ttyUSB0'
        self.login = 'root'
        self.password = 'password'

class Config:
    def __init__(self, configFile):
        self.default()
        self.load(configFile)

    def default(self):
        self.console = ConsoleConfig()
        self.interval = 30

    def load(self, configFile):
        if not file_accessible(configFile, 'r'):
            logging.warn('config: ' + configFile + ' not found, using default')
            return

        with open(configFile) as f:
            data = json.load(f)

            if 'console' not in data:
                raise ValueError("No console config")

            if 'type' in data['console']:
                self.console.type = data['console']['type']
            if 'path' in data['console']:
                self.console.path = data['console']['path']
            if 'login' in data['console']:
                self.console.login = data['console']['login']
            if 'password' in data['console']:
                self.console.password = data['console']['password']

            if 'interval' in data:
                self.interval = data['interval']

            logging.info('Loaded config: ' + self.console.path + ', interval(s): ' + str(self.interval))