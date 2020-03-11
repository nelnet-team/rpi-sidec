from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time
import asyncio
from wifi import wifi_status
from ip_interface import interface_info
from system import sys_info


class DisplayInfo:
    def __init__(self):
        self.serial = i2c(port=1, address=0x3C)
        self.device = ssd1306(self.serial, rotate=0)
        self.interval = 10
        self.wifi_state = ""
        self.wifi_ssid = ""
        self.ip_addr = ""
        self.ip_mask = ""
        self.if_stats = ""
        self.interface = "wlan0"
        self.cpu_usage = ""
        self.mem_usage = ""
        self.disk_usage = ""
        self.uptime = ""
        self.sys_info = sys_info.SysInfo()
        self.interface_info = interface_info.InterfaceInfo(self.interface)
        self.wifi_info = wifi_status.WifiStatus(self.interface)
        self.redraw = True

    def terminate(self):
        self._running = False

    def draw_interface(self):
        top = "{} {}".format(self.interface, self.wifi_ssid)
        status = "State: {}".format(self.wifi_state)
        ipaddr = "{}/{}".format(self.ip_addr, self.ip_mask)
        with canvas(self.device) as draw:
            print("{}\n{}\n{}\n{}".format(top, status, ipaddr, self.if_stats))
            draw.text((0, 0), top, fill="white")
            draw.text((0, 16), status, fill="white")
            draw.text((0, 24), ipaddr, fill="white")
            draw.text((0, 32), self.if_stats, fill="white")

    def draw_sysinfo(self):
        with canvas(self.device) as draw:
            draw.text((0, 0), self.cpu_usage, fill="white")
            draw.text((0, 8), self.uptime, fill="white")
            draw.text((0, 16), self.mem_usage, fill="white")
            draw.text((0, 24), self.disk_usage, fill="white")

    async def display_interface(self):
        while True:
            try:
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
                    print("Testing if redraw needed")
                    self.draw_interface()
                    self.redraw = False

                await asyncio.sleep(self.interval)

            except asyncio.CancelledError:
                self.redraw = True
                return ()

    async def display_sys_info(self):
        while True:
            try:
                self.cpu_usage = self.sys_info.get_cpu_usage()
                self.uptime = self.sys_info.get_uptime()
                self.mem_usage = self.sys_info.get_mem_usage()
                self.disk_usage = self.sys_info.get_disk_usage('/')
                self.draw_sysinfo()
                print("Finished drawing sys_info")
                await asyncio.sleep(self.interval)

            except asyncio.CancelledError:
                return ()
