# pip install requests[socks]
# tor --hash-password mypassword
# sudo nano /etc/tor/torrc
# HashedControlPassword <password>
# sudo systemctl restart tor.service

import requests
from stem import Signal # pip install stem
from stem.control import Controller
import time
import subprocess

command = ['systemctl', 'status', 'tor.service']
password = b'XXX\n' # sudo ?

proc = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
proc.stdin.write(password)
output, _ = proc.communicate()
print(output.decode())

controller = Controller.from_port(port=9051)
controller.authenticate(password="mypassword")

# change IP
controller.signal(Signal.NEWNYM)
time.sleep(controller.get_newnym_wait())

proxies = {"http": "socks5://127.0.0.1:9050","https": "socks5://127.0.0.1:9050"}

cIp = requests.get("http://httpbin.org/ip", proxies=proxies) 
print("New IP:{}".format(cIp.json()["origin"]))

controller.close()
