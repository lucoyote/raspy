from __future__ import print_function
from Logger import log
import paho.mqtt.client as mqtt
from threading import Thread

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
        log.info("MQTT Connect")
        self.client.connect(self.BROKER, self.Port, 60)
        self.client.loop_start()

    def Disconnect(self):
        log.info ("MQTT Disconnect")
        self.client.loop_stop(True)
        self.client.disconnect()

    def Publish(self, sId, Value, Retain=True):
        log.info ("MQTT publish {}({})".format(sId, Value))
        self.client.publish(sId, Value, retain=Retain)

    def AddHandler(self, sToken, fHandler):
        if sToken not in self.Handlers:
            self.Handlers[sToken] = []
        self.Handlers[sToken].append(fHandler)

    def on_connect(self, lclient, userdata, flags, rc):
        log.info ("MQTT Connected")
        for key in self.Handlers.keys():
            log.info ("Subscribe " + key)
            self.client.subscribe(key)
            log.info ("Subscribed " + key)

    def on_message(self, client, userdata, message):
        log.info ("MQTT Message Received {} ({})".
                  format(message.topic, message.payload))
        topic = message.topic
        if topic in self.Handlers:
            for _handler in self.Handlers[topic]:
                worker = Thread(target=_handler, args=(message,))
                worker.start()
                



