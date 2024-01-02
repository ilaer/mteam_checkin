#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time,configparser
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

#开始从config文件读取参数
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

class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.createWidgets()
        self.master = master

    def createWidgets(self):
        self.top = self.master

        self.style = Style()

        #
        
        self.style.configure('mteam_checkin_button.TButton', font=('微软雅黑', 10, "bold"))
        self.mteam_checkin_button = Button(
            self.top, text='mteam签到',
            command=self.mteam_checkin_Cmd,
            style='mteam_checkin_button.TButton'
        )
        self.mteam_checkin_button.place(relx=0.415, rely=0.019, relwidth=0.195, relheight=0.079)

        self.style.configure('exit.TButton', font=('微软雅黑', 10, "bold"))
        self.exit = Button(self.top, text='关闭', command=self.exit_Cmd, style='exit.TButton')
        self.exit.place(relx=0.848, rely=0.019, relwidth=0.134, relheight=0.079)

        self.style.configure('Line1.TSeparator', background='#000000')
        self.Line1 = Separator(self.top, orient='horizontal', style='Line1.TSeparator')
        self.Line1.place(relx=0., rely=0.115, relwidth=1, relheight=0.002)

       
        #######################################################
        #mteam签到的ui代码
        self.style.configure('mteam_frame.TLabelframe', font=('微软雅黑', 10))
        self.mteam_frame = Frame(self.top, style='mteam_frame.TLabelframe')
        self.mteam_frame.place(relx=0., rely=0.127, relwidth=1, relheight=0.78)

        self.style.configure('mteam_start.TButton', font=('微软雅黑', 10))
        self.mteam_start = Button(self.mteam_frame, text='启动', command=self.mteam_start_Cmd,
                                  style='mteam_start.TButton')
        self.mteam_start.place(relx=0.015, rely=0., relwidth=0.134, relheight=0.10)

        self.style.configure('mteam_stop.TButton', font=('微软雅黑', 10))
        self.mteam_stop = Button(self.mteam_frame, text='停止', command=self.mteam_stop_Cmd, style='mteam_stop.TButton')
        self.mteam_stop.place(relx=0.16, rely=0., relwidth=0.134, relheight=0.10)

        self.style.configure('mteam_Checkbutton.TCheckbutton', font=('微软雅黑', 10))
        if mteam_loop=='1':#根据config文件判断是否循环
            self.mteam_checkVar = StringVar(value='1')
        else:
            self.mteam_checkVar = StringVar(value='0')
        self.mteam_Checkbutton = Checkbutton(self.mteam_frame, text='循环', variable=self.mteam_checkVar,
                                             style='mteam_Checkbutton.TCheckbutton')
        self.mteam_Checkbutton.place(relx=0.3, rely=0., relwidth=0.134, relheight=0.1)
        self.mteam_Checkbutton.bind('<Button-1>', self.mteam_checkbutton_Cmd)

        self.style.configure('mteam_label.TLabel', anchor='w', font=('微软雅黑', 10))
        self.mteam_label_text = StringVar()
        self.mteam_label_text.set('最后签到:{}'.format(mteam_last_checkin))
        self.mteam_label = Label(self.mteam_frame, textvariable=self.mteam_label_text, style='mteam_label.TLabel')
        self.mteam_label.place(relx=0.45, rely=0., relwidth=0.534, relheight=0.1)

        # self.style.configure('mteam_line.TSeparator', background='#000000')
        # self.mteam_line = Separator(self.mteam_frame, orient='horizontal', style='mteam_line.TSeparator')
        # self.mteam_line.place(relx=0.01, rely=0.08, relwidth=0.9, relheight=0.001)

        self.mteam_text = Text(self.mteam_frame, font=('微软雅黑', 10))
        self.mteam_text.place(relx=0.013, rely=0.11, relwidth=0.96, relheight=0.909)
        self.mteam_text.insert(1.0, 'mteam\n')
        self.mteam_text.insert(1.0,
                               '{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time())))))

        self.mteam_scrollbar = Scrollbar(self.mteam_text)  # 把滚动条绑定到text
        self.mteam_scrollbar.pack(side=RIGHT, fill=Y)
        self.mteam_text['yscrollcommand'] = self.mteam_scrollbar.set
        self.mteam_scrollbar['command'] = self.mteam_text.yview
        ############################################
        self.style.configure('Line2.TSeparator', background='#000000')
        self.Line2 = Separator(self.top, orient='horizontal', style='Line2.TSeparator')
        self.Line2.place(relx=0., rely=0.92, relwidth=1, relheight=0.002)