from __future__ import print_function
import paho.mqtt.client as mqtt


class mqtt_publisher():

    def __init__(self, Broker, Port, UserName, Password, ClientId="Raspby"):
        self.BROKER = Broker
        self.Port = Port
        self.CLIENT_ID = ClientId
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.username_pw_set(UserName, Password)
        self.Handlers = {}

    def Connect(self):
        print ("MQTT Connect")
        self.client.connect(self.BROKER, self.Port, 60)
        self.client.loop_start()

    def Disconnect(self):
        print ("MQTT Disconnect")
        self.client.loop_stop(True)
        self.client.disconnect()

    def Publish(self, sId, Value, Retain=True):
        print ("MQTT publish {}({})".format(sId, Value))
        self.client.publish(sId, Value, retain=Retain)

    def AddHandler(self, sToken, fHandler):
        self.Handlers[sToken] = fHandler

    def on_connect(self, lclient, userdata, flags, rc):
        print ("MQTT Connected")
        for key in self.Handlers.keys():
            print ("Subscribe " + key)
            lclient.subscribe(key)
            print ("Subscribed " + key)

    def on_message(self, client, userdata, message):
        print ("MQTT Message Received {} ({})".
               format(message.topic, message.payload))
        topic = message.topic
        if topic in self.Handlers:
            self.Handlers[topic](message)



