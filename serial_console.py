#!/usr/bin/python3

import serial
import time
import os
import re

class SerialConsole:
    def __init__(self):
        self.out = ''

    def send(self, command_str):
        serial_obj = serial.Serial()
        serial_obj.baudrate = 115200
        serial_obj.port = '/dev/ttyUSB0'
        serial_obj.timeout = 1
        
        if "top" in command_str:
            serial_obj.timeout = 10
        serial_obj.open()
    
        time.sleep(1)
        #if serial_obj.isOpen():
            #print('Port: ' + serial_obj.portstr + " " + command_str)
            #print("Command: " + command_str)
        cmd = command_str + "\r"
        #print("Port: " + serial_obj.portstr + "Cmd: " + cmd)
        if serial_obj.inWaiting() > 0:
            serial_obj.flushInput()

        serial_obj.write(bytes(cmd, 'UTF-8'))
        self.out = serial_obj.read(size=4028).decode()
        #print(msg)
        #serial_obj.write("\x03\r\n")
        serial_obj.close()
        return self.out

