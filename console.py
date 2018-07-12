#!/usr/bin/python3

import serial
import time
from datetime import datetime
import os
import logging
import paramiko
import traceback
from config import ConsoleConfig
from common import utc_str

class Console:
    def __init__(self):
        self.iteration = 0
        self.logfile = 'console.log' # FIXME: Make this per logging session
        if os.path.isfile(self.logfile):
            # Operate in current working directory
            target = "console_" + utc_str() + ".bak"
            logging.warn(self.logfile + " exists, backup as " + target)
            os.rename(self.logfile, target)

    def send(self, command, timeout=1):
        print("Implement send command: " + command)
        return ''

    def log(self, content):
        ''' Hacking way first - always append to same file '''
        with open(self.logfile, "a") as log:
            log.write("--- " + str(datetime.now()) + "  " + utc_str() + "  itr " + str(self.iteration) + " ---\n")
            log.write(content + "\n")

class SerialConsole(Console):
    def __init__(self, config):
        Console.__init__(self)
        self.port = config.path

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
        out = ser.read(size=8096).decode().strip('\n')
        ser.close()
        logging.debug("Serial output: " + out)
        self.log(out)
        return out

    def login(self, user, password):
        content = self.send("\r\n")
        if "~ #" in content:
            logging.info("Already Logged in!")
            return 1
        while True:
            if "~ #" not in content:
                logging.info("Logging in to system... " + user + " " + password)
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
        self.do_connect()

    def __exit__(self, type, value, traceback):
        self.do_close()

    def do_connect(self):
        if self.client.get_transport() is not None:
            if self.client.get_transport().is_active():
                return True

        try:
            self.client.connect(self.path, username=self.login, password=self.password)
        except Exception as e:
            logging.error("SSH connect failed: " + str(e))
            traceback.print_exc()
            self.do_close()
            return False

    def do_close(self):
        try:
            self.client.close()
        except:
            pass

    def send(self, command, timeout=1):
        if self.do_connect() == False:
            return ''

        out = ''
        try:
            # @TODO - Do reconnect on failed? Possible for connection to break
            logging.debug("Shell input: " + command)
            _, stdout, _ = self.client.exec_command(command, timeout=timeout)
            out = stdout.read().decode().strip('\n')
            # close MUST only happen after stdout is processed
            logging.debug("Shell output: " + out)
        except Exception as e:
            logging.error("SSH failed: " + str(e))
            traceback.print_exc()
            self.do_close()

        self.log(out)
        return out
