from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
from wifi import wifi_status
from ip_interface import interface_info


class DisplayInfo:
    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial, rotate=0)
        self._running = True
        self.interval = 10
        self.wifi_state = ""
        self.wifi_ssid = ""
        self.ip_addr = ""
        self.ip_mask = ""
        self.if_stats = ""
        self.interface = "wlan0"
        self.interface_info = interface_info.InterfaceInfo(self.interface)
        self.wifi_info = wifi_status.WifiStatus(self.interface)
        self.redraw = True

    def terminate(self):
        self._running = False

    def draw_info(self):
        top = "{} {}".format(self.interface, self.wifi_ssid)
        status = "State: {}".format(self.wifi_state)
        ipaddr = "{}/{}".format(self.ip_addr, self.ip_mask)
        with canvas(self.device) as draw:
            print("{}\n{}\n{}\n{}".format(top, status, ipaddr, self.if_stats))
            draw.text((0, 0), top, fill="white")
            draw.text((0, 16), status, fill="white")
            draw.text((0, 24), ipaddr, fill="white")
            draw.text((0, 32), self.if_stats, fill="white")

    def display_interface(self):
        nexttime = 0
        while self._running:
            timestamp = time.time()
            if timestamp >= nexttime:
                nexttime = timestamp + self.interval

                ip_addr = self.interface_info.get_ip()
                if ip_addr != self.ip_addr:
                    self.redraw = True
                    self.ip_addr = ip_addr

                ip_mask = self.interface_info.get_mask_slash()
                if ip_mask != self.ip_mask:
                    self.redraw = True
                    self.ip_mask = ip_mask

                if_stats = self.interface_info.get_stats()
                if if_stats != self.if_stats:
                    self.redraw = True
                    self.if_stats = if_stats

                wifi_state = self.wifi_info.get_state()
                if wifi_state != self.wifi_state:
                    self.redraw = True
                    self.wifi_state = wifi_state

                wifi_ssid = self.wifi_info.get_ssid()
                if wifi_ssid != self.wifi_ssid:
                    self.redraw = True
                    self.wifi_ssid = wifi_ssid

                if self.redraw:
                    self.draw_info()
                    self.redraw = False
