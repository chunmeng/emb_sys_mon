
#!/usr/bin/python3

####
# Small utils plot graph from csv data
# - Not really useful as the csv can easily to open in spreadsheet app with greater graphing feature
# required modules: matplotlib, numpy
# ref: https://stackoverflow.com/questions/24783530/python-realtime-plotting
####

import argparse
import logging
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from common import *

# @TODO: Make these args
type = 'cpu'
data_log = 'cpu_data_1527800617.csv'

# Expected data format as of now:
# cpu: ts,used,sirq
# mem: ts,memutil,memfree,slab,sunreclaim,kmalloc-2048,kmalloc-512

def cpu_graph(data):
    logging.info('Ploting CPU graph')
    # FIXME x with tick count currently, should use timestamp
    x = np.arange(len(data))
    fig = plt.figure()
    axl = fig.add_subplot(111)
    fig.suptitle('CPU over time')
    axl.set_xlabel('time')
    # @TODO Figure out how to move this to top left
    axl.set_ylabel('%')

    li_cpu, = axl.plot(x, data[:,1], 'b', label='cpu_used')
    li_sirq, = axl.plot(x, data[:,2], 'r', label='sirq')
    plt.legend(handles=[li_cpu,li_sirq], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

    axl.relim()
    axl.autoscale_view(True,True,True)
    #fig.canvas.draw()
    plt.ion()
    plt.show('''block=False''')

def mem_graph(data):
    logging.info('Ploting MEM graph')
    # FIXME x with tick count currently, should use timestamp
    x = np.arange(len(data))
    fig = plt.figure()
    axl = fig.add_subplot(111)
    fig.suptitle('MEM over time')
    axl.set_xlabel('time')
    axl.set_ylabel('kB')

    li_memfree, = axl.plot(x, data[:,2], 'b', label='memfree')
    li_slab, = axl.plot(x, data[:,3], 'r', label='slab')
    li_sunr, = axl.plot(x, data[:,4], 'g', label='sunreclaim')

    # Add right axis for %
    axr = axl.twinx()
    axr.set_ylabel('%')
    li_memutil, = axr.plot(x, data[:,1], 'y', linestyle='--', label='memutil')
    plt.legend(handles=[li_memfree,li_slab,li_sunr,li_memutil], bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

    # draw and show it
    axl.relim()
    axl.autoscale_view(True,True,True)
    #fig.canvas.draw()
    plt.ion()
    plt.show('''block=False''')

''' Apps start '''
set_logging(logging.DEBUG)

parser = argparse.ArgumentParser()
args_group = parser.add_argument_group()
args_group.add_argument("-i", "--input", required=True, help = "INPUT file contains raw data")
args_group.add_argument("-t", "--type", type=str, default='mem', help = "Type of INPUT file. mem | cpu")
# @TODO pass in data plotting config? (or just use gnuplot template)
args = parser.parse_args()

data_log = args.input.lstrip()
type = args.type
logging.info("Plot " + type + " from " + data_log)

# sanity check
if not file_accessible(data_log, 'r'):
    logging.error("Error reading " + data_log)
    dirname = os.path.dirname(__file__)
    data_log = os.path.join(dirname, data_log)

if not file_accessible(data_log, 'r'):
    logging.error("Error reading " + data_log)
    exit(1)

# Loads data
data = np.genfromtxt(data_log,  delimiter=',')

if type == 'mem':
    mem_graph(data)
elif type == 'cpu':
    cpu_graph(data)

logging.info('Completed')