import json
from mqtt_httprele import mqtt_httprele
from mqtt_serial_gate import mqtt_serial_gate

place_Config = {'Name': 'San Michele dei Mucchietti',
                'Address': 'Viale Rivi 32 Sassuolo',
                'Latitude': 44.50527, 
                'Longitude': 10.75054, 
                'Altitude': 189.241638184}

mqtt_Config = {'IP': 'www.montionline.eu',
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

DeviceConfig = [{'Name': 'Cancello', 'Type': mqtt_serial_gate,'SerialPort': 'COM3', 'MasterId': '1', 'SlaveId': '2'},
                {'Name': 'LuciEsterne','Type': mqtt_httprele,'CommandUrl': 'http://192.168.1.212/light', 'StateUrl': 'http://192.168.1.212'}]


Config = {'Place': place_Config,
          'MQTT': mqtt_Config,
          'mail': mail_config,
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
