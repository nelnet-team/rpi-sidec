import subprocess
import re


class WifiStatus:
    def __init__(self, interface):
        self.interface = interface
        self.cmd = "/sbin/wpa_cli"

    def get_state(self):
        cmd = self.cmd
        completed = subprocess.run(
            [cmd, "-i", self.interface, "status"], capture_output=True)
        status = str(completed.stdout)
        rawstate = re.search("wpa_state=(\w+)", status)
        if rawstate == None:
            state = "UNKNOWN"
        else:
            state = rawstate.group(1)
        return state

    def get_ssid(self):
        cmd = self.cmd
        completed = subprocess.run(
            [cmd, "-i", self.interface, "status"], capture_output=True)
        status = str(completed.stdout)
        rawstate = re.search("[^b]ssid=(\w+)", status)
        if rawstate == None:
            state = "UNKNOWN"
        else:
            state = rawstate.group(1)
        return state

    def report(self):
        report = "{} {}".format(self.get_ssid(), self.get_state())
        return report


if __name__ == '__main__':
    wifiobj = WifiStatus("wlan0")
    wifiobj.interface_info
