import json
import requests
from timer import IntervalTimer

class HttpRele():
    """
    HTTP commanded rele

    Accept command with the follwing syntax:
    http://{$CommandUrl}?OnOff=$State,TimerOnOff=$EnableTimer,TON=$TimerValue
    
    where 
        $State is the rele command, 0 or 1
        $EnableTimer is the enabling of the automatic power off
        $TimerValue is the delay between on and off

    """
    def __init__(self, Name, StateUrl, CommandUrl):
        self.Name = Name
        self.CommandUrl = CommandUrl
        self.StateUrl = StateUrl
        self.__PollingThread = IntervalTimer(1, self.PollingFunction)
        self.OnOff = 0
        self.TimerOnOff =  0
        self.TON = 60
        self.__Requested_OnOff = 0
        self.__Requested_TimerOnOff = 0
        self.__Requested_TON = 60
        self.State = 0

    def Enable(self, EnableState):
        """
        Enable HTTP commands
        Every 1 second pulls the state of the rele, if something change in parameters, send one command packet
        and refresh state and values
        """
        if EnableState:
            if not self.__PollingThread.isAlive():
                 self.__PollingThread.start()
        else:
            self.__PollingThread.stop()

    def PollingFunction (self):
        """
        Polling functon, only internal use
        """
        if (self.OnOff != self.__Requested_OnOff or
            self.TimerOnOff != self.__Requested_TimerOnOff or
            self.TON != self.__Requested_TON):
                requests.post(self.CommandUrl,data={'OnOff': self.__Requested_TON,
                                                    'TimerOnOff': self.__Requested_TimerOnOff,
                                                    'TON': self.__Requested_TON})
                self.OnOff = self.__Requested_OnOff
                self.TimerOnOff = self.__Requested_TimerOnOff
                self.TON = self.__Requested_TON                
        else:        
            _State = requests.get(self.StateUrl).json()
            if _State['OnOff'] == 1:
                self.State = 1
            else:
                self.State = 0
        
    


    

    
## requests.get("http://192.168.1.212/").json()
## r = requests.post("http://192.168.1.212/light",data={'OnOff': 1, 'TimerOnOff': 1, 'TON': 60})