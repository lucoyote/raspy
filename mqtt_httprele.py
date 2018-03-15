from mqtt_publisher import mqtt_publisher
from HttpRele import HttpRele

class mqtt_httprele (mqtt_publisher, HttpRele) :
    def __init__(self, BrokerConfig, HTTPReleConfig):

        mqtt_publisher.__init__(self, 
                                Broker = BrokerConfig['IP'], 
                                Port = BrokerConfig['Port'], 
                                UserName = BrokerConfig['UserName'], 
                                Password = BrokerConfig['Password'], 
                                ClientId = BrokerConfig['ClientId'])
        
        HttpRele.__init__(self,
                          Name = HTTPReleConfig['Name'],
                          StateUrl = HTTPReleConfig['StateUrl'],
                          CommandUrl = HTTPReleConfig['CommandUrl'])

        mqtt_path = BrokerConfig['ClientId'] + "/" + HTTPReleConfig['Name']
        self.mqtt_all = mqtt_path + "/#"
        self.mqtt_command = mqtt_path + "/OnOff"
        self.mqtt_state = mqtt_path + "/State"
        self.mqtt_timeronoff = mqtt_path + "/TimerOnOff"
        self.mqtt_TON = mqtt_path + "/TON"
        self.mqtt_StateAux = mqtt_path + "/StateAux "

        self.Connect()
        self.AddHandler(self.mqtt_command, self.OnMqttCommand)
        self.AddHandler(self.mqtt_TON, self.OnMqtt_TON)
        self.AddHandler(self.mqtt_timeronoff, self.OnMqttTimerOnOff)
        
        

    def OnMqttCommand (self, mqttmessage):
        try:
            self.OnOff = int(mqttmessage.payload)
        except:
            self.OnOff = 0
    
    def OnMqtt_TON(self, mqttmessage):
        try:
            self.TON = int(mqttmessage.payload)
        except:
            self.TON = 2

    def OnMqttTimerOnOff (self, mqttmessage):
        try:
            self.OnTimerOff = int(mqttmessage.payload)
        except:
            self.OnTimerOff = 0
    
        


    
    
