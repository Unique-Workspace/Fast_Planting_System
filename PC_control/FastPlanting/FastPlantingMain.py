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
        #print(msg.data)
        self.m_txtMain.AppendText(msg.data)

    #def on_btnClear_clicked( self, event ):
      #  self.m_txtMain.Clear()

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
                #self.m_imgStat.SetBitmap(Img_inopening.getBitmap())
        else:
            self.ser.close()
            while self.ser.isOpen(): pass

            self.m_btnConnect.SetLabel(u'打开串口')
            #self.m_imgStat.SetBitmap(Img_inclosing.getBitmap())


        
class XbeeThread(threading.Thread):
    
    #PORT = 'COM18'
    #BAUD_RATE = 9600

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
        
        text = 'Hum:' + strHum_num + ' Temp:' + strTemp_num + ' ' + now_time
        print text
        wx.CallAfter(self.Publisher.sendMessage('update',text))

    def run(self):
        
        # Do other stuff in the main thread
        while True:
            try:
                #print 'XbeeThread while loop.'
                if self.Serial.isOpen() and self.Serial.inWaiting():
                    data = self.Xbee.wait_read_frame()
                    self.message_received(data)
                    
                time.sleep(1)
            except KeyboardInterrupt:
                break

        


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = FastPlantingFrame()
    frame.Show(True)
    app.MainLoop()
