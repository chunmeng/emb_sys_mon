#!/usr/bin/python3

import serial
import time
import os
import logging
import paramiko
import traceback
from config import ConsoleConfig

class Console:
    def __init__(self):
        self.out = ''

    def send(self, command, timeout=1):
        print("Implement send command: " + command)

class SerialConsole(Console):
    def __init__(self, config):
        self.port = config.path
        Console.__init__(self)

    def send(self, command, timeout=1):
        self.out = ''
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
        self.out = ser.read(size=4028).decode().strip('\n')
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

class SshConsole(Console):
    def __init__(self, config):
        Console.__init__(self)
        self.path = config.path
        self.login = config.login
        self.password = config.password
        self.client = paramiko.SSHClient()
        # client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def send(self, command, timeout=1):
        self.out = ''
        try:
            self.client.connect(self.path, username=self.login, password=self.password)
            logging.debug("Shell input: " + command)
            _, stdout, _ = self.client.exec_command(command, timeout=timeout)
            self.out = stdout.read().decode().strip('\n')
            # close MUST only happen after stdout is processed
            logging.debug("Shell output: " + self.out)
        except Exception as e:
            logging.error("SSH connection failed: " + str(e))
            traceback.print_exc()

        try:
            self.client.close()
        except:
            pass
        return self.out
