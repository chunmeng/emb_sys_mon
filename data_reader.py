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

    def set_iteration(self, itr=0):
        self.stats.it = itr
        self.stats.ts = utc_str()

    def get_stats(self, itr=0):
        self.stats = Stats()  # Clean stats
        self.set_iteration(itr)
        self.read_meminfo()
        self.read_slabinfo()
        self.read_cpuinfo()
        return self.stats

class DataReader(DataReaderStub):
    mem_command = 'cat /proc/meminfo'
    cpu_command = 'top -n 2'
    slab_command = 'slabinfo kmalloc'

    def __init__(self, console):
        self.console = console
        DataReaderStub.__init__(self)

    def set_iteration(self, itr=0):
        self.stats.it = itr
        self.stats.ts = utc_str()
        self.console.iteration = itr

    def parse_meminfo(self, content, tag):
        matches = re.search(tag + ':(.*) kB', content)
        if matches is None:
            return False,0

        value = int(matches.group(1).lstrip())
        # print("Found %s -> %s" % (matches.groups(), stats.memfree))
        return True,value

    def read_meminfo(self):
        logging.info('Reading mem stats ...')
        content = self.console.send(self.mem_command)
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
        content = self.console.send(self.slab_command)
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
            output = self.console.send(self.cpu_command, timeout=6)
            valid,idle,sirq = parse_top(output)
            if not valid: break
            used_cpu = float(100-idle)
            sum = float(sum + used_cpu)
            sum_sirq = float(sum_sirq + sirq)

            logging.debug("Sample: " + str(num) + " " + str(idle) + " " + str(round(used_cpu,2)) + " " + str(round(sum,2)) + " " + str(sirq))

        avg = float(sum/sample)
        avg_sirq = float(sum_sirq/sample)
        self.stats.used_cpu = round(avg,2)
        self.stats.sirq = round(avg_sirq,2)
        logging.debug("CPU avg: " + str(self.stats.used_cpu) + " " + str(self.stats.sirq))

        logging.info('   ... Done')