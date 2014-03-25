# -*- coding: utf-8 -*- 
# Read a string line and analyse the specific charactors.
# Filename: Analyse_String.py

import sys,string

humidity_str="H:"
temperature_str="T:"

orig_str="ABCEEFGH,.;'[ H:50.34  T:24.23  asdfg"
print orig_str

nHumPos = orig_str.index(humidity_str)
strHum_num = orig_str[nHumPos+len(humidity_str):nHumPos+len(humidity_str)+6]

nTempPos = orig_str.index(temperature_str)
strTemp_num = orig_str[nTempPos+len(temperature_str):nTempPos+len(temperature_str)+6]

nHum_num = string.atof(strHum_num)
nTemp_num = string.atof(strTemp_num)
print 'Hum:' + strHum_num + ' Temp:' + strTemp_num
print nHum_num
print nTemp_num
