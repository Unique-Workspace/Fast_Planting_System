# -*- coding: utf-8 -*- 

import wx
import wx.xrc
from serial import Serial
from wx.lib.pubsub import pub
import FastPlantUI.FastPlantUI


class SerialFrame(FastPlantUI):
    def __init__(self,parent=None):
        super(SerialFrame,self).__init__(parent)
        
        self.m_imgStat.SetBitmap(Img_inclosing.getBitmap())
        
        self.Ser = Serial()
        self.serialThread = SerialThread(self.Ser)
        
        #create a pubsub receiver
        Publisher = pub.Publisher()
        Publisher.subscribe(self.on_txtMain_update,'update')    
        
    def on_txtMain_update(self, msg):
        self.m_txtMain.AppendText(msg.data)
    
    def on_btnSend_clicked( self, event ):
        self.Ser.write(self.m_txtInput.GetValue())
        
    def on_btnClear_clicked( self, event ):
        self.m_txtMain.Clear()
    
    def on_chkHEXShow_changed( self, event ):
        s = self.m_txtMain.GetValue()
        if self.m_chkHEXShow.IsChecked():
            s = ''.join('%02X' %i for i in [ord(c) for c in s])
        else:
            s = ''.join([chr(int(i,16)) for i in [s[i*2:i*2+2] for i in range(0,len(s)/2)]])
        self.m_txtMain.Clear()
        self.m_txtMain.SetValue(s)
        
    def on_cmbBaud_changled( self, event ):
        self.Ser.setBaudrate(int(self.m_cmbBaud.GetValue()))
        
    def on_btnOpen_clicked( self, event ):
        if not self.Ser.isOpen():
            try:
                self.Ser.timeout = 1
                self.Ser.xonxoff = 0
                self.Ser.port = self.m_cmbCOMX.GetValue()
                self.Ser.parity = self.m_cmbChek.GetValue()[0]
                self.Ser.baudrate = int(self.m_cmbBaud.GetValue())
                self.Ser.bytesize = int(self.m_cmbData.GetValue())
                self.Ser.stopbits = int(self.m_cmbStop.GetValue())
                self.Ser.open()
            except Exception,e:
                print 'COMM Open Fail!!',e
            else:
                self.m_btnOpen.SetLabel(u'关闭串口')
                self.m_imgStat.SetBitmap(Img_inopening.getBitmap())
        else:
            self.Ser.close()
            while self.Ser.isOpen(): pass

            self.m_btnOpen.SetLabel(u'打开串口')
            self.m_imgStat.SetBitmap(Img_inclosing.getBitmap())

    
    def on_btnExtn_clicked( self, event ):
        event.Skip()




import time
import threading


class SerialThread(threading.Thread):
	
    def __init__(self,Ser):
        super(SerialThread,self).__init__()
        
        self.Ser=Ser
        
        self.start()
    
    def run(self):
    	Publisher = pub.Publisher()
        while True:            
            if self.Ser.isOpen() and self.Ser.inWaiting():
                text = self.Ser.read(self.Ser.inWaiting())
                wx.CallAfter(Publisher.sendMessage('update',text))
                
            time.sleep(0.01)
                            


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
    frame = SerialFrame()
    frame.Show(True)
    app.MainLoop()
