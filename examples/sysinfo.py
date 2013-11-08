#!/usr/bin/env python3
import sys
import subprocess
from time import sleep
import pifacecad

UPDATE_INTERVAL = 10  # 10 sec
GET_IP_CMD = "hostname --all-ip-addresses"
GET_TEMP_CMD = "/opt/vc/bin/vcgencmd measure_temp"
TOTAL_MEM_CMD = "free | grep 'Mem' | awk '{print $2}'"
USED_MEM_CMD = "free | grep '\-\/+' | awk '{print $3}'"
CPU_LOAD_CMD = "uptime | awk '{print $9}' | sed s/,/""/g"
HOSTNAME_CMD = "hostname"
FREE_DISK_CMD = "df -h | grep rootfs | awk '{print $5}'"

cpu_symbol = pifacecad.LCDBitmap( [0x0, 0x1f, 0x11, 0x15, 0x11, 0x1f, 0x0, 0x0] )
disk_symbol = pifacecad.LCDBitmap( [0x0, 0x1c, 0x1e, 0x1e, 0x1e, 0x1e, 0x0, 0x0] )
temperature_symbol = pifacecad.LCDBitmap( [0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0] )
memory_symbol = pifacecad.LCDBitmap( [0xe, 0x1f, 0xe, 0x1f, 0xe, 0x1f, 0xe, 0x0] )

temp_symbol_index, memory_symbol_index, cpu_symbol_index, disk_symbol_index = 0, 1, 2, 3

def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True).decode('utf-8')

def get_cpu_load():
    return run_cmd(CPU_LOAD_CMD)[:-1]

def get_disk_usage():
    return run_cmd(FREE_DISK_CMD)[:-1]

def get_my_ip():
    return run_cmd(GET_IP_CMD)[:-1]

def get_hostname():
    return run_cmd(HOSTNAME_CMD)[:-1]

def get_my_temp():
    return run_cmd(GET_TEMP_CMD)[5:9]


def get_my_free_mem():
    total_mem = int(run_cmd(TOTAL_MEM_CMD))
    used_mem = int(run_cmd(USED_MEM_CMD))
    mem_perc = used_mem / total_mem
    return "{:.1%}".format(mem_perc)


def wait_for_ip():
    ip = ""
    while len(ip) <= 0:
        sleep(1)
        ip = get_my_ip()


def show_sysinfo():
    while True:
        cad.lcd.clear()
        cad.lcd.write("IP:{}\n".format(get_my_ip()))
        cad.lcd.write_custom_bitmap(cpu_symbol_index)
        cad.lcd.write(":{} ".format(get_cpu_load()))
        cad.lcd.write_custom_bitmap(memory_symbol_index)
        cad.lcd.write(":{}".format(get_my_free_mem()))

        sleep(UPDATE_INTERVAL)

        cad.lcd.clear()
        cad.lcd.write(format(get_hostname())+"\n")
        cad.lcd.write_custom_bitmap(temp_symbol_index)
        cad.lcd.write(":{}C ".format(get_my_temp()))        
        cad.lcd.write_custom_bitmap(disk_symbol_index)
        cad.lcd.write(":{}".format(get_disk_usage()))

        sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    cad = pifacecad.PiFaceCAD()
    cad.lcd.blink_off()
    cad.lcd.cursor_off()

    if "clear" in sys.argv:
        cad.lcd.clear()
        cad.lcd.display_off()
        cad.lcd.backlight_off()
    else:
        cad.lcd.store_custom_bitmap(temp_symbol_index, temperature_symbol)
        cad.lcd.store_custom_bitmap(memory_symbol_index, memory_symbol)
        cad.lcd.store_custom_bitmap(cpu_symbol_index, cpu_symbol)
        cad.lcd.store_custom_bitmap(disk_symbol_index, disk_symbol)
        cad.lcd.backlight_on()
        cad.lcd.write("Waiting for IP..")
        wait_for_ip()
        show_sysinfo()