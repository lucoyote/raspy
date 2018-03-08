from __future__ import division
import requests
import timer
import socket
import struct
import threading

class RGBColor(object):
    def __init__(self, red, green, blue):
        self.Red = red
        self.Green = green
        self.Blue = blue
    
class HSBColor(object):
    def __init__(self, hue, saturation, brightness):
        self.Hue = hue
        self.Saturation = saturation
        self.Brightness = brightness 

class HSLColor(object):
    def __init__(self, hue, saturation, lightness):
        self.Hue = hue
        self.Saturation = saturation
        self.Lightness = lightness 


class neoPixelBus (object):
    """docstring for ClassName"""
    def __init__(self, sIp, Port=2390, NumberOfLeds=30):
        self.Ip = sIp
        self.UdpPort = Port
        self.UrlPlay = 'http://{}/play'.format(sIp)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpserver = (sIp, Port)
        self.leds = NumberOfLeds
        self.Sema = threading.Semaphore()
        self.interval = timer.IntervalTimer(1, self.SendStream)
        self.Array = []
        for i in range(self.leds * 3 + 2):
            self.Array.append(i)
        self.Array[0] = 1
        self.nrows = 0
        self.DataBuffer = []

    def PostCommand(self, sCommand):
        try:
            # self.StreamStop()
            r = requests.post(self.UrlPlay, data={'plain': sCommand})
            return (r.text == u'OK')
        except Exception:
            return False

    def Blank(self):
        sCommand = 'blank'
        return self.PostCommand(sCommand)

    def Blink(self, StartColor, EndColor, Repetitions, Frames):
        if isinstance(StartColor, RGBColor) and isinstance(EndColor, RGBColor):
            sCommand = 'blink rgb{},{},{} rgb{},{},{} t{} f{}'.format(
                       StartColor.Red, StartColor.Green, StartColor.Blue,
                       EndColor.Red, EndColor.Green, EndColor.Blue,
                       Repetitions, Frames)
            return self.PostCommand(sCommand)
        else:
            return False

    def Pulse(self, StartColor, EndColor, Repetitions, Frames):
        if isinstance(StartColor, RGBColor) and isinstance(EndColor, RGBColor):
            sCommand = 'pulse rgb{},{},{} rgb{},{},{} t{} f{}'.format(
                       StartColor.Red, StartColor.Green, StartColor.Blue,
                       EndColor.Red, EndColor.Green, EndColor.Blue,
                       Repetitions, Frames)
            return self.PostCommand(sCommand)
        else:
            return False

    def Hue(self, StartColor, EndColor, Repetitions, Frames):
        if isinstance(StartColor, RGBColor) and isinstance(EndColor, RGBColor):
            sCommand = 'hue rgb{},{},{} rgb{},{},{} t{} f{}'.format(
                       StartColor.Red, StartColor.Green, StartColor.Blue,
                       EndColor.Red, EndColor.Green, EndColor.Blue,
                       Repetitions, Frames)
            return self.PostCommand(sCommand)
        else:
            return False

    def Hue2(self, StartColor, EndColor, Repetitions, Frames):
        if isinstance(StartColor, RGBColor) and isinstance(EndColor, RGBColor):
            sCommand = 'hue2 rgb{},{},{} rgb{},{},{} t{} f{}'.format(
                       StartColor.Red, StartColor.Green, StartColor.Blue,
                       EndColor.Red, EndColor.Green, EndColor.Blue,
                       Repetitions, Frames)
            return self.PostCommand(sCommand)
        else:
            return False

    def HueHSL(self, StartColor, EndColor, Repetitions, Frames):
        if isinstance(StartColor, HSLColor) and isinstance(EndColor, HSLColor):
            sCommand = 'huehsl hsl{},{},{} hsl{},{},{} t{} f{}'.format(
                       StartColor.Hue, StartColor.Saturation,
                       StartColor.Lightness, EndColor.Hue,
                       EndColor.Saturation, EndColor.Lightness,
                       Repetitions, Frames)
            return self.PostCommand(sCommand)
        else:
            return False

    def HueHSB(self, StartColor, EndColor, Repetitions, Frames):
        if isinstance(StartColor, HSBColor) and isinstance(EndColor, HSBColor):
            sCommand = 'huehsb hsb{},{},{} hsb{},{},{} t{} f{}'.format(
                       StartColor.Hue, StartColor.Saturation,
                       StartColor.Brightness,
                       EndColor.Hue, EndColor.Saturation,
                       EndColor.Brightness,
                       Repetitions, Frames)
            return self.PostCommand(sCommand)
        else:
            return False

    def LoadBufferFromFile(self, sFileName, rowsize):
        bbuff = file(sFileName, 'rb').read()
        self.Sema.acquire()
        self.nrows = int(len(bbuff) / rowsize)
        self.DataBuffer = []
        sFormat = '{}B'.format(rowsize)
        for i in range(self.nrows):
            row = struct.unpack(sFormat, bbuff[rowsize * i:rowsize * (i + 1)])
            self.DataBuffer.append(row)
        self.Sema.release()

    def AppendBufferFromFile(self, sFileName, rowsize):
        bbuff = file(sFileName, 'rb').read()
        nowstoappend = int(len(bbuff) / rowsize)

        sFormat = '{}B'.format(rowsize)
        self.Sema.acquire()
        self.nrows += nowstoappend
        for i in range(nowstoappend):
            row = struct.unpack(sFormat, bbuff[rowsize * i:rowsize * (i + 1)])
            self.DataBuffer.append(row)
        self.Sema.release()

    def LoadBuffer_ScrollingRed(self):
        self.Sema.acquire()
        self.DataBuffer = []
        self.nrows = self.leds
        for i in range(self.nrows):
            row = []
            for j in range(self.leds * 3):
                if j == 3 * i:
                    row.append(255)
                else:
                    row.append(0)
            self.DataBuffer.append(row)
        self.Sema.release()

    def SendStream(self):
        self.Sema.acquire()
        if self.nrows > 0:
            if self.Index >= self.nrows:
                self.Index = 0
            self.Array[1: self.leds * 3 + 1] = self.DataBuffer[self.Index]
            self.Index = self.Index + 1
        self.Sema.release()

        message = bytearray(self.Array)
        self.sock.sendto(message, self.udpserver)

    def StreamStart(self, fps):
        if not self.interval.is_alive():
            self.interval.Interval = 1 / fps
            self.Sema.acquire()
            self.Index = 0
            self.Sema.release()
            self.interval = timer.IntervalTimer(1 / fps, self.SendStream)
            self.interval.start()

    def StreamStop(self):
        self.interval.stop()


