#!/usr/bin/python3

import random
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
        self.stats.memfree = self.stats.memavail - 5
        self.stats.slab = random.randint(20, 100)
        self.stats.slab_unreclaim =  self.stats.slab * 0.8

    def read_slabinfo(self):
        ''' Read slabinfo into stats '''        
        self.stats.km2k = random.randint(20, 60)
        self.stats.km512 = random.randint(10, 50)
    
    def read_cpuinfo(self):
        ''' Read cpuinfo into stats '''
        self.stats.used_cpu = round(random.random() * 100, 2)
        self.stats.sirq = round(random.random() * 100, 2)

    def get_stats(self):
        self.read_meminfo()
        self.read_slabinfo()
        self.read_cpuinfo()
        return self.stats

class DataReader(DataReaderStub):
    def __init__(self, console):
        DataReaderStub.__init__(self)
