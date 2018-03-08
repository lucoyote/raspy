import serial
import time
import thread
import threading



class PowerLineDevice():
    def __init__(self, SerialPort):
        self.ser = serial.Serial(SerialPort, 9600)
        self.ser.timeout = 0
        self.lock = threading.Lock()

    def close(self):
        self.Stop_Thread()
        self.ser.close()

    def Start_Receive(self):
        self.Reading = True
        self.lock.acquire()
        thread.start_new_thread(self.ReceiveThread, ())

    def Stop_Thread(self):
        self.Reading = False
        self.lock.acquire()
        self.lock.release()

    def ReceiveThread(self):
        PacketStart = 0
        stringa = ''
        while(self.Reading):
            time.sleep(0.1)
            ch = self.ser.read()
            if ch == '{':
                PacketStart = 1
            if PacketStart == 1:
                stringa += ch
                if ch == '}':
                    self.Received(stringa)
                    PacketStart = 0
                    stringa = ''
        self.lock.release()

    def Send(self, Packet):
        string = '{{{}}}'.format(Packet)
        bytepacket = bytearray(string, 'utf-8')
        self.ser.write(bytepacket)

    def Received(self, Packet):
        pass
        

