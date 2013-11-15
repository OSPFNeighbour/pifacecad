#!/usr/bin/env python3
# requires `lldpctl` to be installed

import sys
import subprocess
import os
from time import sleep
import pifacecad

UPDATE_INTERVAL = 30  # 10 sec

GET_LLDP_HOSTNAME_CMD = "lldpctl | grep SysName | awk '{print $2}'"
GET_LLDP_PORT_CMD = "lldpctl | grep PortDescr | awk '{print $2}'"


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_lldp_hostname():
    return run_cmd(GET_LLDP_HOSTNAME_CMD)[:-1]

def get_lldp_port():
    return run_cmd(GET_LLDP_PORT_CMD)[:-1]


def wait_for_neighbour():
    hostname = ""
    while len(hostname) <= 0:
        sleep(1)
        hostname = get_lldp_hostname()


def show_lldpinfo():
    while True:
        cad.lcd.clear()
        cad.lcd.write(get_lldp_hostname()+"\n"+get_lldp_port())
        sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    # test for lldpd
    try:
        subprocess.call(["lldpctl"], stdout=open('/dev/null'))
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            print(
                "lldpctl was not found, install with "
                "`sudo apt-get install lldpd`")
            sys.exit(1)
        else:
            raise  # Something else went wrong while trying to run `lldpd`
            
    cad = pifacecad.PiFaceCAD()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()

    if "clear" in sys.argv:
        cad.lcd.clear()
        cad.lcd.display_off()
        cad.lcd.backlight_off()
    else:
        cad.lcd.backlight_on()
        cad.lcd.write("Waiting for LLDP..")
        wait_for_neighbour()
        show_lldpinfo()