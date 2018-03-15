from config import Config
from Ephem import Home

from mqtt_httprele import mqtt_httprele
from mqtt_serial_gate import mqtt_serial_gate


Devices =[]

def Init():
    for _device in Config['devices']:
        if _device['Type'] == mqtt_serial_gate:
            Devices.append(mqtt_serial_gate(Config['MQTT'],_device))
        elif _device['Type'] == mqtt_httprele:
            Devices.append(mqtt_httprele(Config['MQTT'],_device))


def Main():
    pass

if __name__ == '__main__':
    Init()
    while(1):
        Main()

    
    
