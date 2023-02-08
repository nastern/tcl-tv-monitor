import subprocess
import datetime
import time
from threading import Thread

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

    def start_monitor(self):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        status = ''
        while 'connected to' not in status:
            connect_process = subprocess.Popen(['adb', 'connect', '192.168.1.101:5555'], stdout=subprocess.PIPE)
            status = connect_process.stdout.readline().decode()
            time.sleep(1)

        print('Connected to the tv logs')

        adb_logcat_process = subprocess.Popen(['adb', 'logcat', '-T', current_time], stdout=subprocess.PIPE)

        # Read 100 lines at a time
        BATCH_SIZE = 100

        while True:
            log_batch = adb_logcat_process.stdout.read(BATCH_SIZE).decode()
            log_lines = log_batch.strip().split('\n')

            if any("HdmiCecLocalDevice: ---onMessage--fuli---messageOpcode:157" in line for line in log_lines):
                self.turn_off_tv()



def main():
    monitor = Monitor()
    monitor.start_monitor()

if __name__ == '__main__':
    main()

