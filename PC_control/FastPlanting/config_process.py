#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys, string
import os

CONFIG_FILE_PATH = '.config'

class ConfigProcess():
    def __init__(self):
        if not os.path.exists(CONFIG_FILE_PATH):
            self.fd = open(CONFIG_FILE_PATH, 'w+')
        else:
            self.fd = open(CONFIG_FILE_PATH, 'r+')

        # 由于网络地址会变化，故不记录, node_id即为物理地址
        # 'node_id': {'value': '0', 'tmin': 0, 'tmax': 0, 'hmin': 0, 'hmax': 0,
        #                    'wtmin': 0, 'wtmax': 0, 'led': 0}
        self.config_dict = {}

    def __del__(self):
        self.fd.close()
        pass

    def load_config(self):
        config_lines = self.fd.readlines()
        cfg_dict = {}
        for line in config_lines:
            #len(line)=56
            if len(line) < 50:
                print 'load_config empty.'
                return
            records = line.split(',')
            if records[0] in self.config_dict:
                self.config_dict[records[0]]['value'] = records[0]
                self.config_dict[records[0]]['tmin'] = '%4.2f' % float(records[1])
                self.config_dict[records[0]]['tmax'] = '%4.2f' % float(records[2])
                self.config_dict[records[0]]['hmin'] = '%4.2f' % float(records[3])
                self.config_dict[records[0]]['hmax'] = '%5.2f' % float(records[4])
                self.config_dict[records[0]]['wtmin'] = '%4.2f' % float(records[5])
                self.config_dict[records[0]]['wtmax'] = '%4.2f' % float(records[6])
                self.config_dict[records[0]]['led'] = int(records[7])
                print 'load_config duplicate.'
            else:
                cfg_dict[records[0]] = {}
                cfg_dict[records[0]]['value'] = records[0]
                cfg_dict[records[0]]['tmin'] = '%4.2f' % float(records[1])
                cfg_dict[records[0]]['tmax'] = '%4.2f' % float(records[2])
                cfg_dict[records[0]]['hmin'] = '%4.2f' % float(records[3])
                cfg_dict[records[0]]['hmax'] = '%5.2f' % float(records[4])
                cfg_dict[records[0]]['wtmin'] = '%4.2f' % float(records[5])
                cfg_dict[records[0]]['wtmax'] = '%4.2f' % float(records[6])
                cfg_dict[records[0]]['led'] = int(records[7])
                self.config_dict.update(cfg_dict)

        #print self.config_dict

    def save_config(self):
        lines = ''
        for key in self.config_dict.keys():
            config = self.config_dict.pop(key)
            addr_long = str(key)
            tmin = str(config['tmin'])
            tmax = str(config['tmax'])
            hmin = str(config['hmin'])
            hmax = str(config['hmax'])
            wtmin = str(config['wtmin'])
            wtmax = str(config['wtmax'])
            led = str(config['led'])
            line = addr_long + ',' + tmin + ',' + tmax + ',' + hmin + ',' \
             + hmax + ',' + wtmin + ',' + wtmax + ',' + led + '\n'
            lines += line
            #print key, line

        self.fd.seek(0)
        self.fd.truncate(0)
        self.fd.writelines(lines)


    # 鉴于文件操作的复杂性，保存的时候采取全部覆盖保存
    # data数据格式：tuple: (addr,tmin,tmax,hmin,hmax,wtmin,wtmax,led)
    def set_config_value(self, data):
        if len(data) == 8:
            if data[0] in self.config_dict:
                self.config_dict[data[0]] = {}
                self.config_dict[data[0]]['value'] = data[0]
                self.config_dict[data[0]]['tmin'] = '%4.2f' % float(data[1])
                self.config_dict[data[0]]['tmax'] = '%4.2f' % float(data[2])
                self.config_dict[data[0]]['hmin'] = '%4.2f' % float(data[3])
                self.config_dict[data[0]]['hmax'] = '%5.2f' % float(data[4])
                self.config_dict[data[0]]['wtmin'] = '%4.2f' % float(data[5])
                self.config_dict[data[0]]['wtmax'] = '%4.2f' % float(data[6])
                self.config_dict[data[0]]['led'] = int(data[7])
                print data[0] + 'set_config_value is duplicate.'
            else:
                cfg_dict = {}
                cfg_dict[data[0]] = {}
                cfg_dict[data[0]]['value'] = data[0]
                cfg_dict[data[0]]['tmin'] = '%4.2f' % float(data[1])
                cfg_dict[data[0]]['tmax'] = '%4.2f' % float(data[2])
                cfg_dict[data[0]]['hmin'] = '%4.2f' % float(data[3])
                cfg_dict[data[0]]['hmax'] = '%5.2f' % float(data[4])
                cfg_dict[data[0]]['wtmin'] = '%4.2f' % float(data[5])
                cfg_dict[data[0]]['wtmax'] = '%4.2f' % float(data[6])
                cfg_dict[data[0]]['led'] = int(data[7])
                self.config_dict.update(cfg_dict)
                #print self.config_dict
        else:
            print '[Error] data is invalid.'

    # 传入addr_long，在字典中查找对应参数，并返回元组
    def get_config_value(self, addr_long):
        if addr_long in self.config_dict:
            tmin = self.config_dict[addr_long]['tmin']
            tmax = self.config_dict[addr_long]['tmax']
            hmin = self.config_dict[addr_long]['hmin']
            hmax = self.config_dict[addr_long]['hmax']
            wtmin = self.config_dict[addr_long]['wtmin']
            wtmax = self.config_dict[addr_long]['wtmax']
            led = self.config_dict[addr_long]['led']
            ret = (tmin, tmax, hmin, hmax, wtmin, wtmax, led)
            return ret
        else:
            return ()

'''
if __name__ == "__main__":
    config = ConfigProcess()
    config.load_config()

    data = ('0013A20040B41039', 20.0, 30.0, 90.0, 100.0, 20.0, 35.0, 1)
    config.set_config_value(data)

    result = config.get_config_value('0013A20040B41039')
    print result

    config.save_config()
'''