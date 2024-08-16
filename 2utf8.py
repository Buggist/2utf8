"""
指定目录内的全部文本文件的编码格式转换为 UTF-8。

依赖库【python-magic】存在不支持中文的BUG，需要对该库进行修改，否则无法正常识别中文文件名。
具体修改方法在相应个人技术文档中已经列出。

修改方法摘录如下（python-magic - bin版）：

    site-packages/magic/magic.py    （如果是在Linux/MacOS上安装的非bin版，则为site-packages/magic/__init__.py）

    查找【def coerce_filename(filename):】

    将代码块内的 'utf-8' 改为 'gbk'

"""
import sys, os
import chardet
import codecs
import magic



def is_text_file(file_path):
    #----工作路径变更--
    alter_path = file_path[:file_path.rfind("\\")]
    current_dir = os.getcwd()
    os.chdir(alter_path)
    #--
    file_name = file_path.split("\\")[-1]
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(file_name)
    #----工作路径复原--
    os.chdir(current_dir)
    #--
    return mime_type.startswith('text')


def convert_to_utf8(file_path):
    """ 将指定文件编码转换为 UTF-8. """
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding != 'utf-8':
            with codecs.open(file_path, 'r', encoding) as f:
                text = f.read()
            with codecs.open(file_path, 'w', 'utf-8') as f:
                f.write(text)
            print(f'{file_path} 已转换为utf-8编码')
        else:
            print(f'{file_path} 已经是utf-8编码')


def search(dir_):
    items = os.listdir(dir_)
    for item in os.listdir(dir_):
        path = os.path.join(dir_, item)
        if os.path.isfile(path):
            if is_text_file(path):
                convert_to_utf8(path)
            else:
                print(f'{path} 不是文本类型======')
                continue
        elif os.path.isdir(path):
            search(path)
        else:
            print(f'{path} 不是【文件】或【目录】======')
            continue


if __name__ == "__main__":
    current_dir = os.getcwd()
    
    search(current_dir)
    os.system("pause")
    
        
