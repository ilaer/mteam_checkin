#coding:utf-8
__author__ = 'ila'
# -*- coding:utf-8 -*-
import win32api,win32con,platform,os

class Starting_Up_Setting(object):
    def __init__(self):
        name = 'mteam_checkin'  # 要添加的项值名称
        sysstr = platform.system()
        if (sysstr == "Windows"):
            path = '{}\\{}'.format(os.getcwd(),'mteam_checkin.exe')
        elif (sysstr == "Linux"):
            path = '{}/{}'.format(os.getcwd(),'mteam_checkin.exe')
        else:
            path = '{}/{}'.format(os.getcwd(), 'mteam_checkin.exe')
        # 注册表项名
        KeyName = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        # 异常处理
        try:
            key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
            win32api.RegSetValueEx(key, name, 0, win32con.REG_SZ, path)
            win32api.RegCloseKey(key)
        except Exception as e:
            print(Exception,':',e)
