# 递归获取路径下所有文件名
# -*- coding: utf-8 -*-
import os
def test():
    l = []
    li=[]
    path = 'D:/codes/python/Eve_ide'
    def listdi(path, list_name,list1):  # 传入存储的list
        for file in os.listdir(path):
            #print(file)
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                listdi(file_path, list_name,list1)
            else:
                list_name.append(file_path)
                list1.append(file)
        #print(list1)
        return list_name

    name =listdi(path,l,li)
    print(l)
    print(li)
    #print(name)
test()
def read_line(name,li):
    with open(name,"r") as in_file:
        num = 0
        for line in in_file:
            num+=1
            if num ==li:
                return line

def test0():
    configure_file = "configure.txt"
    num  = 0
    for root, dirs, files in os.walk("D:/codes/python/Eve_ide/icos/t", topdown=True):
        o_p = len(read_line(configure_file,1))
        num +=1
        print(str(num)+"文件")

        for name in files:
            print(os.path.join(root, name))
        print(str(num)+"文件夹")
        for name in dirs:
            #print(name+"    this is name")

            di = name[len(name)-o_p:]
            n_m=os.path.join(root, name)
            n = len(n_m)
            m = n-o_p
            d = n_m[len(n_m)-o_p:]
            #print(name)
            #print(n)
            print(n_m)
