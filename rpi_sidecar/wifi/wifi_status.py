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
        elif rawstate.group(1) == "COMPLETED":
            state = "CONNECTED"
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
