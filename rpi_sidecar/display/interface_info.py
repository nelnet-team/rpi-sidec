from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
import netifaces as iface
import wifi_status


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

    def report(self):
        report = "{}/{}".format(self.get_ip(), self.get_mask_slash())
        return report


class InterfaceInfo:
    def __init__(self):
        self._running = True
        self.interface = "wlan0"
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial, rotate=0)
        self.interval = 10

    def terminate(self):
        self._running = False

    def interface_info(self):
        nexttime = 0
        while self._running:
            timestamp = time.time()
            if timestamp >= nexttime:
                nexttime = timestamp + self.interval
                ip = IP(self.interface)
                ip_report = ip.report()
                wifi = wifi_status.WifiStatus(self.interface)
                wifi_report = wifi.report()
                with canvas(self.device) as draw:
                    draw.text((0, 8), self.interface, fill="blue")
                    draw.text((0, 16), ip_report, fill="yellow")
                    draw.text((0, 24), wifi_report, fill="yellow")


if __name__ == '__main__':
    intobj = InterfaceInfo()
    intobj.interface_info()
