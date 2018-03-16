from config import Config
from Ephem import Home

from mqtt_httprele import mqtt_httprele
from mqtt_serial_gate import mqtt_serial_gate
from Logger import log

Devices ={}

def GateCommand(mqttmessage):
    if mqttmessage.payload == '1':
        if Home.isNightNow():
            log.info('Gate Open: Turn on External Lights')
            Devices['LuciEsterne'].OnOff = 1
            Devices['LuciEsterne'].TON = 120
            Devices['LuciEsterne'].OnTimerOff = 1
        else:
            log.info('Gate Open: It\'s day now,you don\'t need lights')


def Init():
    for _device in Config['devices']:
        if _device['Type'] == mqtt_serial_gate:
            Devices[_device['Name']] = mqtt_serial_gate(Config['MQTT'],_device)       
        elif _device['Type'] == mqtt_httprele:
            Devices[_device['Name']] = mqtt_httprele(Config['MQTT'],_device)
    
    Devices['Cancello'].AddHandler(Devices['Cancello'].mqtt_command, GateCommand)        
    Devices['LuciEsterne'].Enable(1)
 
def Main():
    pass

if __name__ == '__main__':
    try:
        Init()
        while(1):
            Main()
    except:
        Devices['LuciEsterne'].Enable (0)
    

    
    
