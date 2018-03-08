from mqtt_publisher import mqtt_publisher
from SerialGate import SerialGate

class mqtt_serial_gate (mqtt_publisher, SerialGate) :
    def __init__(self, BrokerConfig, SerialGateConfig):

        mqtt_publisher.__init__(self, 
                                Broker = BrokerConfig['IP'], 
                                Port = BrokerConfig['Port'], 
                                UserName = BrokerConfig['UserName'], 
                                Password = BrokerConfig['Password'], 
                                ClientId = BrokerConfig['ClientId'])
        SerialGate.__init__(self, 
                            Name = SerialGateConfig['Name'],
                            SerialPort = SerialGateConfig['SerialPort'],
                            MasterId = SerialGateConfig['MasterId'],
                            SlaveId = SerialGateConfig['SlaveId'])

        mqtt_path = BrokerConfig['ClientId'] + "/" + SerialGateConfig['Name']
        self.mqtt_all = mqtt_path + "/#"
        self.mqtt_command = mqtt_path + "/OnOff"
        self.mqtt_state = mqtt_path + "/State"
        self.mqtt_timeronoff = mqtt_path + "/TimerOnOff"
        self.mqtt_TON = mqtt_path + "/TON"
        self.mqtt_StateAux = mqtt_path + "/StateAux "

        self.Connect()
        self.AddHandler(self.mqtt_command, self.OnMqttCommand)
        self.AddHandler(self.mqtt_TON, self.OnMqtt_TON)

    def OnMqttCommand (self, mqttmessage):
        if mqttmessage.payload == 1:
            self.OpenDoor()

    
    def OnMqtt_TON(self, mqttmessage):
        try:
            self.TON = int(mqttmessage.payload)
        except:
            self.TON = 2


    
    
