#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from snipsTools import SnipsConfigParser
from hermes_python.hermes import Hermes
from hermes_python.ontology import *
import io
import time
import sys
from threading import Thread
import RPi.GPIO as GPIO
import subprocess
import os
from nanpy import ArduinoApi
from nanpy import SerialManager

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class RelaySwitch(object):

    def __init__(self):
        try:
            self.config = SnipsConfigParser.read_configuration_file(CONFIG_INI)
        except :
            print 'No "config.ini" found!'
            sys.exit(1)
        
        
        self.mqtt_host = self.config.get('secret',{"mqtt_host":"localhost"}).get('mqtt_host','localhost')
        self.mqtt_port = self.config.get('secret',{"mqtt_port":"1883"}).get('mqtt_port','1883')
        self.mqtt_addr = "{}:{}".format(self.mqtt_host, self.mqtt_port)

        self.site_id = self.config.get('secret',{"site_id":"default"}).get('site_id','default')
        
        
        self.start_blocking()

    
    # -> extraction of slots value
    def extractHouseRoom(self, intent_message, default_value):
        #if intent_message.slots.house_room:
        #    return intent_message.slots.house_room.first()
        return default_value

    def extractDevice(self, intent_message, default_value):
        #if intent_message.slots.device:
        #    return intent_message.slots.device.first()
        return default_value

    # -> action callbacks
    def turnOnRelay(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        connection=SerialManager(device='/dev/ttyACM0')
        a=ArduinoApi(connection=connection)
        bulb=10
        a.pinMode(bulb,a.OUTPUT)
        for i in range(0,200):
              a.analogWrite(bulb,100)
    
        hermes.publish_end_session(intent_message.session_id, "light is on ")

    def turnOffRelay(self, hermes, intent_message):
        print '[Received] intent: {}'.format(intent_message.intent.intent_name)
        connection=SerialManager(device='/dev/ttyACM0')
        a=ArduinoApi(connection=connection)
        bulb=10
        a.pinMode(bulb,a.OUTPUT)
        for i in range(0,200):
              a.analogWrite(bulb,0)
    
        hermes.publish_end_session(intent_message.session_id, "")

    def master_intent_callback(self, hermes, intent_message):
        if self.site_id != intent_message.site_id:
            print "[Return] Site Id unmatch"
            return

        if intent_message.intent.intent_name == 'relayTurnOn':
            self.turnOnRelay(hermes, intent_message)
        if intent_message.intent.intent_name == 'relayTurnOff':
            self.turnOffRelay(hermes, intent_message)

    def start_blocking(self):
        with Hermes(self.mqtt_addr) as h:
            h.subscribe_intents(self.master_intent_callback).start()

if __name__ == "__main__":
    RelaySwitch()

