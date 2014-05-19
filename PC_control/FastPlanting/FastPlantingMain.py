#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
FastPlantingMain.py

By Kun Ling, 2014
timonkun@gmail.com

This is main program for Fast Planting System.

2014.05.17
sendMessage() takes exactly 2 arguments (3 given)

2014.05.15
程序退出时出现：“swig/python detected a memory leak of type 'wxPyXmlSubclassFactory *', no destructor found.”
参考：https://groups.google.com/forum/#!topic/wxPython-users/984OzOdHQCc
无须理会
"""

import wx
import wx.xrc
from wx.lib.pubsub import setuparg1
from wx.lib.pubsub import pub
from FastPlantingUI import FastPlantingUI

from xbee import ZigBee
import serial
import time
import threading

R1_ADDR_LONG = b'\x00\x13\xA2\x00\x40\xB4\x10\x3b'
R1_ADDR_SHORT = b'\xff\xfe' 

xbee_thread_exit_flag = False

class FastPlantingFrame(FastPlantingUI):

    def __init__(self, parent=None):
        super(FastPlantingFrame, self).__init__(parent)

        #create a pubsub receiver
        pub.subscribe(self.on_txtMain_update, 'update')

        # Open serial port
        self.Serial = serial.Serial()

        # Create API object, which spawns a new thread
        #self.Xbee = ZigBee(self.Serial, callback=self.message_received)
        self.Xbee = ZigBee(self.Serial)
        
        self.serialThread = XbeeThread(self.Serial, self.Xbee)

    def __del__(self):
        global xbee_thread_exit_flag
        xbee_thread_exit_flag = True
        self.Xbee.halt()
        self.Serial.close()
        print 'FastPlantingFrame delete.'

    def on_txtMain_update(self, msg):
        print(msg.data)
        humidity_str="H:"
        temperature_str="Tr:"
        temperature_water_str="Tw:"
        nHumPos = msg.data.index(humidity_str)
        strHum_num = msg.data[nHumPos+len(humidity_str):nHumPos+len(humidity_str)+5]
        nTempPos = msg.data.index(temperature_str)
        strTemp_num = msg.data[nTempPos+len(temperature_str):nTempPos+len(temperature_str)+5]
        nTempWaterPos = msg.data.index(temperature_water_str)
        strTempWater_num = msg.data[nTempWaterPos+len(temperature_water_str):nTempWaterPos+len(temperature_water_str)+5]
        now_time = time.strftime('%m-%d %H:%M:%S', time.localtime(time.time()))
        #print data
        self.m_txtMain.AppendText(msg.data)
        self.m_txtMain.AppendText('\n')
        self.m_textTemp.Clear()
        self.m_textTemp.AppendText(strTemp_num)
        self.m_textHum.Clear()
        self.m_textHum.AppendText(strHum_num)
        self.m_textTempWater.Clear()
        self.m_textTempWater.AppendText(strTempWater_num)
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
        tempra_min = self.m_txtTempMin.GetValue()[0:6]
        tempra_max = self.m_txtTempMax.GetValue()[0:6]
        if float(tempra_min) < 0 or float(tempra_min) > 50:
            print '[Error]TempMin out of range: ' + tempra_min
            return
        if float(tempra_max) < 0 or float(tempra_max) > 50:
            print '[Error]TempMax out of range: ' + tempra_max
            return
        if float(tempra_max) < float(tempra_min):
            print '[Error]TempMax < TempMin'
            return

        tempra_min_data = 'TRmin:' + tempra_min
        tempra_max_data = 'TRmax:' + tempra_max
        print tempra_min_data
        # Send Tx packet Temperature min
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='A', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(tempra_min_data))

        # Wait for response
        #if self.Serial.isOpen() and self.Serial.inWaiting():
        #    response = self.Xbee.wait_read_frame()
        #    print response

        # Send Tx packet Temperature max
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='B', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(tempra_max_data))
        
        # Wait for response
        #if self.Serial.isOpen() and self.Serial.inWaiting():
        #    response = self.Xbee.wait_read_frame()
        #    print response

    def on_btnHumCtrl_clicked(self, event):
        humi_min = self.m_txtHumMin.GetValue()[0:6]
        humi_max = self.m_txtHumMax.GetValue()[0:6]
        if float(humi_min) < 0 or float(humi_min) > 100:
            print '[Error]HumMin out of range: ' + humi_min
            return
        if float(humi_max) < 0 or float(humi_max) > 100:
            print '[Error]HumMax out of range: ' + humi_max
            return
        if float(humi_max) < float(humi_min):
            print '[Error]HumMax < HumMin'
            return
        humi_min_data = 'Hmin:' + humi_min
        humi_max_data = 'Hmax:' + humi_max
        # Send Tx packet Humidity min
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='C', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(humi_min_data))

        # Wait for response
        #if self.Serial.isOpen() and self.Serial.inWaiting():
        #    response = self.Xbee.wait_read_frame()
        #    print response

        # Send Tx packet Humidity max
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='D', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(humi_max_data))
        
        # Wait for response
        #if self.Serial.isOpen() and self.Serial.inWaiting():
        #    response = self.Xbee.wait_read_frame()
        #    print response

    def on_btnTempWaterCtrl_clicked(self, event):
        temp_water_min = self.m_txtTempWaterMin.GetValue()[0:6]
        temp_water_max = self.m_txtTempWaterMax.GetValue()[0:6]
        if float(temp_water_min) < 0 or float(temp_water_min) > 50:
            print '[Error]TempWaterMin out of range: ' + temp_water_min
            return
        if float(temp_water_max) < 0 or float(temp_water_max) > 50:
            print '[Error]TempWaterMax out of range: ' + temp_water_max
            return
        if float(temp_water_max) < float(temp_water_min):
            print '[Error]TempWaterMax < TempWaterMin'
            return
        temp_water_min_data = 'TWmin:' + temp_water_min
        temp_water_max_data = 'TWmax:' + temp_water_max
        # Send Tx packet Humidity min
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='E', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(temp_water_min_data))

        # Wait for response
        #if self.Serial.isOpen() and self.Serial.inWaiting():
        #    response = self.Xbee.wait_read_frame()
        #    print response

        # Send Tx packet Humidity max
        if self.Serial.isOpen():
            self.Xbee.send('tx', frame_id='F', dest_addr_long=R1_ADDR_LONG, dest_addr=R1_ADDR_SHORT, data=str(temp_water_max_data))

        # Wait for response
        #if self.Serial.isOpen() and self.Serial.inWaiting():
        #    response = self.Xbee.wait_read_frame()
        #    print response


class XbeeThread(threading.Thread):

    def __init__(self, Serial, Xbee):
        super(XbeeThread,self).__init__()

        self.Serial=Serial
        self.Xbee=Xbee
  
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
        try:
            '''数据结构：字符串类型 '湿度，温度，水温' '''
            #print orig_str
            text = orig_str.split(',')
            humidity = text[0]
            temperature_room = text[1]
            temperature_water = text[2]
            now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            text = 'H:' + humidity + ' Tr:' + temperature_room + ' Tw:' + temperature_water + ' ' + now_time
            #print text
            #wx.CallAfter(pub.sendMessage, 'update', text)
            pub.sendMessage('update', text)
        except Exception, e:
            print e
            pass
        

    def run(self):
        global xbee_thread_exit_flag
        # Do other stuff in the main thread
        while not xbee_thread_exit_flag:
            try:
                if self.Serial.isOpen() and self.Serial.inWaiting():
                    # print 'serial is ok'
                    data = self.Xbee.wait_read_frame()
                    self.message_received(data)
                    
                time.sleep(3)
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
    app = wx.App(False)
    frame = FastPlantingFrame()
    frame.Show(True)
    app.MainLoop()
