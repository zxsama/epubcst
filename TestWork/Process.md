
opencc
> https://github.com/BYVoid/OpenCC

安装opencc出错
```
    ERROR: Command errored out with exit status 1:
     command: 'C:\Users\LC\AppData\Local\Programs\Python\Python38\python.exe' -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'C:\\Users\\LC\\AppData\\Local\\Temp\\pip-install-o08ri5eh\\opencc\\setup.py'"'"'; __file__='"'"'C:\\Users\\LC\\AppData\\Local\\Temp\\pip-install-o08ri5eh\\opencc\\setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' egg_info --egg-base 'C:\Users\LC\AppData\Local\Temp\pip-install-o08ri5eh\opencc\pip-egg-info'  
         cwd: C:\Users\LC\AppData\Local\Temp\pip-install-o08ri5eh\opencc\
    Complete output (7 lines):
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "C:\Users\LC\AppData\Local\Temp\pip-install-o08ri5eh\opencc\setup.py", line 19, in <module>
        long_description=fread('README.rst'),
      File "C:\Users\LC\AppData\Local\Temp\pip-install-o08ri5eh\opencc\setup.py", line 10, in fread
        return f.read()
    UnicodeDecodeError: 'gbk' codec can't decode byte 0x80 in position 462: illegal multibyte sequence
    ----------------------------------------
ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
```

尝试了
```
python -m pip install --upgrade setuptools
```

尝试无果后改用，github 的opencc-python 
https://github.com/yichen0831/opencc-python/tree/master/opencc
> opencc-python 是用純 Python 所寫，使用由 BYVoid(byvoid.kcp@gmail.com) 所開發的 OpenCC 中的字典檔案。 opencc-python 可以支援 Python2.7 及 Python3.x。

安装
```
pip install opencc-python-reimplemented
```

python
重命名
os.rename
shutil.move

压缩文件
shutil.make_archive
读取压缩文件
epub_r = zipfile.ZipFile(file_path,'r')
获取压缩文件列表
epub_r.namelist()
删除文件shutil.retree()

