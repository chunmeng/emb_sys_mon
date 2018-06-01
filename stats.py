#!/usr/bin/python3

####
# Container for parsed data
####
class Stats:
    def __init__(self):
        self.ts = ''
        self.memtotal = 0
        self.memfree = 0
        self.memavail = 0
        self.slab = 0
        self.slab_unreclaim = 0
        self.memavail = 0
        self.km2k = 0
        self.km512 = 0
        self.used_cpu = 0.0
        self.sirq = 0.0

    def calc_memutil(self):
        if (self.memtotal == 0):
            return 0.0
        memused = (self.memtotal - self.memavail)
        memutil = float((memused/self.memtotal)*100)
        return round(memutil,2)