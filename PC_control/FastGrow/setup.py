# setup.py

from distutils.core import setup
import py2exe

options = {"py2exe": {"packages": ['wx.lib.pubsub']}}
setup(windows=[{'script': 'wxserial.py'}],options=options)