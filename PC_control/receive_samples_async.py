#! /usr/bin/python

"""
receive_samples_async.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

This example reads the serial port and asynchronously processes IO data
received from a remote XBee.
"""

from xbee import ZigBee
import time
import serial
import sys,string
import time

PORT = 'COM18'
BAUD_RATE = 9600

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

humidity_str="H:"
temperature_str="T:"

def message_received(data):
    orig_str = data['rf_data']  #dict assign to string
    nHumPos = orig_str.index(humidity_str)
    strHum_num = orig_str[nHumPos+len(humidity_str):nHumPos+len(humidity_str)+5]
    nTempPos = orig_str.index(temperature_str)
    strTemp_num = orig_str[nTempPos+len(temperature_str):nTempPos+len(temperature_str)+5]
    #print data
    now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    print 'Hum:' + strHum_num + ' Temp:' + strTemp_num + ' ' + now_time

# Create API object, which spawns a new thread
xbee = ZigBee(ser, callback=message_received)

# Do other stuff in the main thread
while True:
    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        break

# halt() must be called before closing the serial
# port in order to ensure proper thread shutdown
xbee.halt()
ser.close()
