#!/usr/bin/python3

import logging

from common import *

class DataWriter:
    def __init__(self, path):
        self.file_ts = utc_str()
        self.cpu_log = path + '/cpu_data_' + self.file_ts + '.csv'
        self.mem_log = path + '/mem_data_' + self.file_ts + '.csv'

        self.create_logs()

    def append(self, stats):
        self.append_cpu(stats)
        self.append_mem(stats)

    def append_cpu(self, stats):
        with open(self.cpu_log, "a") as myfile:
            line = str(stats.it) + "," + stats.ts + "," + str(stats.used_cpu) + "," + str(stats.sirq) + "\n"
            myfile.write(line)

    def append_mem(self, stats):
        with open(self.mem_log, "a") as myfile:
            line = str(stats.it) + "," + stats.ts + "," + str(stats.calc_memutil()) + "," + str(stats.memfree) + "," + str(stats.memavail) + "," + str(stats.slab) + "," + str(stats.slab_unreclaim) + "," + str(stats.km2k) + "," + str(stats.km512) + "\n"
            myfile.write(line)

    def create_logs(self):
        logging.info("Creating logs with header...")
        with open(self.mem_log, "w") as myfile:
            line = "it,ts,memutil,memfree,memavail,slab,sunreclaim,kmalloc-2048,kmalloc-512\n"
            myfile.write(line)

        with open(self.cpu_log, "w") as myfile:
            line = "it,ts,used,sirq\n"
            myfile.write(line)