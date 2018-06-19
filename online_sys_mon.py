

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

from common import *
from config import Config
from data_reader import *
from data_writer import DataWriter
from serial_console import SerialConsole
from data_updater import DataUpdater

def read_fw_version(console):
    fw_version = serial.send('version')
    logging.info('System running FW: ' + filter_nonprintable(fw_version[9:26]))
    return fw_version[9:26]

''' Apps start '''
set_logging(logging.INFO)

# @TODO Make config path input arg
config = Config(os.getcwd() + '/config.json')

serial = SerialConsole(config.console.path) # The serial console to acquire data source stream
serial.login(user=config.console.login, password=config.console.password)

ver = read_fw_version(serial)

# Use this for test mode without serial
# data_reader = DataReaderStub()

data_reader = DataReader(serial) # The parsing and aggregation of data into Stats
data_writer = DataWriter(os.getcwd()) # Output Stats data to file
figure = plt.figure()

fig = plt.gcf()
fig.canvas.set_window_title('Mem, CPU over time - ' + ver)

du = DataUpdater(data_reader, data_writer, figure)
# The interval timer is restarted after each call to __call__ returns
# So the total time for each iteration is interval + data processing time (sleeps)
anim = FuncAnimation(figure, du, init_func=du.init,
                     interval=config.interval * 1000, blit=True)
plt.show()
