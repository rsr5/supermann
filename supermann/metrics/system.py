"""System metrics"""

from __future__ import absolute_import, unicode_literals

import os

import psutil


def cpu(self, event):
    """Returns the systems total CPU and memory usage"""
    self.riemann.event(
        service='system:cpu:percent',
        metric_f=psutil.cpu_percent(interval=None))


def mem(self, event):
    mem = psutil.virtual_memory()
    self.riemann.event(service='system:mem:percent', metric_f=mem.percent)
    self.riemann.event(service='system:mem:total', metric_f=mem.total)
    self.riemann.event(service='system:mem:free', metric_f=mem.free)
    self.riemann.event(service='system:mem:cached', metric_f=mem.cached)
    self.riemann.event(service='system:mem:buffers', metric_f=mem.buffers)


def swap(self, event):
    swap = psutil.swap_memory()
    self.riemann.event(service='system:swap:percent', metric_f=swap.percent)
    self.riemann.event(service='system:swap:absolute', metric_f=swap.used)


def load(self, event):
    load1, load5, load15 = os.getloadavg()
    self.riemann.event(service='system:load:1min', metric_f=load1)
    self.riemann.event(service='system:load:5min', metric_f=load5)
    self.riemann.event(service='system:load:15min', metric_f=load15)


def load_scaled(self, event):
    """Load average divided by number of CPUs"""
    load1 = os.getloadavg()[0] / psutil.cpu_count()
    self.riemann.event(service='system:load_scaled:1min', metric_f=load1)


def uptime(self, event):
    with open('/proc/uptime', 'r') as f:
        uptime, idle = map(float, f.read().strip().split())
    self.riemann.event(service='system:uptime', metric_f=uptime)
