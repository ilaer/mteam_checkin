#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time, sys, configparser, random, logging, json,requests,os
from logging import handlers
from threading import Thread
from trayicon import SysTrayIcon
try:
    from tkinter import *
except ImportError:  # Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    # Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    # Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    # import tkFileDialog
    # import tkSimpleDialog
else:  # Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    # import tkinter.filedialog as tkFileDialog
    # import tkinter.simpledialog as tkSimpleDialog    #askstring()

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning  # 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)  # 禁用安全请求警告

from ui import Application_ui

conf = configparser.ConfigParser()
ini_path = 'config.ini'
conf.read(ini_path, encoding='utf-8')

if 'mteam' in conf.sections():
    for i in conf.items('mteam'):
        if 'username' in i:
            mteam_username = i[1]
        elif 'password' in i:
            mteam_password = i[1]
        elif 'login_url' in i:
            mteam_login_url = i[1]
        elif 'checkin_url' in i:
            mteam_checkin_url = i[1]
        elif 'loop' in i:
            mteam_loop = i[1]
        elif 'interval' in i:
            mteam_interval = i[1]
        elif 'last_login' in i:
            mteam_last_login =i[0]
        elif 'last_checkin' in i:
            mteam_last_checkin =i[0]
else:
    sys.exit()

if 'app' in conf.sections():
    for i in conf.items('app'):
        if 'default_frame' in i:
            default_frame = i[1]
else:
    sys.exit()

mteam_cycle_flag = 1#mteam循环签到flag，1为循环，0为停止循环
mteam_run_flag=0#mteam启动状态flag，1为已启动，0为未启动

class Mteam_Checkin(Thread):
    def __init__(self, username, password, login_url, checkin_url, mteam_text, mteam_label_text, mteam_log,
                 mteam_interval,conf):
        Thread.__init__(self)
        self.username = username
        self.passsword = password
        self.login_url = login_url
        self.checkin_url = checkin_url
        self.mteam_text = mteam_text
        self.mteam_label_text = mteam_label_text
        self.mteam_log = mteam_log
        self.mteam_interval = mteam_interval
        self.conf=conf
    def run(self):
        global mteam_cycle_flag,mteam_run_flag
        mteam_run_flag=1
        headers = {'Accept': 'text/html, application/xhtml+xml, */*',
                   'Accept-Encoding': 'gzip, deflate',
                   'Accept-Language': 'zh-CN',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   'Referer': 'https://tp.m-team.cc/login.php',
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Host': 'tp.m-team.cc',
                   'Connection': 'Keep-Alive',
                   'Cache-Control': 'no-cache'
                   }
        post_data = {
            'username': self.username,
            'password': self.passsword
        }
        # 循环
        t1 = float(time.time())
        mteam_num = 0
        while 1:
            if mteam_cycle_flag == 0:
                break
            if mteam_num > 0:
                if float(time.time()) - t1 < random.uniform(float(self.mteam_interval),float(self.mteam_interval) + 60):
                    continue
            # 条件成立，开始登录签到
            self.mteam_text.insert(1.0, '###############\n{},开始mteam本次登录。\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            self.mteam_log.warning('###############\n开始mteam本次登录。')
            s = requests.session()
            r1=s.post(url=self.login_url, headers=headers, data=post_data,  verify=False)

            if r1.status_code == requests.codes.ok and 'ila2002' in r1.content:

                self.conf.set('mteam','last_login',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))))
                self.conf.write(open(ini_path, "r+"))

                self.mteam_text.insert(1.0, '{},mteam登录成功。\n'.format(
                    time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                self.mteam_log.warning('mteam登录成功。')
                r2 = s.get(url=self.checkin_url, headers=headers,  verify=False)
                if r2.status_code == requests.codes.ok:

                    self.conf.set('mteam', 'last_checkin',time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))))
                    self.conf.write(open(ini_path, "r+"))

                    self.mteam_text.insert(1.0, '{},mteam签到成功。\n'.format(
                        time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                    self.mteam_log.warning('mteam签到成功。')
                else:
                    self.mteam_text.insert(1.0, '{},mteam签到失败。\n'.format(
                        time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                    self.mteam_log.warning('mteam签到失败。')
            else:
                self.mteam_text.insert(1.0, '{},mteam登录失败。\n'.format(
                    time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
                self.mteam_log.warning('mteam登录失败。')

            mteam_num += 1
            self.mteam_label_text.set(
                '最后签到:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
            t1 = float(time.time())
        # 跳出循环，停止签到
        self.mteam_text.insert(1.0, '{},mteam停止签到！\n###############\n'.format(
            time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
        self.mteam_log.warning('mteam停止签到！')


class Application(Application_ui):
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        self.master.bind("<F9>", self.Hide_Window_Cmd)
        # print('self.{}'.format(default_frame))
        # globals()['self.{}'.format(default_frame)].tkraise()
        self.mteam_frame.tkraise()



        self.level_relations = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR,
            'crit': logging.CRITICAL
        }  # 日志级别关系映射
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨

        self.mteam_log = self.Logger('{}_mteam.log'.format(time.strftime('%Y-%m-%d', time.localtime(int(time.time())))),
                                     level='warning')

        #gui启动时开始自动签到
        if mteam_run_flag==0:
            mc1 = Mteam_Checkin(mteam_username, mteam_password, mteam_login_url,
                                 mteam_checkin_url, self.mteam_text, self.mteam_label_text, self.mteam_log,
                                 mteam_interval,conf)
            mc1.start()

    def Logger(self, filename, level='info', when='D', backCount=180,
               fmt='%(asctime)s -[line:%(lineno)d] - %(levelname)s: %(message)s'):  # %(pathname)s
        logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)  # 设置日志格式
        logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount,
                                               encoding='utf-8')  # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)  # 设置文件里写入的格式
        logger.addHandler(sh)  # 把对象加到logger里
        logger.addHandler(th)
        return logger

    def exit_Cmd(self, event=None):
        # TODO, Please finish the function here!
        if askokcancel("退出", "是否退出  “签到工具”  ?"):
            self.master.destroy()

    #############################

    def mteam_checkin_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.mteam_frame.tkraise()

    def mteam_start_Cmd(self, event=None):
        # TODO, Please finish the function here!
        if mteam_run_flag==0:
            mc1 = Mteam_Checkin(mteam_username, mteam_password, mteam_login_url,
                                 mteam_checkin_url, self.mteam_text, self.mteam_label_text, self.mteam_log,
                                 mteam_interval,conf)
            mc1.start()


    def mteam_stop_Cmd(self, event=None):
        # TODO, Please finish the function here!
        global mteam_cycle_flag
        mteam_cycle_flag = 0

    def mteam_checkbutton_Cmd(self, event=None):
        # TODO, Please finish the function here!
        if self.mteam_checkVar.get() == '1':
            self.mteam_log.warning(',mteam的循环签到已取消.')
            self.mteam_text.insert(1.0, '{},mteam的循环签到已取消.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))
        elif self.mteam_checkVar.get() == '0':
            self.mteam_log.warning(',mteam的循环签到已启动.')
            self.mteam_text.insert(1.0, '{},mteam的循环签到已启动.\n'.format(
                time.strftime('%y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))

    def Hide_Window_Cmd(self, event):
        self.master.iconify()#隐藏窗体
        #Turns the window into an icon (without destroying it).
        # To redraw the window, use deiconify.
        # Under Windows, the window will show up in the taskbar.


class Checkin_App(object):
    def app_start(self):
        top = Tk()
        top.title('{}'.format('签到工具'))
        top.iconbitmap(os.path.join(os.getcwd(), 'icon.ico'))
        top.resizable(width=False, height=False)  # 窗口禁止拉伸
        # linux和windows通用的最大化
        self.w, self.h = top.maxsize()
        sw = top.winfo_screenwidth()
        sh = top.winfo_screenheight()
        x = int((sw - self.w * 0.3) / 2)
        y = int((sh - self.h * 0.4) / 2)
        width = int(self.w * 0.30)
        height = int(self.h * 0.40)
        top.geometry("{}x{}+{}+{}".format(width, height, x, y))
        top.attributes('-toolwindow', 0,  # 可设置窗口为工具栏样式
                       '-alpha', 1,  # 可设置透明度，0完全透明，1不透明。窗口内的所有内容
                       '-fullscreen', False,  # 设置全屏
                       '-topmost', False)  # 设置窗口置顶。
        top.overrideredirect(0)  # 去掉标题栏

        self.root = top
        icons = os.path.join(os.getcwd(), 'icon.ico')

        hover_text = "签到工具"  # 悬浮于图标上方时的提示
        menu_options = ()
        self.sysTrayIcon = SysTrayIcon(top, icons, hover_text, menu_options, on_quit=self.exit,
                                       default_menu_index=0)  # 把top传过去，让泪可以调用恢复界面的方法

        self.root.bind("<Unmap>", lambda event: self.Unmap() if self.root.state() == 'iconic' else False)
        self.root.protocol('WM_DELETE_WINDOW', self.exit)
        Application(top).mainloop()
        try:
            top.destroy()
        except:
            pass

    def switch_icon(self, _sysTrayIcon, icons=os.path.join(os.getcwd(), 'icon.ico')):
        _sysTrayIcon.icon = icons
        _sysTrayIcon.refresh_icon()
        # 点击右键菜单项目会传递SysTrayIcon自身给引用的函数，所以这里的_sysTrayIcon = s.sysTrayIcon

    def Unmap(self):
        self.root.withdraw()
        self.sysTrayIcon.show_icon()

    def exit(self, _sysTrayIcon=None):
        self.root.destroy()
