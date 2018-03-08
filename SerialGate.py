from PowerLineDevice import PowerLineDevice
from Logger import Logger
import time


class SerialGate(PowerLineDevice):

    def __init__(self, Name, SerialPort, MasterId, SlaveId, Ton=2):
        PowerLineDevice.__init__(self, SerialPort)    
        self.Name = Name
        self.MasterId = MasterId
        self.SlaveId = SlaveId
        self.DoorOpen = 0
        self.PulseActive = 0
        self.TON = Ton
        self.log = Logger(name= Name)

    def Received(self, Packet):
        arr = bytearray(Packet, 'utf-8')

        if chr(arr[3]) == self.MasterId:
            if chr(arr[5]) == 'D':
                if chr(arr[7]) == '1':
                    self.DoorOpen = 1
                else:
                    self.DoorOpen = 0
                self.log.info ("Door Open: {}".format(self.DoorOpen))
            else:
                if chr(arr[5]) == 'P':
                    if chr(arr[7]) == '1':
                        self.PulseActive = 1
                    else:
                        self.PulseActive = 0
                    self.log.info ("Pulse Active: {}".format(self.PulseActive))


    def OpenDoor(self):
        self.Start_Receive()
        T0 = time.time()
        CommandReceived = 0
        while CommandReceived  == 0 and (time.time() - T0) < 30:
            sCommand = '{}_{}_P_{}'.format(self.MasterId, self.SlaveId, self.TON)
            self.Send(sCommand)
            self.log.info  ("Sent {}".format(sCommand))
            T1 = time.time()
            while time.time() - T1 < self.TON + 1.0  and self.PulseActive == 0:
               time.sleep(0.1)
            while self.PulseActive == 1:
                time.sleep(0.1)
                CommandReceived = 1
            
        if CommandReceived == 0:
            self.log.info ("TIMEOUT")

    
            
