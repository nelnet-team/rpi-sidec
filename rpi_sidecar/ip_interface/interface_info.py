import netifaces as iface
import psutil


class IP:
    def __init__(self, interface):
        self.interface = interface

    def get_ip(self):
        ip = iface.ifaddresses(self.interface)[iface.AF_INET][0]['addr']
        return ip

    def get_mask_dotted(self):
        nm = iface.ifaddresses(self.interface)[iface.AF_INET][0]['netmask']
        return nm

    def get_mask_slash(self):
        mask_dotted = self.get_mask_dotted()
        mask_slash = str(sum(bin(int(x)).count('1')
                             for x in mask_dotted.split('.')))
        return mask_slash


class InterfaceInfo:
    def __init__(self, interface):
        self.interface = interface
        self.ip_info = IP(self.interface)

    def get_ip(self):
        return (self.ip_info.get_ip())

    def get_mask_dotted(self):
        return (self.ip_info.get_mask_dotted())

    def get_mask_slash(self):
        return (self.ip_info.get_mask_slash())

    def bytes2human(self, n):
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

    def get_stats(self):
        stat = psutil.net_io_counters(pernic=True)[self.interface]
        return "Tx: %s, Rx: %s" % \
            (self.bytes2human(stat.bytes_sent),
             self.bytes2human(stat.bytes_recv))
