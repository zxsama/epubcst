#coding=utf-8
# from tkinter import *
import tkinter as tk
import tkinter.constants
import tkinter.filedialog
from multiprocessing import Pool
import multiprocessing
from tkinter import ttk
from tkinter.filedialog import *
from MainProcessGUI import CSTProcess

#翻译方式
cc_num = 0

#创建容器
tk=tk.Tk()
tk.title("epub繁简转换(opencc)")
#固定窗口大小
tk.resizable(0,0)

fram=Frame(tk,width=460, height=135,bg='#333333')
fram.grid_propagate(0)
fram.grid()
e = Entry(fram, width = 40,fg = "#ededed",bg = '#565656',relief = FLAT, bd = 3)
e.grid(row=0, column=1, padx = 0,pady = 15)

e.delete(0, END)  # 将输入框里面的内容清空
e.insert(0, '')
filepath=StringVar()

#下拉列表样式
combostyle = ttk.Style()
combostyle.theme_create('combostyle', parent='alt',
                        settings={'TCombobox':
                            {'configure':
                                {
                                    'foreground': '#cccccc',  # 前景色
                                    'selectbackground': '#333333',  # 选择后的背景颜色
                                    'fieldbackground': '#444444',  # 下拉框颜色
                                    # 'background': 'red',  # 下拉按钮颜色
                                    'relief' : FLAT
                                }}}
                        )
combostyle.theme_use('combostyle')


def FileFound():
    '''
    获取文件路径  
    '''
    global filepath
    filepath= askopenfilename()
    # print(filepath)
    e.delete(0, END)  # 将输入框里面的内容清空
    e.insert(0, filepath)

def ChooTran(*args):   #处理事件，*args表示可变参数 
    '''  
    获取翻译方式
    '''
    get_com = combobox1.get()
    global cc_num 
    cc_num = (int)(get_com[0])
    # print(cc_num) #打印选中的值

def RunTran():
    '''  
    进行翻译
    '''
    print((str)(cc_num)+"  "+filepath)

    cst_tran = CSTProcess(cc_num)
    cst_tran.start_tran(filepath)

tkinter.Label(fram,text = "文件路径 :", fg = "#efefef", bg ='#333333', relief=FLAT).grid(row=0,column=0, padx = 0,pady = 15)
tkinter.Button(fram, text = "选择", command = FileFound,width=8,fg = "#cccccc", bg ='#232323', relief=FLAT).grid(row=0,column=2, padx = 10,pady = 15)
tkinter.Label(fram,text = "翻译方式 :", fg = "#efefef", bg ='#333333', relief=FLAT).grid(row=1,column=0, padx = 0,pady = 0)
combobox1 = ttk.Combobox(fram, width=39, values=[  '0: 简体中文到繁体中文',
                                                                        '1: 繁体中文到简体中文', 
                                                                        '2: 简体中文到繁体中文（香港标准）',
                                                                        '3: 简体中文到繁体中文（台湾标准）',
                                                                        '4: 简体中文到繁体中文（台湾标准，带短语）',
                                                                        '5: 繁体中文（香港标准）到简体中文',
                                                                        '6: 繁体中文到繁体中文（香港标准）',
                                                                        '7: 繁体中文到繁体中文（台湾标准）',
                                                                        '8: 繁体中文（台湾标准）至简体中文',
                                                                        '9: 繁体中文（台湾标准）到简体中文（带短语）'])
combobox1.grid(row=1,column=1, padx = 0,pady = 5, columnspan=1)
combobox1.current(0) 
combobox1.bind("<<ComboboxSelected>>",ChooTran)
tkinter.Button(fram, text = "转换", command = RunTran,width=8,fg = "#cccccc", bg ='#000000', relief=FLAT).grid(row=1,column=2, padx = 5,pady = 0)
tkinter.Label(fram,text = "·by zxsama", fg = "#efefef", bg ='#333333', relief=FLAT).grid(row=2,column=0, padx = 5,pady = 15)

if __name__ == "__main__":

    #多进程打包需要
    multiprocessing.freeze_support()
    
    tk.mainloop()
