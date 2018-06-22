

#!/usr/bin/python3

####
# Program to monitor the embedded resources via serial console and update data/graph in online mode.
# required modules: matplotlib, numpy
# ref: https://stackoverflow.com/questions/24783530/python-realtime-plotting
####

import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

import common
from config import Config
from data_reader import DataReaderStub,DataReader
from data_writer import DataWriter
from console import SerialConsole,SshConsole
from data_updater import DataUpdater

def read_fw_version(client):
    import re
    read_out = client.send('version')
    ver = ''
    if read_out != '':
        # Test: read_out = '0.1.1.0-build5'
        # 2 groups matching - will always return a tuple of 2 items or empty
        groups = re.findall('(\d+\.(?:\d+\.)*\d+)([-]\w+)?', read_out)
        if len(groups) != 0:
            # print(groups)
            part1,part2 = groups[0]
            ver = part1 + part2
            logging.info('System running FW: ' + ver)
    return ver

''' Apps start '''
common.set_logging(logging.INFO)

# @TODO Make config path input arg
config = Config(os.getcwd() + '/config.json')

client = None
if config.console.type == 'serial':
    client = SerialConsole(config.console) # The serial console to acquire data source stream
    client.login(user=config.console.login, password=config.console.password)
elif config.console.type == 'ssh':
    client = SshConsole(config.console)

ver = '0.0.0.0'
if client is None:
    data_reader = DataReaderStub()
else:
    ver = read_fw_version(client)
    data_reader = DataReader(client) # The parsing and aggregation of data into Stats

data_writer = DataWriter(os.getcwd()) # Output Stats data to file
figure = plt.figure('Mem, CPU over time - ' + ver)

du = DataUpdater(data_reader, data_writer, figure)
# The interval timer is restarted after each call to __call__ returns
# So the total time for each iteration is interval + data processing time (sleeps)
anim = FuncAnimation(figure, du, init_func=du.init,
                     interval=config.interval * 1000, blit=True)
plt.show()
