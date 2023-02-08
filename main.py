import argparse
import logging
import os
import subprocess
import time
from threading import Thread

import cec
from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner


class Monitor:
    def __init__(self) -> None:
        super().__init__()
        self.tv_ip_address = '192.168.1.101'
        self.adb_key_filepath = '/home/admin/.android/adbkey'
        self.adb_port = 5555

    def turn_off_tv(self):
        # Load the public and private keys
        with open(self.adb_key_filepath) as f:
            priv = f.read()
        with open(self.adb_key_filepath + '.pub') as f:
            pub = f.read()
        signer = PythonRSASigner(pub, priv)

        # Connect
        android_tv = AdbDeviceTcp(self.tv_ip_address, self.adb_port, default_transport_timeout_s=9.)
        android_tv.connect(rsa_keys=[signer], auth_timeout_s=0.1)

        # Send a shell command
        tv_off_command_key = '26'
        android_tv.shell('input keyevent %s' % tv_off_command_key)

        android_tv.close()

def main():
    monitor = Monitor()

    import datetime

    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    subprocess.Popen(['adb', 'connect', '192.168.1.101:5555'])
    adb_logcat_process = subprocess.Popen(['adb', 'logcat', '-T', current_time], stdout=subprocess.PIPE)

    while True:
        log_line = adb_logcat_process.stdout.readline().decode().strip()
        if "HdmiCecLocalDevice: ---onMessage--fuli---messageOpcode:157" in log_line:
            monitor.turn_off_tv()

if __name__ == '__main__':
    main()

