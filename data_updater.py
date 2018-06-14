#!/usr/bin/python3

import logging
from matplotlib.lines import Line2D

from data_reader import DataReader
from data_writer import DataWriter

class DataUpdater:
    def __init__(self, reader, writer, figure):
        self.__initData()

        # Setup plots
        self.figure = figure
        self.ax_cpu = figure.add_subplot(2, 1, 1)
        self.ax_mem_kb = figure.add_subplot(2, 1, 2)
        self.ax_mem_pct = self.ax_mem_kb.twinx()

        self.ax_cpu.set_title("CPU")
        self.ax_mem_kb.set_title("Memory")

        # 2 different ways to do the same thing
        self.li_cpu = Line2D(self.t, self.cpu_util, color='b', label='cpu_util')
        self.li_sirq = Line2D(self.t, self.cpu_sirq, color='r', label='sirq')

        self.ax_cpu.add_line(self.li_cpu)
        self.ax_cpu.add_line(self.li_sirq)
        
        self.li_memutil, = self.ax_mem_pct.plot(self.t, self.mem_util, 'b', label='mem_util')
        self.li_memavail, = self.ax_mem_kb.plot(self.t, self.mem_avail, 'r', label='mem_avail')
        self.li_memslab, = self.ax_mem_kb.plot(self.t, self.mem_slab, 'g--', label='slab')
        self.li_memslab_unreclaim, = self.ax_mem_kb.plot(self.t, self.mem_slab_unreclaim, 'y--', label='slab_unreclaim')

        self.lines = [self.li_cpu, self.li_sirq, self.li_memutil, self.li_memavail, self.li_memslab, self.li_memslab_unreclaim]

        # Setup data source and sink
        self.reader = reader
        self.writer = writer

    def __initData(self):
        # Data points
        self.t = []
        self.cpu_util = []
        self.cpu_sirq = []
        self.mem_util = []
        self.mem_avail = []
        self.mem_slab = []
        self.mem_slab_unreclaim = []

    def __appendData(self, stats):
        self.t += [stats.it]
        self.cpu_util += [stats.used_cpu]
        self.cpu_sirq += [stats.sirq]
        self.mem_util += [stats.memutil]
        self.mem_avail += [stats.memavail]
        self.mem_slab += [stats.slab]
        self.mem_slab_unreclaim += [stats.slab_unreclaim]

    def init(self):
        logging.info("Initialize lines...")
        for l in self.lines:
            l.set_data([], [])
        return self.lines

    def __call__(self, i):
        logging.info("Iteration " + str(i))

        # Read and write data
        stats = self.reader.get_stats()
        stats.it = i
        self.writer.append(stats)

        # Update lines data
        self.__appendData(stats)

        # @TODO These line to data relationship should be mapped
        self.li_cpu.set_data(self.t, self.cpu_util)
        self.li_sirq.set_data(self.t, self.cpu_sirq)

        self.li_memutil.set_data(self.t, self.mem_util)
        self.li_memavail.set_data(self.t, self.mem_avail)
        self.li_memslab.set_data(self.t, self.mem_slab)
        self.li_memslab_unreclaim.set_data(self.t, self.mem_slab_unreclaim)

        self.ax_cpu.relim()
        self.ax_cpu.autoscale_view(True,True,True)

        self.ax_mem_pct.relim()
        self.ax_mem_pct.autoscale_view(True,True,True)
        self.ax_mem_kb.relim()
        self.ax_mem_kb.autoscale_view(True,True,True)
        self.figure.canvas.draw()

        return self.lines