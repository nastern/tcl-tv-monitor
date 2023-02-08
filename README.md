# tcl-tv-monitor
A simple application to shut down your TCL tv when it receives a CEC shutdown signal running on a raspberry pi

## Setup
1. Clone this repository locally/onto your raspberry pi
2. Create a virtual enviroment inside the cloned folder

`python3 -m venv venv`
3. Activate your virtual enviroment

`source venn/bin/activate`
4. Install requirements.txt

`pip3 install -r requirements.txt`
5. Update the places in the code marked as #UPDATE with your own tv IP address, logging location.
    - Note: You will want to set a static IP address with your TV. See your home network setup for instructions
6. Add this script to your cron jobs to start automatically when the pi reboots

`crontab -e`

and add this line to the top replacing your venv version of python and main python files

`@reboot /bin/sleep 30; /home/admin/venv/bin/python3 /home/admin/tcl-tv-monitor/main.py &`
7. Reboot your pi and check that it starts automatically

`sudo reboot`

wait for reboot

`ps -aef | grep python3`


