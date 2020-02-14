#!/usr/bin/env Python
# coding = utf-8
#多进程
from opencc import OpenCC
from multiprocessing import Pool
import multiprocessing
import sys
import os
import zipfile
import shutil
import time
# 初始化文件路径
file_path = ''
#中转文件夹名称
epub_temp_name = 'epubcst_temp'
#初始化翻译类型
cc_num = 1
#翻译类型
CC_way = ['s2t','t2s','s2hk','s2tw','s2twp','hk2s','t2hk','t2tw','tw2s','tw2sp']

''' 
1: 简体中文到繁体中文 
2: 繁体中文到简体中文 
3: 简体中文到繁体中文（香港标准）
4: 简体中文到繁体中文（台湾标准）
5: 简体中文到繁体中文（台湾标准，带短语）
6: 繁体中文（香港标准）到简体中文
7: 繁体中文到繁体中文（香港标准）
8: 繁体中文到繁体中文（台湾标准）
9: 繁体中文（台湾标准）至简体中文
10: 繁体中文（台湾标准）到简体中文（带短语） 
'''
class CSTProcess:
    def __init__(self, cc_num):
        #多进程打包需要
        multiprocessing.freeze_support()
        #获取翻译方式  
        cc_st = OpenCC(CC_way[cc_num])
        self.cc_st = cc_st

    def start_tran(self, file_path):
        time_start = time.time()

        file_info = self.__file_init_deal(file_path)
        self.__file_type_check(file_info, file_path)
        
        time_end = time.time()
        print(time_end-time_start)
        print('complete!')
        
    def __file_init_deal(self, file_path):
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

    def __file_read(self, file_path, chunk_size=32*32):
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

    def __file_write(self, file_path_deal, file_converted):
        '''  
        参数：输出文件路径，文件内容
        追加写入文件
        '''
        file_w = open(file_path_deal, 'a+', encoding='utf-8')
        file_w.write(file_converted)
        file_w.flush()
        file_w.close()

    def __epub_read(self, epub_out_file_path_sour, chunk_size=32*32):
        ''' 
        参数：已读取的压缩包，文件块大小
        读取文件
        Lazy function (generator) to read a file piece by piece.
        You can set your own chunk size
        '''    
        epub_file_ = open(epub_out_file_path_sour,'r',encoding='utf-8')
        while True:
            chunk_data = epub_file_.read(chunk_size)
            if not chunk_data:
                break
            yield chunk_data
        epub_file_.close()

    def __epub_write(self, file_w, file_converted):
        '''  
        参数：epub文件夹路径，文件内容
        创建写入文件
        '''
        file_w.write(file_converted)
        
    def __file_translate(self, file_convert_read):
        '''
        参数：文件块，翻译方式
        繁简翻译 
        '''
        file_converted = self.cc_st.convert(file_convert_read)
        return file_converted

    def __epub_file_deal(self, file_path):
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
        epub_extr_path = epub_out_path+'/'+epub_temp_name
        #最终路径
        epub_finalname_path = epub_out_path+'/'+ epub_name_name + '_cst.epub'
        #解压文件到*/
        if(os.path.exists(epub_finalname_path)):
            os.remove(epub_finalname_path)
        elif(os.path.exists(epub_extr_path)):
            shutil.rmtree(epub_extr_path)
        epub_r.extractall(epub_extr_path)

        #繁简翻译(多进程)
        epub_list_r = []
        for e_lsit in epub_namelist:
            epub_list_r.append([e_lsit, epub_extr_path])  
        epub_pool = Pool(20)
        for epub_file_path_r in epub_list_r:
            epub_pool.apply_async(self.epub_run_process, args=(epub_file_path_r,))
        epub_pool.close()
        epub_pool.join()

        epub_r.close()
        # 压缩文件
        shutil.make_archive(epub_extr_path, 'zip', epub_extr_path)
        #重命名
        os.rename(epub_extr_path+'.zip', epub_finalname_path)
        # 删除中间文件
        shutil.rmtree(epub_extr_path)

    def epub_run_process(self, epub_file_path_r):
        '''
        并发任务  
        '''
        # print(epub_file_path_r)
        epub_file_path = epub_file_path_r[0]
        epub_extr_path = epub_file_path_r[1]
        # cc_st = epub_file_path_r[2]
        try:
            _, e_staf = epub_file_path.split('.')
        except:
            return -1
        epub_file_info = self.__file_init_deal(epub_file_path)
        epub_path_dir = epub_file_info[1]
        epub_name_all = epub_file_info[3]
        #源文件路径
        epub_in_file_path_sour = epub_path_dir+'/'+ epub_name_all
        epub_out_file_path_sour = epub_extr_path + '/' + epub_in_file_path_sour
        #翻译文件路径
        epub_in_file_path = epub_path_dir+'/_CSTTEMP_'+ epub_name_all
        epub_out_file_path = epub_extr_path + '/' + epub_in_file_path

        if(e_staf == "xml" or e_staf == "html" or e_staf == "xhtml" or 
        e_staf == "opf" or e_staf == "XML" or e_staf == "HTML" or 
        e_staf == "XHTML" or e_staf == "OPF" or e_staf == "txt" or e_staf == "TXT"):
            #file_w写入的文件
            file_w = open(epub_out_file_path, 'a+', encoding='utf-8')
            for chunk in self.__epub_read(epub_out_file_path_sour):
                file_converted = self.__file_translate(chunk)
                self.__epub_write(file_w, file_converted)
            file_w.close()
            os.remove(epub_out_file_path_sour)
            os.rename(epub_out_file_path, epub_out_file_path_sour)
            print(epub_in_file_path)  

    # def __init_opencc(self, cc_num):
    #     '''  
    #     参数：翻译方式选择
    #     确定翻译方式
    #     '''      
    #     nonlocal cc_st
    #     if(cc_num == 1):
    #         # s2t：简体中文到繁体中文
    #         cc_st = OpenCC('s2t')
    #     elif(cc_num == 2):
    #         # t2s：繁体中文到简体中文
    #         cc_st = OpenCC('t2s')   
    #     elif(cc_num == 3):
    #         # s2hk：简体中文到繁体中文（香港标准）
    #         cc_st = OpenCC('s2hk') 
    #     elif(cc_num == 4):
    #         # s2tw：简体中文到繁体中文（台湾标准）
    #         cc_st = OpenCC('s2tw') 
    #     elif(cc_num == 5):
    #         # s2twp：简体中文到繁体中文（台湾标准，带短语）
    #         cc_st = OpenCC('s2twp') 
    #     elif(cc_num == 6):
    #         # hk2s：繁体中文（香港标准）到简体中文
    #         cc_st = OpenCC('hk2s') 
    #     elif(cc_num == 7):
    #         # t2hk：繁体中文到繁体中文（香港标准）
    #         cc_st = OpenCC('t2hk')  
    #     elif(cc_num == 8):
    #         # t2tw：繁体中文到繁体中文（台湾标准）
    #         cc_st = OpenCC('t2tw') 
    #     elif(cc_num == 9):
    #         # tw2s：繁体中文（台湾标准）至简体中文
    #         cc_st = OpenCC('tw2s') 
    #     elif(cc_num == 10):
    #         # tw2sp：繁体中文（台湾标准）到简体中文（带短语）
    #         cc_st = OpenCC('tw2sp')            
    #     return cc_st

    def __file_type_check(self, file_info, file_path):
        ''' 
        参数：文件信息（后缀名，文件夹路径，输出文件路径，原文件名），文件路径
        分支1：epub
        分支2：txt, html, xml,···
        '''
        file_name_suffix = file_info[0]
        file_path_deal = file_info[2]

        if(file_name_suffix == 'epub' or file_name_suffix == 'EPUB'):
            # epub解包后需要转换的文件类型有xml, html, xhtml, opf
            self.__epub_file_deal(file_path)

        else:
            for chunk in self.__file_read(file_path):
                file_converted = self.__file_translate(chunk)
                self.__file_write(file_path_deal, file_converted)
