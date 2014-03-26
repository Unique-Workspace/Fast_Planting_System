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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FastPlanting", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer6 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_txtMain = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_NO_VSCROLL|wx.TE_READONLY )
		bSizer4.Add( self.m_txtMain, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer6.Add( bSizer4, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		m_comboSerialChoices = [ u"COM1", u"COM2", u"COM3", u"COM4", u"COM5", u"COM6", u"COM7", u"COM8", u"COM9", u"COM10", u"COM11", u"COM12", u"COM13", u"COM14", u"COM15", u"COM16", u"COM17", u"COM18", u"COM19", u"COM20" ]
		self.m_comboSerial = wx.ComboBox( self, wx.ID_ANY, u"COM1", wx.DefaultPosition, wx.DefaultSize, m_comboSerialChoices, 0 )
		self.m_comboSerial.SetSelection( 0 )
		bSizer8.Add( self.m_comboSerial, 0, wx.ALL, 5 )
		
		m_comboBaudRateChoices = [ u"9600", u"14400", u"19200" ]
		self.m_comboBaudRate = wx.ComboBox( self, wx.ID_ANY, u"9600", wx.DefaultPosition, wx.DefaultSize, m_comboBaudRateChoices, 0 )
		bSizer8.Add( self.m_comboBaudRate, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_btnClear = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_btnClear, 0, wx.ALL, 5 )
		
		self.m_btnConnect = wx.Button( self, wx.ID_ANY, u"Connect", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.m_btnConnect, 0, wx.ALL, 5 )
		
		
		bSizer6.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer6 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_btnClear.Bind( wx.EVT_BUTTON, self.on_btnClear_clicked )
		self.m_btnConnect.Bind( wx.EVT_BUTTON, self.on_btnConnect_clicked )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_btnClear_clicked( self, event ):
		event.Skip()
	
	def on_btnConnect_clicked( self, event ):
		event.Skip()
	

