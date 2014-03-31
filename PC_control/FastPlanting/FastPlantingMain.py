#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
receive_samples_async.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

This example reads the serial port and asynchronously processes IO data
received from a remote XBee.
"""

import wx
import wx.xrc
from wx.lib.pubsub import pub
from FastPlantingUI import FastPlantingUI

from xbee import ZigBee
import time
import serial
import sys,string
import time
import threading

class FastPlantingFrame(FastPlantingUI):
    #port = 'COM18'
    #baud_rate = 9600

    def __init__(self, parent=None):
        super(FastPlantingFrame, self).__init__(parent)

        #create a pubsub receiver
        Publisher = pub.Publisher()
        Publisher.subscribe(self.on_txtMain_update,'update')

        # Open serial port
        self.ser = serial.Serial()
        self.serialThread = XbeeThread(self.ser, Publisher) 
        
    def on_txtMain_update(self, msg):
        print(msg.data)
        humidity_str="H:"
        temperature_str="T:"
        nHumPos = msg.data.index(humidity_str)
        strHum_num = msg.data[nHumPos+len(humidity_str):nHumPos+len(humidity_str)+5]
        nTempPos = msg.data.index(temperature_str)
        strTemp_num = msg.data[nTempPos+len(temperature_str):nTempPos+len(temperature_str)+5]
        now_time = time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))
        #print data
        self.m_txtMain.AppendText(msg.data)
        self.m_txtMain.AppendText('\n')
        self.m_textTemp.Clear()
        self.m_textTemp.AppendText(strTemp_num)
        self.m_textHum.Clear()
        self.m_textHum.AppendText(strHum_num)
        self.m_textTime.Clear()
        self.m_textTime.AppendText(now_time)

    def on_btnClear_clicked( self, event ):
        self.m_txtMain.Clear()

    def on_cmbBaud_changed( self, event ):
        self.ser.setBaudrate(int(self.m_cmbBaud.GetValue()))

    def on_btnConnect_clicked( self, event ):
        print self.ser.isOpen()
        if not self.ser.isOpen():
            try:
                self.ser.port = self.m_comboSerial.GetValue()
                print self.ser.port 
                self.ser.baudrate = int(self.m_comboBaudRate.GetValue())
                print self.ser.baudrate
                self.ser.open()
            except Exception,e:
                print 'COMM Open Fail!!',e
            else:
                self.m_btnConnect.SetLabel(u'关闭串口')
                self.m_imgStat.SetBitmap(Img_inopening.getBitmap())
        else:
            self.ser.close()
            while self.ser.isOpen(): pass

            self.m_btnConnect.SetLabel(u'打开串口')
            self.m_imgStat.SetBitmap(Img_inclosing.getBitmap())


        
class XbeeThread(threading.Thread):

    def __init__(self, Serial, Publish):
        super(XbeeThread,self).__init__()

        self.Serial=Serial
        self.Publisher = Publish
        # Create API object, which spawns a new thread
        #self.Xbee = ZigBee(self.Serial, callback=self.message_received)
        self.Xbee = ZigBee(self.Serial)
        print 'XbeeThread init.'

        self.start()
        
    def __del__(self):
        # halt() must be called before closing the serial
        # port in order to ensure proper thread shutdown
        self.Xbee.halt()
        self.Serial.close()
        print 'XbeeThread delete.'
        
    
    def message_received(self, data):
        humidity_str="H:"
        temperature_str="T:"
        orig_str = data['rf_data']  #dict assign to string
        nHumPos = orig_str.index(humidity_str)
        strHum_num = orig_str[nHumPos+len(humidity_str):nHumPos+len(humidity_str)+5]
        nTempPos = orig_str.index(temperature_str)
        strTemp_num = orig_str[nTempPos+len(temperature_str):nTempPos+len(temperature_str)+5]
        #print data
        now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        
        text = 'H:' + strHum_num + ' T:' + strTemp_num + ' ' + now_time
        print text
        wx.CallAfter(self.Publisher.sendMessage('update',text))

    def run(self):
        
        # Do other stuff in the main thread
        while True:
            try:
                #only for testing without xbee
                #strHum_num='61.23'
                #strTemp_num='23.84'
                #now_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                #text = 'Hum:' + strHum_num + ' Temp:' + strTemp_num + ' ' + now_time
                #wx.CallAfter(self.Publisher.sendMessage('update',text))
                    
                if self.Serial.isOpen() and self.Serial.inWaiting():
                    data = self.Xbee.wait_read_frame()
                    self.message_received(data)
                    
                time.sleep(1)
            except KeyboardInterrupt:
                break

        
from wx.lib import embeddedimage

Img_inclosing = embeddedimage.PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAIAAAAC64paAAAAAXNSR0IArs4c6QAAAARnQU1B"
    "AACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAABiSURBVDhPY/iPDTBgAOzK0EQxtSGL"
    "oCtG5uPXCZFFUQ/nEKMTTT/UJOJ1IusHaSZVJ1z/AGkmz70jXBfZ8QxNq+QFH8hWsm2GaiZD"
    "PyQ7IbIY8Y5HZETq5GeoS/A6AK0kAQCtTO8ROTKfPAAAAABJRU5ErkJggg==")


Img_inopening = embeddedimage.PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAAXNSR0IArs4c6QAAAARnQU1B"
    "AACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAACKSURBVDhPY/wPBAw4wDtZVawyQo9v"
    "49LCwIjNQFwGoZuCzWAmdEXEGgbSh00tioGkGAZzCLoeuIHkGIbNULCBlBiGbihGGOKMPiIl"
    "qGogyKeMb2VUcKZDIh2FooyqLgSZPBINxJfRBzxSQI6jTaRQw9swM+AupMRQZL0oXibHUHQ9"
    "GGFIiqHY1AIAg2UtGigTDxsAAAAASUVORK5CYII=")

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = FastPlantingFrame()
    frame.Show(True)
    app.MainLoop()
