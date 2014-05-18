# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Nov  6 2013)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class FastPlantingUI
###########################################################################

class FastPlantingUI ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FastPlanting", pos = wx.DefaultPosition, size = wx.Size( 648,388 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_txtMain = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TE_MULTILINE|wx.TE_READONLY )
		bSizer4.Add( self.m_txtMain, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_btnClear = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.m_btnClear, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"设定范围" ), wx.VERTICAL )
		
		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticConfigTemp = wx.StaticText( self, wx.ID_ANY, u"温度范围：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticConfigTemp.Wrap( -1 )
		bSizer7.Add( self.m_staticConfigTemp, 0, wx.ALL, 5 )
		
		self.m_txtTempMin = wx.TextCtrl( self, wx.ID_ANY, u"15.00", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtTempMin.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_txtTempMin, 0, wx.ALL, 3 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"~", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		bSizer7.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.m_txtTempMax = wx.TextCtrl( self, wx.ID_ANY, u"25.00", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtTempMax.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer7.Add( self.m_txtTempMax, 0, wx.ALL, 5 )
		
		
		bSizer7.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_btnTempCtrl = wx.Button( self, wx.ID_ANY, u"温度设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer7.Add( self.m_btnTempCtrl, 0, wx.ALL, 5 )
		
		
		sbSizer4.Add( bSizer7, 1, wx.EXPAND, 5 )
		
		bSizer81 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticConfigTemp1 = wx.StaticText( self, wx.ID_ANY, u"湿度范围：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticConfigTemp1.Wrap( -1 )
		bSizer81.Add( self.m_staticConfigTemp1, 0, wx.ALL, 5 )
		
		self.m_txtHumMin = wx.TextCtrl( self, wx.ID_ANY, u"80.00", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtHumMin.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer81.Add( self.m_txtHumMin, 0, wx.ALL, 5 )
		
		self.m_staticText71 = wx.StaticText( self, wx.ID_ANY, u"~", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText71.Wrap( -1 )
		bSizer81.Add( self.m_staticText71, 0, wx.ALL, 5 )
		
		self.m_txtHumMax = wx.TextCtrl( self, wx.ID_ANY, u"100.00", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtHumMax.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer81.Add( self.m_txtHumMax, 0, wx.ALL, 5 )
		
		
		bSizer81.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_btnHumCtrl = wx.Button( self, wx.ID_ANY, u"湿度设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer81.Add( self.m_btnHumCtrl, 0, wx.ALL, 5 )
		
		
		sbSizer4.Add( bSizer81, 1, wx.EXPAND, 5 )
		
		bSizer71 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticConfigTemp2 = wx.StaticText( self, wx.ID_ANY, u"水温范围：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticConfigTemp2.Wrap( -1 )
		bSizer71.Add( self.m_staticConfigTemp2, 0, wx.ALL, 5 )
		
		self.m_txtTempWaterMin = wx.TextCtrl( self, wx.ID_ANY, u"20.00", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtTempWaterMin.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer71.Add( self.m_txtTempWaterMin, 0, wx.ALL, 3 )
		
		self.m_staticText72 = wx.StaticText( self, wx.ID_ANY, u"~", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText72.Wrap( -1 )
		bSizer71.Add( self.m_staticText72, 0, wx.ALL, 5 )
		
		self.m_txtTempWaterMax = wx.TextCtrl( self, wx.ID_ANY, u"30.00", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_txtTempWaterMax.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 93, 90, False, wx.EmptyString ) )
		
		bSizer71.Add( self.m_txtTempWaterMax, 0, wx.ALL, 5 )
		
		
		bSizer71.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_btnTempWaterCtrl = wx.Button( self, wx.ID_ANY, u"水温设定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer71.Add( self.m_btnTempWaterCtrl, 0, wx.ALL, 5 )
		
		
		sbSizer4.Add( bSizer71, 1, wx.EXPAND, 5 )
		
		
		bSizer6.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		bSizer61 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTxtTemp = wx.StaticText( self, wx.ID_ANY, u"温度：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTxtTemp.Wrap( -1 )
		bSizer61.Add( self.m_staticTxtTemp, 0, wx.ALL, 5 )
		
		self.m_textTemp = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.SIMPLE_BORDER )
		bSizer61.Add( self.m_textTemp, 0, wx.ALL, 5 )
		
		self.m_staticTxtHum = wx.StaticText( self, wx.ID_ANY, u"    湿度：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTxtHum.Wrap( -1 )
		bSizer61.Add( self.m_staticTxtHum, 0, wx.ALL, 5 )
		
		self.m_textHum = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.SIMPLE_BORDER )
		bSizer61.Add( self.m_textHum, 0, wx.ALL, 5 )
		
		self.m_staticTxtTime = wx.StaticText( self, wx.ID_ANY, u"水温：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTxtTime.Wrap( -1 )
		bSizer61.Add( self.m_staticTxtTime, 0, wx.ALL, 5 )
		
		self.m_textTempWater = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.SIMPLE_BORDER )
		bSizer61.Add( self.m_textTempWater, 0, wx.ALL, 5 )
		
		self.m_staticTxtTime1 = wx.StaticText( self, wx.ID_ANY, u"时间：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTxtTime1.Wrap( -1 )
		bSizer61.Add( self.m_staticTxtTime1, 0, wx.ALL, 5 )
		
		self.m_textTime = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY|wx.SIMPLE_BORDER )
		bSizer61.Add( self.m_textTime, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer61, 0, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticTxtPort = wx.StaticText( self, wx.ID_ANY, u"串口号：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTxtPort.Wrap( -1 )
		bSizer8.Add( self.m_staticTxtPort, 0, wx.ALL, 5 )
		
		m_comboSerialChoices = [ u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8", u"COM9", u"COM10", u"COM11", u"COM12", u"COM13", u"COM14", u"COM15", u"COM16", u"COM17", u"COM18", u"COM19", u"COM20" ]
		self.m_comboSerial = wx.ComboBox( self, wx.ID_ANY, u"COM28", wx.DefaultPosition, wx.DefaultSize, m_comboSerialChoices, 0 )
		self.m_comboSerial.SetSelection( 0 )
		bSizer8.Add( self.m_comboSerial, 0, wx.ALL, 5 )
		
		self.m_staticTxtBaudRate = wx.StaticText( self, wx.ID_ANY, u"    波特率：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTxtBaudRate.Wrap( -1 )
		bSizer8.Add( self.m_staticTxtBaudRate, 0, wx.ALL, 5 )
		
		m_comboBaudRateChoices = [ u"9600", u"14400", u"19200", u"115200" ]
		self.m_comboBaudRate = wx.ComboBox( self, wx.ID_ANY, u"115200", wx.DefaultPosition, wx.DefaultSize, m_comboBaudRateChoices, 0 )
		bSizer8.Add( self.m_comboBaudRate, 0, wx.ALL, 5 )
		
		
		bSizer8.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_btnConnect = wx.Button( self, wx.ID_ANY, u"连接串口", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_btnConnect, 0, wx.ALL, 5 )
		
		self.m_imgStat = wx.StaticBitmap( self, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_BUTTON ), wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_imgStat, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		self.m_timer1 = wx.Timer()
		self.m_timer1.SetOwner( self, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_btnClear.Bind( wx.EVT_BUTTON, self.on_btnClear_clicked )
		self.m_btnTempCtrl.Bind( wx.EVT_BUTTON, self.on_btnTempCtrl_clicked )
		self.m_btnHumCtrl.Bind( wx.EVT_BUTTON, self.on_btnHumCtrl_clicked )
		self.m_btnTempWaterCtrl.Bind( wx.EVT_BUTTON, self.on_btnTempWaterCtrl_clicked )
		self.m_btnConnect.Bind( wx.EVT_BUTTON, self.on_btnConnect_clicked )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_btnClear_clicked( self, event ):
		event.Skip()
	
	def on_btnTempCtrl_clicked( self, event ):
		event.Skip()
	
	def on_btnHumCtrl_clicked( self, event ):
		event.Skip()
	
	def on_btnTempWaterCtrl_clicked( self, event ):
		event.Skip()
	
	def on_btnConnect_clicked( self, event ):
		event.Skip()
	

