#!/usr/bin/python3

import random
import re
import time
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
        # @TODO: Mark timestamp
        self.read_meminfo()
        self.read_slabinfo()
        self.read_cpuinfo()
        return self.stats

class DataReader(DataReaderStub):
    def __init__(self, console):
        self.console = console
        DataReaderStub.__init__(self)

    def parse_meminfo(content, tag):
        matches = re.search(tag + ':(.*) kB', content)
        if matches is None:
            return False,0

        value = int(matches.group(1).lstrip())
        # print("Found %s -> %s" % (matches.groups(), stats.memfree))
        return True,value

    def read_meminfo(self):
        self.console.send("\x03\r\n")
        time.sleep(2)
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