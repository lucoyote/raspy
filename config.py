import json
from SerialGate import SerialGate
from HttpRele import HttpRele

place_Config = {'Name': 'San Michele dei Mucchietti',
                'Address': 'Viale Rivi 32 Sassuolo',
                'Latitude': 44.50527, 
                'Longitude': 10.75054, 
                'Altitude': 189.241638184}

mqtt_Config = {'IP': '127.0.0.1',
               'Port': 1883,
               'UserName': 'lucoyote',
               'Password': '28091811',
               'ClientId': 'RaspberryCasa'}

mail_config = {'smtp': 'smtp.gmail.com',
               'Port': 587,
               'TLS': True,
               'UserName': 'lucmonti@gmail.com',
               'Password': '28091811',
               'Destination': 'luca@montionline.eu'}

router_config = {'Enabled': True,
                 'IP': '192.168.1.1',
                 'UserName': 'lucoyote',
                 'Password': 'Giallo2Sara@'}
        
DeviceConfig = [{'Name': 'Cancello', 'Type': SerialGate,'SerialPort': '/dev/serial0', 'MasterId': '1', 'SlaveId': '2'},
                {'Name': 'LuciEsterne','Type': HttpRele,'CommandURL': 'http://192.168.1.212/light', 'StateURL': 'http://192.168.1.212'}]


Config = {'Place': place_Config,
          'MQTT': mqtt_Config,
          'mail': mail_config,
          'router': router_config,
          'devices': DeviceConfig}

def SaveConfig (sFile, Configuration):
    with open(sFile, 'w') as outfile:
        json.dump(Config, outfile)

def LoadConfig (sFile):
    Configuration = None
    with open(sFile) as data_file:
        Configuration = json.load(data_file)
    return Configuration
    




#mqtt command:      Config['mqtt']['ClientId'] + "/" + DeviceConf1['Name'] + "/OnOff"
#mqtt state:        Config['mqtt']['ClientId'] + "/" + DeviceConf1['Name'] + "/State"
#mqtt timeronoff:   Config['mqtt']['ClientId'] + "/" + DeviceConf1['Name'] + "/TimerOnOff"
#mqtt TON:          Config['mqtt']['ClientId'] + "/" + DeviceConf1['Name'] + "/TON"
#mqtt StateAux:     Config['mqtt']['ClientId'] + "/" + DeviceConf1['Name'] + "/StateAux"
