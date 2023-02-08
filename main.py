import subprocess
import datetime
import time
import logging
from threading import Thread

from adb_shell.adb_device import AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', filename=f'/home/admin/python-cec/logs/logs-{current_time}.log', encoding='utf-8', level=logging.INFO)
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
        logging.info(f'Sending shutdown signal to {self.tv_ip_address}')
        android_tv.close()

    def start_monitor(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        status = ''
        while 'connected to' not in status:
            connect_process = subprocess.Popen(['adb', 'connect', '192.168.1.101:5555'], stdout=subprocess.PIPE)
            status = connect_process.stdout.readline().decode()
            time.sleep(1)

        logging.info(f'Connected to abd TV logs')

        adb_logcat_process = subprocess.Popen(['adb', 'logcat', '-T', current_time, '\*:D', '-e', 'messageOpcode:157'], stdout=subprocess.PIPE)

        while True:
            log_line = adb_logcat_process.stdout.readline().decode()
            if "messageOpcode:157" in log_line:
                logging.info(f'Recieved shutdown signal from CEC device')
                self.turn_off_tv()
            else:
                logging.info(f'Recieved a different line : {log_line}')



def main():
    monitor = Monitor()
    monitor.start_monitor()

if __name__ == '__main__':
    main()

