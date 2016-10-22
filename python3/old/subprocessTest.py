#!/usr/bin/python3

import subprocess
import time

cmd='python /home/pi/BerniHeizung/relais.py'
sub=subprocess.Popen(cmd.split(), shell=False)
time.sleep(10)
sub.kill()


