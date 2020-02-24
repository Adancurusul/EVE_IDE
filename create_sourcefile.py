
import os
import shutil
import time

configure_file = "configure.txt"


def read_line(name, li):  # 读取指定文件指定行
    with open(name, "r") as in_file:
        num = 0
        for line in in_file:
            num += 1
            if num == li:
                return line


class move_source:
    def __init__(self, project_path):
        self.path = project_path
        self.project_main_path = self.path + '/main.c'
        self.project_source_path = self.path + '/source'
        self.project_include_path = self.path + '/include'
        self.time_now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.from_path = read_line(configure_file,5)[:-1]
        self.source_path = self.from_path+'/source'
        self.include_path = self.from_path + '/include'



    def create_empty(self):
        with open(self.project_main_path,'w') as main:
            main.write('//Created at '+self.time_now+'\n'+"//Eve ide ")



    def create_with_source(self):#创建含有source的工程
        '''
        os.mkdir(self.project_source_path)
        os.mkdir(self.project_include_path)
        shutil.copytree(self.source_path,self.project_source_path)#复制source
        shutil.copytree(self.include_path, self.project_include_path)#复制include
        '''
        '''
        上面是一个一个
        下面直接搬过来
        下午来改
        
        
        '''
        shutil.copytree(self.from_path,self.path)
        with open(self.path+'/Application/main.c','w+') as main:
            main.write('//Created at '+self.time_now+'\n'+"//Eve ide for gd32vf103")

    def create_with_main(self):#创建只有main的
        with open(self.project_main_path,'w') as main:
            main.write('//Created at '+self.time_now+'\n'+"//Eve ide for prv332")
