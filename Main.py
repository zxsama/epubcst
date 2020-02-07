#!/usr/bin/env Python
# coding = utf-8

from opencc import OpenCC
import sys
import tkinter
import os
import zipfile
import shutil
import time

def file_init_deal(file_path):
    '''  
    参数：文件路径
    处理文件路径及名称
    '''
    file_name_all = os.path.basename(file_path)
    #文件名与后缀名
    file_name_name, file_name_suffix = file_name_all.split('.')
    #输出的文件名
    file_name_deal = file_name_name + '_st.' + file_name_suffix
    #文件的文件夹路径
    file_path_dir = os.path.dirname(file_path)
    #输出文件路径
    file_path_deal = file_path_dir +"/" + file_name_deal

    #若已有同名文件，则删除
    if(os.path.exists(file_path_deal)):
        os.remove(file_path_deal)
        # print('removed')

    # （后缀名，文件夹路径，输出文件路径，原文件名）
    return [file_name_suffix, file_path_dir, file_path_deal, file_name_all]

def file_read(file_path, chunk_size=32*32):
    ''' 
    参数：文件路径，文件块大小
    读取文件
    Lazy function (generator) to read a file piece by piece.
    You can set your own chunk size
    '''
    file_ = open(file_path,'r',encoding='utf-8')
    while True:
        chunk_data = file_.read(chunk_size)
        if not chunk_data:
            break
        yield chunk_data
    file_.close()

def file_write(file_path_deal, file_converted):
    '''  
    参数：输出文件路径，文件内容
    追加写入文件
    '''
    file_w = open(file_path_deal, 'a+', encoding='utf-8')
    file_w.write(file_converted)
    file_w.flush()
    file_w.close()

def epub_read(epub_, epub_file, chunk_size=32*32):
    ''' 
    参数：已读取的压缩包，文件块大小
    读取文件
    Lazy function (generator) to read a file piece by piece.
    You can set your own chunk size
    '''    
    epub_file_ = epub_.open(epub_file,'r')
    while True:
        chunk_data = epub_file_.read(chunk_size).decode('utf-8','ignore')
        if not chunk_data:
            break
        yield chunk_data
    epub_file_.close()

def epub_write(file_w, file_converted):
    '''  
    参数：epub文件夹路径，文件内容
    创建写入文件
    '''
    file_w.write(file_converted)
    
def file_translate(file_convert_read, cc_st):
    '''
    参数：文件块，翻译方式
    繁简翻译 
    '''
    file_converted = cc_st.convert(file_convert_read)
    return file_converted

def epub_file_deal(file_path, cc_st):
    '''
    参数：文件路径
    处理equb文件  
    '''
    #读取压缩包
    epub_r = zipfile.ZipFile(file_path,'r')
    epub_namelist = epub_r.namelist()
    epub_out_path = os.path.dirname(file_path)
    epub_out_name = os.path.basename(file_path)
    epub_name_name, _ = epub_out_name.split('.')
    #中转文件路径
    epub_temp_name = 'epubcst_temp'
    epub_extr_path = epub_out_path+'/'+epub_temp_name
    #最终路径
    epub_finalname_path = epub_out_path+'/'+ epub_name_name + '_cst.epub'
    #解压文件到*/
    if(os.path.exists(epub_finalname_path)):
        os.remove(epub_finalname_path)
    elif(os.path.exists(epub_extr_path)):
        shutil.rmtree(epub_extr_path)
    epub_r.extractall(epub_extr_path)
    #筛选文件后翻译
    for epub_file_path in epub_namelist:
        try:
            _, e_staf = epub_file_path.split('.')
        except:
            continue

        epub_file = epub_r.getinfo(epub_file_path)
        epub_file_info = file_init_deal(epub_file_path)
        epub_path_dir = epub_file_info[1]
        epub_name_all = epub_file_info[3]

        epub_in_file_path = epub_path_dir+'/'+ epub_name_all
        epub_out_file_path = epub_extr_path + '/' + epub_in_file_path
        if(e_staf == "xml" or e_staf == "html" or e_staf == "xhtml" or 
        e_staf == "opf" or e_staf == "XML" or e_staf == "HTML" or 
        e_staf == "XHTML" or e_staf == "OPF" or e_staf == "txt" or e_staf == "TXT"):
            #需要翻译的文件
            if(os.path.exists(epub_out_file_path)):
                os.remove(epub_out_file_path)
            file_w = open(epub_out_file_path, 'a+', encoding='utf-8')
            for chunk in epub_read(epub_r, epub_file):
                file_converted = file_translate(chunk, cc_st)
                epub_write(file_w, file_converted)
            file_w.close()

            print(epub_in_file_path)

    # 压缩文件
    shutil.make_archive(epub_extr_path, 'zip', epub_extr_path)
    #重命名
    os.rename(epub_extr_path+'.zip', epub_finalname_path)
    epub_r.close()
    # 删除中间文件
    shutil.rmtree(epub_extr_path)



def init_opencc(cc_num):
    '''  
    参数：翻译方式选择
    确定翻译方式
    '''
    if(cc_num == 1):
        # s2t：简体中文到繁体中文
        cc_st = OpenCC('s2t')
    elif(cc_num == 2):
        # t2s：繁体中文到简体中文
        cc_st = OpenCC('t2s')   
    elif(cc_num == 3):
        # s2hk：简体中文到繁体中文（香港标准）
        cc_st = OpenCC('s2hk') 
    elif(cc_num == 4):
        # s2tw：简体中文到繁体中文（台湾标准）
        cc_st = OpenCC('s2tw') 
    elif(cc_num == 5):
        # s2twp：简体中文到繁体中文（台湾标准，带短语）
        cc_st = OpenCC('s2twp') 
    elif(cc_num == 6):
        # hk2s：繁体中文（香港标准）到简体中文
        cc_st = OpenCC('hk2s') 
    elif(cc_num == 7):
        # t2hk：繁体中文到繁体中文（香港标准）
        cc_st = OpenCC('t2hk')  
    elif(cc_num == 8):
        # t2tw：繁体中文到繁体中文（台湾标准）
        cc_st = OpenCC('t2tw') 
    elif(cc_num == 9):
        # tw2s：繁体中文（台湾标准）至简体中文
        cc_st = OpenCC('tw2s') 
    elif(cc_num == 10):
        # tw2sp：繁体中文（台湾标准）到简体中文（带短语）
        cc_st = OpenCC('tw2sp')            
    return cc_st

def file_type_check(file_info, file_path, cc_st):
    ''' 
    参数：文件信息（后缀名，文件夹路径，输出文件路径，原文件名），文件路径
    分支1：epub
    分支2：txt, html, xml,···
    '''
    file_name_suffix = file_info[0]
    file_path_dir = file_info[1]
    file_path_deal = file_info[2]

    if(file_name_suffix == 'epub' or file_name_suffix == 'EQUB'):
        # epub解包后需要转换的文件类型有xml, html, xhtml, opf
        epub_file_deal(file_path, cc_st)

    else:
        for chunk in file_read(file_path):
            file_converted = file_translate(chunk, cc_st)
            file_write(file_path_deal, file_converted)

if __name__ == "__main__":
    # cc_num = input("number")
    cc_num = 2
    cc_st = init_opencc(cc_num)
    file_path = r"C:\Users\LC\Desktop\LYH\epubcst\File\异世界狂想曲+Web.epub"
    time_start = time.time()
    file_info = file_init_deal(file_path)

    file_type_check(file_info, file_path, cc_st)
    time_end = time.time()
    print(time_end-time_start)
