#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import telnetlib
import re
import psutil
import os
import sys
import io
import smtplib
from config import Config

class MailClient():

    @staticmethod
    def FromConfig(MailConfiguration):
        _client = MailClient(smtpurl= MailConfiguration['smtp'],
                             smtport = MailConfiguration['Port'],
                             smtpTLS = MailConfiguration['TLS'],
                             smtpuser = MailConfiguration['UserName'],
                             smtpasswd = MailConfiguration['Password'])
        return _client
        


    def __init__ (self, smtpurl, smtport, smtpTLS, smtpuser,smtpasswd):
        self.server = smtplib.SMTP(smtpurl, smtport)
        if smtpTLS:
            self.server.starttls()
        self.UserName = smtpuser
        self.Password = smtpasswd
        
    def Send(self, Destination, Header, Message):
        self.server.login(self.UserName, self.Password)
        msg = 'Subject: {}\n\n{}'.format(Header, Message)
        From = self.UserName
        self.server.sendmail(From, Destination, msg)
        self.server.quit()
    
class SystemInformation():
    @staticmethod
    def isRaspberryPi():
        isRaspberry = False
        if os.name == 'posix':
            with io.open('/proc/cpuinfo', 'r') as cpuinfo:
                for line in cpuinfo:
                    if line.startswith('Hardware'):
                        value = line.strip().split(':', 1)[1]
                        if value in (
                                'BCM2708',
                                'BCM2709',
                                'BCM2835',
                                'BCM2836'
                            ):
                            isRaspberry = True
        return isRaspberry

    @staticmethod
    def getCPUtemperature():
        if SystemInformation.isRaspberryPi():
            res = os.popen('vcgencmd measure_temp').readline()
            return True, (res.replace('temp=','').replace("''C\n",''))
        else:
            return False, 0


    @staticmethod
    def cpu():
        return psutil.cpu_percent()

    @staticmethod
    def memory():
        memory = psutil.virtual_memory()
        return {'Avalaible': memory.available,
                'Total': memory.total,
                'Percent': memory.percent }

    @staticmethod
    def disk():
        disk = psutil.disk_usage('/')
        # Divide from Bytes -> KB -> MB -> GB
        available = round(disk.free/1024.0/1024.0/1024.0,1)
        total = round(disk.total/1024.0/1024.0/1024.0,1)
        return {'Avalaible': available,
                'Total': total,
                'Percent': disk.percent }
      
    @staticmethod
    def ExternalIP():
        try:
            tn = telnetlib.Telnet()
            tn.open("192.168.1.1")
            tn. read_until("password:")
            tn.write("Giallo2Sara@\r\n")
            tn.read_until("TP-LINK(conf)#")
            tn.write("wan show service atm\r\n")
            s = tn.read_until("TP-LINK(conf)#")
            # print s
            tn.close()
            grab = re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', s)
            return True,grab[0]
        except:
            return False,"0.0.0.0"

if __name__ == '__main__':
    print ('SystemInformation')
    print ('CPU: {}'.format(SystemInformation.cpu()))
    print ('Memory: Total {Total}, Avalaible {Avalaible}, Percent {Percent}%'.format(**SystemInformation.memory()))    
    print ('Disk:  Total {Total}, Avalaible {Avalaible}, Percent {Percent}%'.format(**SystemInformation.disk()))    
    IPValid, IP = SystemInformation.ExternalIP()
    if IPValid:
        print ('External IP: {}'.format(IP))
    else:
        print ('External IP: Valid address not found')

    ValidTemperature, Temperature = SystemInformation.getCPUtemperature()
    if ValidTemperature:
        print ('Temperature: {}°C'.format(Temperature))
    else:
        print ('Temperature: not avalaible, not a Raspberry')
    

