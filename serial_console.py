#!/usr/bin/python3

import serial
import time
import os
import logging

class SerialConsole:
    def __init__(self, port):
        self.out = ''
        self.port = port

    def send(self, command):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
            port=self.port,
            baudrate=115200,
            parity=serial.PARITY_ODD,
            stopbits=serial.STOPBITS_TWO,
            bytesize=serial.SEVENBITS,
            timeout=1
        )

        if "top" in command:
            ser.timeout = 10
        ser.open()
    
        time.sleep(1)
        cmd = command + "\r"
        if ser.inWaiting() > 0:
            ser.flushInput()

        ser.write(bytes(cmd, 'UTF-8'))
        self.out = ser.read(size=4028).decode()

        ser.close()
        return self.out

    def login(user, password):
        self.send("\x03\r\n")
        time.sleep(2)
        content = self.send("\r")
        if "~ #" in content:
            logging.info("Already Logged in!")
            return 1
        while True:
            if "~ #" not in content:
                logging.info("Logging in to system...\n")
                if "login" in content:
                    content = self.send(user + "\r")
                    content = self.send(password + "\r")
                else:
                    content = self.send("\r")
            else:
                logging.info("Login Complete!")
                return 1

        logging.error("Login Failed")
        return 0  # Failed