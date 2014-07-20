# setup.py

from distutils.core import setup
import numpy
import py2exe

option={"py2exe":{"includes":["sip", "numpy"]}}
setup(windows=[{"script":"fastplanting_main.py"}], options=option)