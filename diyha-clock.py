#!/usr/bin/python3
""" DIYHA clock
    Display time and respond to MQTT messages
"""

# The MIT License (MIT)
#
# Copyright (c) 2019 parttimehacker@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
import time
import logging
import logging.config

# imported third party classes

import paho.mqtt.client as mqtt

# import clock and who HAL classes

from pkg_classes.sevensegmenthal import SevenSegmentHAL

# import normal diyha helper classes

from pkg_classes.configmodel import ConfigModel

#imported constants

from pkg_classes.sevensegmenthal import TIME_MODE, WHO_MODE

# Start logging and enable imported classes to log appropriately.

LOGGING_FILE = '/usr/local/diyha-clock/logging.ini'
logging.config.fileConfig( fname=LOGGING_FILE, disable_existing_loggers=False )
LOGGER = logging.getLogger(__name__)
LOGGER.info('Application started')

# parse the command line arguments

CONFIG = ConfigModel(LOGGING_FILE)

# Initialize devices

DISPLAY = SevenSegmentHAL(LOGGING_FILE) # Seven segment LED backpack from Adafruit
DISPLAY.set_display_mode(TIME_MODE)

# Process MQTT messages using a dispatch table algorithm.

def system_message(client, msg):
    """ Log and process system messages. """
    LOGGER.info(msg.topic+" "+msg.payload.decode('utf-8'))
    if msg.topic == 'diy/system/who':
        if msg.payload == b'ON':
            DISPLAY.set_display_mode(WHO_MODE)
        else:
            DISPLAY.set_display_mode(TIME_MODE)
    elif msg.topic == 'diy/system/silent':
        if msg.payload == b'ON':
            DISPLAY.set_brightness(0.1)
        else:
            DISPLAY.set_brightness(1.0)
    elif msg.topic == 'diy/system/demo':
        if msg.payload == b'ON':
            DISPLAY.set_brightness(1.0)
        else:
            DISPLAY.set_brightness(0.1)
                   
#pylint: disable=unused-argument

#  A dictionary dispatch table is used to parse and execute MQTT messages.

TOPIC_DISPATCH_DICTIONARY = {
    "diy/system/demo":
        {"method":system_message},
    "diy/system/silent":
        {"method":system_message},
    "diy/system/who":
        {"method":system_message},
    }

def on_message(client, userdata, msg):
    """ dispatch to the appropriate MQTT topic handler """
    #pylint: disable=unused-argument
    TOPIC_DISPATCH_DICTIONARY[msg.topic]["method"](client, msg)


def on_connect(client, userdata, flags, rc_msg):
    """ Subscribing in on_connect() means that if we lose the connection and
        reconnect then subscriptions will be renewed.
    """
    #pylint: disable=unused-argument
    client.subscribe("diy/system/demo", 1)
    client.subscribe("diy/system/silent", 1)
    client.subscribe("diy/system/who", 1)

def on_disconnect(client, userdata, rc_msg):
    """ Subscribing on_disconnect() tilt """
    #pylint: disable=unused-argument
    client.connected_flag = False
    client.disconnect_flag = True


if __name__ == '__main__':

    # Setup MQTT handlers then wait for timed events or messages

    CLIENT = mqtt.Client()
    CLIENT.on_connect = on_connect
    CLIENT.on_disconnect = on_disconnect
    CLIENT.on_message = on_message

    # command line argument for the switch mode - motion activated is the default

    CLIENT.connect(CONFIG.get_broker(), 1883, 60)
    CLIENT.loop_start()
    
    # let MQTT stuff initialize

    time.sleep(2) 

    # Loop forever checking for timed events every 10 seconds.

    while True:
        time.sleep(1.0)
        DISPLAY.update()
