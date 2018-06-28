#!/usr/bin/python3

import logging
import random
import re
import time
from common import *
from stats import Stats


'''
' Stub class for testing without real data source
' Generate random input
'''
class DataReaderStub:
    def __init__(self):
        self.stats = Stats()
    
    def read_meminfo(self):
        ''' Read meminfo into stats '''
        self.stats.memtotal = 100
        self.stats.memavail = random.randint(40, 90)
        self.stats.memfree = self.stats.memavail - random.randint(0, 5)
        self.stats.slab = random.randint(20, 100)
        self.stats.slab_unreclaim =  round(self.stats.slab * 0.8, 2)

    def read_slabinfo(self):
        ''' Read slabinfo into stats '''        
        self.stats.km2k = random.randint(20, 60)
        self.stats.km512 = random.randint(10, 50)
    
    def read_cpuinfo(self):
        ''' Read cpuinfo into stats '''
        self.stats.used_cpu = round(random.random() * 100, 2)
        self.stats.sirq = round(random.random() * 100, 2)

    def get_stats(self):
        self.stats = Stats()  # Clean stats
        self.stats.ts = utc_str()
        self.read_meminfo()
        self.read_slabinfo()
        self.read_cpuinfo()
        return self.stats

class DataReader(DataReaderStub):
    def __init__(self, console):
        self.console = console
        DataReaderStub.__init__(self)

    def parse_meminfo(self, content, tag):
        matches = re.search(tag + ':(.*) kB', content)
        if matches is None:
            return False,0

        value = int(matches.group(1).lstrip())
        # print("Found %s -> %s" % (matches.groups(), stats.memfree))
        return True,value

    def read_meminfo(self):
        logging.info('Reading mem stats ...')
        content = self.console.send("cat /proc/meminfo")
        exist,val = self.parse_meminfo(content, tag='MemTotal')
        if exist: self.stats.memtotal = val
        exist,val = self.parse_meminfo(content, tag='MemAvailable')
        if exist: self.stats.memavail = val
        exist,val = self.parse_meminfo(content, tag='MemFree')
        if exist: self.stats.memfree = val
        exist,val = self.parse_meminfo(content, tag='Slab')
        if exist: self.stats.slab = val
        exist,val = self.parse_meminfo(content, tag='SUnreclaim')
        if exist: self.stats.slab_unreclaim = val

        # handle meminfo without MemAvailable
        if self.stats.memfree == 0:
            _,buf = self.parse_meminfo(content, 'Buffers')
            _,cache = self.parse_meminfo(content, 'Cached')
            _,shmem = self.parse_meminfo(content, 'Shmem')

            self.stats.memavail = int((self.stats.memfree + buf + cache)-shmem)

        logging.info('   ... Done')

    def parse_slabinfo(self, content, tag):
        matches = re.findall(tag + '\s+(\d+)', content)
        if len(matches) == 0:
            return False,0

        value = int(matches[0])
        # print("Found %s -> %s" % (matches.groups(), stats.memfree))
        return True,value

    def read_slabinfo(self):
        logging.info('Reading slab stats ...')
        content = self.console.send("slabinfo kmalloc")
        exist,val = self.parse_slabinfo(content, tag='kmalloc-2048')
        if exist: self.stats.km2k = val
        exist,val = self.parse_slabinfo(content, tag='kmalloc-512')
        if exist: self.stats.km512 = val

        logging.info('   ... Done')

    def read_cpuinfo(self):
        logging.info('Reading cpu stats ...')
        sum = 0
        sum_sirq = 0
        sample = 2
        for num in range(0,sample):
            # top command requires at least 6s timeout, the console will block until timeout
            output = self.console.send("top -n 2 | grep CPU", timeout=6)
            lines = output.split("usr")
            if (len(lines) < 2): break
            # output = "CPU:  0.0% usr  0.0% sys  0.0% nic 95.6% idle  0.0% io  0.0% irq  4.3% sirq"
            matches = re.search('nic(.*)% idle',lines[2])
            idle = str(matches.group(1).lstrip())
            used_cpu = float(100-float(idle))
            sum = float(sum + used_cpu)

            matches = re.search('irq(.*)% sirq',lines[2])
            sirq = float(str(matches.group(1)).lstrip())
            sum_sirq = float(sum_sirq + sirq)

            logging.debug("Sample: " + str(num) + " " + idle + " " + str(round(used_cpu,2)) + " " + str(round(sum,2)) + " " + str(sirq))

        avg = float(sum/sample)
        avg_sirq = float(sum_sirq/sample)
        self.stats.used_cpu = round(avg,2)
        self.stats.sirq = round(avg_sirq,2)
        logging.debug("CPU avg: " + str(self.stats.used_cpu) + " " + str(self.stats.sirq))

        logging.info('   ... Done')