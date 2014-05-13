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

R1_ADDR_LONG = b'\x00\x13\xA2\x00\x40\xB4\x10\x3b'
R1_ADDR_SHORT = b'\xff\xfe' 

xbee_thread_exit_flag = 0

class FastPlantingFrame(FastPlantingUI):

    def __init__(self, parent=None):
        super(FastPlantingFrame, self).__init__(parent)

        #create a pubsub receiver
        Publisher = pub.Publisher()
        Publisher.subscribe(self.on_txtMain_update,'update')

        # Open serial port
        self.Serial = serial.Serial()

        # Create API object, which spawns a new thread
        #self.Xbee = ZigBee(self.Serial, callback=self.message_received)
        self.Xbee = ZigBee(self.Serial)
        
        self.serialThread = XbeeThread(self.Serial, self.Xbee, Publisher) 

    def __del__(self):
        global xbee_thread_exit_flag
        xbee_thread_exit_flag = 1
        self.Xbee.halt()
        self.Serial.close()
        print 'FastPlantingFrame delete.'

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

    def on_btnClear_clicked(self, event):
        self.m_txtMain.Clear()

    def on_cmbBaud_changed(self, event):
        self.Serial.setBaudrate(int(self.m_comboBaudRate.GetValue()))

    def on_btnConnect_clicked(self, event):
        print self.Serial.isOpen()
        if not self.Serial.isOpen():
            try:
                self.Serial.port = self.m_comboSerial.GetValue()
                self.Serial.baudrate = int(self.m_comboBaudRate.GetValue())
                self.Serial.open()
            except Exception, e:
                print '[Error]COMM Open Fail!!', e
            else:
                self.m_btnConnect.SetLabel(u'关闭串口')
                self.m_imgStat.SetBitmap(Img_inopening.getBitmap())
                if self.Serial.isOpen() and self.Serial.inWaiting():
                    print 'on_btnConnect_clicked serial is ok'
        else:
            self.Serial.close()
            while self.Serial.isOpen(): pass

            self.m_btnConnect.SetLabel(u'打开串口')
            self.m_imgStat.SetBitmap(Img_inclosing.getBitmap())

    def on_btnTempCtrl_clicked( self, event ):
        strTempMin = self.m_txtTempMin.GetValue()
        strTempMax = self.m_txtTempMax.GetValue()
        nTempMin = float(strTempMin)
        nTempMax = float(strTempMax)
        if nTempMin < 0 or nTempMin > 50:
            print '[Error]TempMin out of range: ' + strTempMin
            return
        if nTempMax < 0 or nTempMax > 50:
            print '[Error]TempMax out of range: ' + strTempMax
            return
        if nTempMax < nTempMin:
            print '[Error]TempMax < TempMin'
            return

        # Send Tx packet Temperature min
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='A', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(nTempMin))
        
        # Wait for response
        if self.Serial.isOpen() and self.Serial.inWaiting():
            response = self.Xbee.wait_read_frame()
            print response

        # Send Tx packet Temperature max
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='B', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(nTempMax))
        
        # Wait for response
        if self.Serial.isOpen() and self.Serial.inWaiting():
            response = self.Xbee.wait_read_frame()
            print response

    def on_btnHumCtrl_clicked( self, event ):
        strHumMin = self.m_txtHumMin.GetValue()
        strHumMax = self.m_txtHumMax.GetValue()
        nHumMin = float(strHumMin)
        nHumMax = float(strHumMax)
        if nHumMin < 0 or nHumMin > 100:
            print '[Error]HumMin out of range: ' + strHumMin
            return
        if nHumMax < 0 or nHumMax > 100:
            print '[Error]HumMax out of range: ' + strHumMax
            return
        if nHumMax < nHumMin:
            print '[Error]HumMax < HumMin'
            return
        # Send Tx packet Humidity min
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='C', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(nHumMin))
        
        # Wait for response
        if self.Serial.isOpen() and self.Serial.inWaiting():
            response = self.Xbee.wait_read_frame()
            print response

        # Send Tx packet Humidity max
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='D', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(nHumMax))
        
        # Wait for response
        if self.Serial.isOpen() and self.Serial.inWaiting():
            response = self.Xbee.wait_read_frame()
            print response

class XbeeThread(threading.Thread):

    def __init__(self, Serial, Xbee, Publish):
        super(XbeeThread,self).__init__()

        self.Serial=Serial
        self.Xbee=Xbee
        self.Publisher = Publish
        print 'XbeeThread init.'

        self.start()
        
    def __del__(self):
        # halt() must be called before closing the serial
        # port in order to ensure proper thread shutdown
        self.Xbee.halt()
        self.Serial.close()
        print 'XbeeThread delete.'

    def message_received(self, data):
        try:
            orig_str = data['rf_data']  # dict assign to string
        except Exception, e:    # Except for receive empty Rx data while sending Tx data.
            print e
            return
        humidity_str = "H:"
        temperature_str = "T:"
        try:
            nHumPos = orig_str.index(humidity_str)
            strHum_num = orig_str[nHumPos+len(humidity_str):nHumPos+len(humidity_str)+5]
            nTempPos = orig_str.index(temperature_str)
            strTemp_num = orig_str[nTempPos+len(temperature_str):nTempPos+len(temperature_str)+5]
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            text = 'H:' + strHum_num + ' T:' + strTemp_num + ' ' + now_time
            #print text
            wx.CallAfter(self.Publisher.sendMessage, 'update', text)
        except Exception, e:
            print e
            pass
        

    def run(self):
        global xbee_thread_exit_flag
        # Do other stuff in the main thread
        while xbee_thread_exit_flag == 0:
            try:
                if self.Serial.isOpen() and self.Serial.inWaiting():
                    # print 'serial is ok'
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
