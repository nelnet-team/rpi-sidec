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
        self.ip_report = ""
        self.wif_report = ""
        self.interface = "wlan0"
        self.interface_info = interface_info.InterfaceInfo(self.interface)
        self.wif_info = wifi_status.WifiStatus(self.interface)

    def terminate(self):
        self._running = False

    def draw_info(self):
        with canvas(self.device) as draw:
            draw.text((0, 8), self.interface)
            draw.text((0, 16), self.ip_report)
            draw.text((0, 24), self.wifi_report
                      )

        def display_info(self):
        nexttime = 0
        while self._running:
            timestamp = time.time()
            if timestamp >= nexttime:
                nexttime = timestamp + self.interval
                self.ip_report = self.interface_info.interface_info()
