#!/usr/bin/python3

####
# Small utils to export existing logs with cpu, meminfo, slabinfo into 2 separate data csv file
# The logs was captured with:
# watch -n 60 'slabinfo kmalloc && cat /proc/meminfo && top -n 2 | grep CPU'
####
import argparse
import logging
import os
import re
from common import *
from stats import Stats

# working dir
path = os.getcwd()

# @TODO Make these args later
file_ts = utc_str()
cpu_log = '/cpu_data_' + file_ts + '.csv'
mem_log = '/mem_data_' + file_ts + '.csv'

set_logging(logging.DEBUG)

# Looks for Every 60s: ... 2018-05-18 14:48:54
header = 'Every 60s:'
header_ts_regex = '\d{4}[-/]\d{2}[-/]\d{2} \d{2}[:]\d{2}[:]\d{2}'

def get_meminfo(content, tag):
    matches = re.search(tag + ':(.*) kB', content)
    if matches is None:
        return False,0

    value = int(matches.group(1).lstrip())
    # print("Found %s -> %s" % (matches.groups(), stats.memfree))
    return True,value

def get_slabinfo(content, tag):
    # @TODO Handle 2 types of slabinfo
    # cat /proc/slabinfo -> object count is at 2
    # kmalloc-2048        8205  14512   2048   16    8 : tunables    0    0    0 : slabdata    907    907      0

    # slabinfo kmalloc -> object count is at 1
    # kmalloc-2048              2398    2048     4.9M       137/6/15   16 3   3  98 *
    idx = 1
    matches = re.match(tag, content)
    if matches is None:
        return False,0

    tokens = str.split(content)
    value = int(tokens[idx])
    # print("Found %s -> %s" % (tokens, stats.km2k))
    return True,value

'''
This takes only 2nd reading due to the log is being read line by line
'''
def get_cpuinfo(content):
    matches = re.match('CPU:', content)
    if matches is None:
        return (False,0.0,0.0)

    # "CPU:  0.0% usr  0.0% sys  0.0% nic 95.6% idle  0.0% io  0.0% irq  4.3% sirq"
    lines = content.split("usr")
    if (len(lines) != 2):
        return (False, 0.0, 0.0)

    matches = re.search('nic(.*)% idle', lines[1])
    idle = str(matches.group(1)).lstrip()
    used_cpu = round(float(100-float(idle)),2)

    matches = re.search('irq(.*)% sirq',lines[1])
    sirq = float(str(matches.group(1)).lstrip())
    return (True,used_cpu,sirq)

''' parse for data '''
def parse_data(content, stats):
    # logging.info("Parsing " + filter_nonprintable(line))
    found,value = get_meminfo(content, 'MemTotal')
    if found:
        stats.memtotal = value
        return found

    found,value = get_meminfo(content, 'MemAvailable')
    if found:
        stats.memavail = value
        return found

    found,value = get_meminfo(content, 'MemFree')
    if found:
        stats.memfree = value
        return found

    found,value = get_meminfo(content, 'Slab')
    if found:
        stats.slab = value
        return found

    found,value = get_meminfo(content, 'SUnreclaim')
    if found:
        stats.slab_unreclaim = value
        return found

    found,value = get_slabinfo(content, 'kmalloc-2048')
    if found:
        stats.km2k = value
        return found

    found,value = get_slabinfo(content, 'kmalloc-512')
    if found:
        stats.km512 = value
        return found

    found,used,sirq = get_cpuinfo(content)
    if found:
        stats.used_cpu = used
        stats.sirq = sirq
        return found

    return False

def create_logs():
    logging.info("Creating logs with header")
    filename = path + mem_log
    with open(filename, "w") as myfile:
        line = "ts,memutil,memfree,slab,sunreclaim,kmalloc-2048,kmalloc-512\n"
        myfile.write(line)

    filename = path + cpu_log
    with open(filename, "w") as myfile:
        line = "ts,used,sirq\n"
        myfile.write(line)

def write_mem(stats):
    filename = path + mem_log
    with open(filename, "a") as myfile:
        line = stats.ts + "," + str(stats.calc_memutil()) + "," + str(stats.memfree) + "," + str(stats.slab) + "," + str(stats.slab_unreclaim) + "," + str(stats.km2k) + "," + str(stats.km512) + "\n"
        myfile.write(line)

def write_cpu(stats):
    filename = path + cpu_log
    with open(filename, "a") as myfile:
        line = stats.ts + "," + str(stats.used_cpu) + "," + str(stats.sirq) + "\n"
        myfile.write(line)

def main():
    parser = argparse.ArgumentParser()
    args_group = parser.add_argument_group()
    args_group.add_argument("-i", "--input", required=True, help = "INPUT file contains raw data")
    args = parser.parse_args()

    # App start
    input_log = args.input
    logging.info("Exporting data from " + input_log)

    # sanity check
    if not file_accessible(input_log, 'rb'):
        logging.error("Error reading " + input_log)
        exit(1)

    create_logs()
    # processing statemachine
    with open(input_log, 'rb') as fin:
        first_section = True
        stats = Stats()

        for line in fin:
            line = line.decode(errors='ignore')
            is_header = re.search(header, line)
            if is_header:
                if not first_section:
                    # if end of a section, flush data to file
                    write_mem(stats)
                    write_cpu(stats)

                # mark start, reset all data variables
                stats = Stats()
                first_section = False
                # parse datetime as new section (assume always exist)
                stats.ts = re.compile(header_ts_regex).search(line).group(0)
            else: # parse other data content
                parse_data(line, stats)

    # Write last block data
    write_mem(stats)
    write_cpu(stats)

    # @TODO Handle incomplete data?

    logging.info("Export completed")

if __name__ == "__main__":
    main()