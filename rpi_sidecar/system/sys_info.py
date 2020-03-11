# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

import os
import sys
import time
from datetime import datetime
import psutil


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return "%sB" % n


class SysInfo:
    def __init__(self):
        pass

    def get_cpu_usage(self):
        av1, av2, av3 = os.getloadavg()
        return "Ld:%.1f %.1f %.1f " % (av1, av2, av3)

    def get_uptime(self):
        uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
        return "Up: %s" % (str(uptime).split('.')[0])

    def get_mem_usage(self):
        usage = psutil.virtual_memory()
        return "Mem: %s %.0f%%" \
            % (bytes2human(usage.used), 100 - usage.percent)

    def get_disk_usage(self, dir):
        usage = psutil.disk_usage(dir)
        return "SD:  %s %.0f%%" \
            % (bytes2human(usage.used), usage.percent)
