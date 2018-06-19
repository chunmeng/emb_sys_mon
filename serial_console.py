#!/usr/bin/python3

import serial
import time
import os
import logging

class SerialConsole:
    def __init__(self, port):
        self.out = ''
        self.port = port

    def send(self, command, timeout=1):
        # configure the serial connections (the parameters differs on the device you are connecting to)
        ser = serial.Serial(
            port=self.port,
            baudrate=115200
        )
        ser.timeout = timeout

        ser.isOpen()

        time.sleep(1)
        cmd = command + "\r"
        if ser.inWaiting() > 0:
            ser.flushInput()

        logging.debug("Serial input: " + cmd)
        ser.write(bytes(cmd, 'UTF-8'))
        self.out = ser.read(size=4028).decode()

        ser.close()
        logging.debug("Serial output: " + self.out)
        return self.out

    def login(self, user, password):
        content = self.send("\r\n")
        if "~ #" in content:
            logging.info("Already Logged in!")
            return 1
        while True:
            if "~ #" not in content:
                logging.info("Logging in to system...")
                if "login" in content:
                    content = self.send(user)
                    content = self.send(password)
                else:
                    content = self.send("\r\n")
            else:
                logging.info("Login Complete!")
                return 1

        # Never reach
        logging.error("Login Failed")
        return 0  # Failed