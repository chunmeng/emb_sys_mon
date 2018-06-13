

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
from data_reader import *
from data_writer import DataWriter
from serial_console import SerialConsole
from data_updater import DataUpdater

set_logging(logging.DEBUG)

serial = SerialConsole() # The serial console to acquire data source stream
# @TODO Login to console here

data_reader = DataReader(serial) # The parsing and aggregation of data into Stats
data_writer = DataWriter(os.getcwd()) # Output Stats data to file
figure = plt.figure()

du = DataUpdater(data_reader, data_writer, figure)
anim = FuncAnimation(figure, du, init_func=du.init,
                     interval=2000, blit=True)
plt.show()