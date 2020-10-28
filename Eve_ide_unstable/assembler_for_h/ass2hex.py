#############################################################
#this is the first test of the prv32ide
#author Adancurusul
#2019.11.6
#这个版本内核支持几乎所有riscv ia指令的翻译和汇编地址的分配
#此汇编器中在算法上进行重构使之与现有的大部分汇编器的两遍扫描算法不同
#使用一遍扫描算法同时配上散列算法进行地址分配
#使将汇编翻译成hex的速度更快
#同时预留多个接口可以从中提取2进制文件方便对自研处理器的验证工作
#该内核可直接用于prv332ide的图形界面
#
##############################################################

import re
import array

#str00 = 'addi x  7,x0,0x0008;asdfja;;21,,,,'


global_label_data_dict = {}

base = [str(x) for x in range(10)] + [ chr(x) for x in range(ord('A'),ord('A')+6)]


'''
下面几个用于进制之间的转换，
输入输出格式均为str




'''
def dec2bin(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 2)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

def dec2hex(string_num):
    num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])

def hex2dec(string_num):
    return str(int(string_num.upper(), 16))

def hex2bin(string_num):
    return dec2bin(hex2dec(string_num.upper()))

def bin2hex(string_num):

    num = int(string_num,2)
    #num = int(string_num)
    mid = []
    while True:
        if num == 0: break
        num,rem = divmod(num, 16)
        mid.append(base[rem])

    return ''.join([str(x) for x in mid[::-1]])
#def bin2hex(self.string_num):
#   return dec2hex(bin2dec(string_num))










'''
下面这个类用于对汇编代码整行的分割
返回一个字典：
opcode ：使用的操作码

key：操作码后的数据


'''




class split_str:#can return as dict like{'opcode': 'addi', 'key': 'x7,x0,0x0008'}
    #正则表达式
    parttern_code = r'^\s*(?P<opcode>\w+)\b\s+(?P<key>.+)(;|#)?'#匹配汇编并拆分
    def __init__(self,str0):
        self.st = ''.join(str0.split())
        self.str0 = str0.split(';')[0]#分出代码区和注释区
        #print(self.str0)
        self.comma_count()
        self.code_split()
        self.dict_of_ass=self.code_split()
        self.change_to()

    def change_to(self):
            if(self.dict_of_ass):
                self.dict_of_ass['key'] =''.join(self.dict_of_ass['key'].split())
                self.opcode = self.dict_of_ass['opcode']
                self.key = self.dict_of_ass['key'].split(',')
            else:
                print('no')#去除空格
    def comma_count(self):#找到逗号的个数个数
        self.count = self.str0.count(',')
        print(self.count)
    def code_split(self):
        self.str0 = self.str0.lower()
        self.result = re.match(self.parttern_code,self.str0)
        if (self.result):
            self.opcode = self.result.group('opcode')
            self.str_key = self.result.group('key')
            self.dict ={'opcode':self.opcode,'key':self.str_key}#创建字典保存分割后的字符串

            return self.dict

        else :
            return None
'''
该类的使用方法
str = 'addi x  7,x0,0x0008;asdfja;;21,,,,'
l = split_str(str)
print(l.dict_of_ass)#{'opcode': 'addi', 'key': 'x7,x0,0x0008'}
'''


'''

下面那个可以用于转化为二进制
继承了上面的split类
先将数据分割后根据操作码来转化




'''



class change_into_bin(split_str):#直接将每行完成转化
    def __init__(self,str0):#继承split的属性
        super().__init__(str0)
        self.list = []
        self.list.append(self.opcode)
        self.list = self.list+self.key
        self.change_and_return()

    def change16(self,wei,str1):#将16进制数转化为二进制
        print(str1)
        q = int(str1,16)
        return str(bin(q))[2:].zfill(wei)
        #Zero = int(wei-len(a))
        #s = '0'*Zero+a


    def change(self, wei, str1):  # 将寄存器值转化出来
        return str(bin(int(str1[1:])))[2:].zfill(wei)

    '''
    2019.11.6这里改为支持10以上
    也不知道当时咋想的。。。。。。




    '''
    '''
    def change16(self,wei,str1):
        q = int(str1,16)
        a  = str(bin(q))[2:].zfill(wei)
        #Zero = int(wei-len(a))
        #s = '0'*Zero+a
        return a
    def change(self,wei,str1):
        a = str(bin(int(str1[-1])))[2:].zfill(wei)
        return a
    '''

    def do_with_fucking_csr(self,str11):#fucking csr!!!!fuck!!!!!!
        str1 = str11.lower()

        csr_head = {

            'mstatus':hex2bin('300').zfill(12),
            'mie':hex2bin('304').zfill(12),
            'mtvee':hex2bin('305').zfill(12),
            'mscratch':hex2bin('340').zfill(12),
            'mepc':hex2bin('341').zfill(12),
            'mcause':hex2bin('342').zfill(12),
            'mtval':hex2bin('343').zfill(12),
            'mbadaddr':hex2bin('343').zfill(12),
            'mip':hex2bin('344').zfill(12),


        }
        return csr_head[str1]()
    def do_with_fucking_label(self,str0):#fuuuuuucking
        global global_label_data_dict
        self.hex_location = dec2bin(global_label_data_dict[str0]).zfill(12)






    def change_and_return(self):

        head = {#这是一个操作码的指向字典来模拟switch语句
            'addi':self.ADDI,
            'lui':self.LUI,
            'auipc':self.AUIPC,
            'jal':self.JAL,
            'jalr':self.JALR,
            'beq':self.BEQ,
            'bne':self.BNE,
            'blt':self.BLT,
            'bge':self.BGE,
            'bltu':self.BLTU,
            'bgeu':self.BGEU,
            'lb':self.LB,
            'lh':self.LH,
            'lw':self.LW,
            'lbu':self.LBU,
            'lhu':self.LHU,
            'sb':self.SB,
            'sh':self.SH,
            'sw':self.SW,
            'slti':self.SLTI,
            'sltiu':self.SLTIU,
            'xori':self.XORI,
            'ori':self.ORI,
            'andi':self.ANDI,
            'slli':self.SLLI,
            'srli':self.SRLI,
            'srai':self.SRAI,
            'add':self.ADD,
            'sub':self.SUB,
            'sll':self.SLL,
            'slt':self.SLT,
            'sltu':self.SLTU,
            'xor':self.XOR,
            'srl':self.SRL,
            'sra':self.SRA,
            'or':self.OR,
            'and':self.AND,
            #'fence':FENCE,
            'fence.i':self.FENCE_I,
            'ecall':self.ECALL,
            'ebreak':self.EBREAK,
            'cssrrw':self.CSRRW,
            'csrrs':self.CSRRS,
            'csrrc':self.CSRRC,
            'csrrwi':self.CSRRWI,
            'csrrsi':self.CSRRSI,
            'csrrci':self.CSRRCI,

        }
        self.after_change_str = head[self.list[0]]()


        print(self.after_change_str)





    def ADDI(self):

        st = self.change16(12,self.list[3])+self.change(5,self.list[2])+'000'+self.change(5,self.list[1])+'0010011'
        return st
    def SLTI(self):
        st = self.change16(12,self.list[3])+self.change(5,self.list[2])+'010'+self.change(5,self.list[1])+'0010011'
        return st
    def SLTIU(self):
        st = self.change16(12,self.list[3])+self.change(5,self.list[2])+'011'+self.change(5,self.list[1])+'0010011'
        return st
    def ANDI(self):
        st = self.change16(12,self.list[3])+self.change(5,self.list[2])+'111'+self.change(5,self.list[1])+'0010011'
        return st
    def ORI(self):
        st = self.change16(12,self.list[3])+self.change(5,self.list[2])+'110'+self.change(5,self.list[1])+'0010011'
        return st
    def XORI(self):
        st = self.change16(12,self.list[3])+self.change(5,self.list[2])+'100'+self.change(5,self.list[1])+'0010011'
        return st
    def SLLI(self):
        st = '0000000'+self.change16(5,self.list[-1])+self.change(5,self.list[2])+'001'+self.change(5,self.list[1])+'0010011'
        return st
    def SRLI(self):
        st = '0000000'+self.change16(5,self.list[-1])+self.change(5,self.list[2])+'101'+self.change(5,self.list[1])+'0010011'
        return st
    def SRAI(self):
        st = '0100000'+self.change16(5,self.list[-1])+self.change(5,self.list[2])+'101'+self.change(5,self.list[1])+'0010011'
        return st
    def ADD(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'000'+self.change(5,self.list[1])+'0110011'
        return st
    def SUB(self):
        st = '0100000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'000'+self.change(5,self.list[1])+'0110011'
        return st
    def SLL(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'001'+self.change(5,self.list[1])+'0110011'
        return st
    def SLT(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'010'+self.change(5,self.list[1])+'0110011'
        return st
    def SLTU(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'011'+self.change(5,self.list[1])+'0110011'
        return st
    def XOR(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'100'+self.change(5,self.list[1])+'0110011'
        return st
    def SRL(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'101'+self.change(5,self.list[1])+'0110011'
        return st
    def SRA(self):
        st= '0100000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'101'+self.change(5,self.list[1])+'0110011'
        return st
    def OR(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'110'+self.change(5,self.list[1])+'0110011'
        return st
    def AND(self):
        st = '0000000'+self.change(5,self.list[-1])+self.change(5,self.list[2])+'111'+self.change(5,self.list[1])+'0110011'
        return st
    def LUI(self):
        st = self.change16(20,self.list[-1])+self.change(5,self.list[1])+'0110111'
        return st
    def AUIPC(self):
        st = self.change16(20,self.list[-1])+self.change(5,self.list[1])+'0010111'
        return st
    def JAL(self):
        st = self.change16(20,self.list[-1])+self.change(5,self.list[1])+'1101111'
        return st
    def JALR(self):
        st = self.change16(12,self.list[-1])+self.change(5,self.list[2])+'000'+self.change(5,self.list[1])+'1100111'
        return st
    def BEQ(self):
        s = self.change16(12,self.list[-1])
        st1 = s[0:7]
        st2 = s[7:12]
        st = st1 +self.change(5,self.list[2])+self.change(5,self.list[1])+'000'+st2+'1100011'
        return st
    def BNE(self):
        s = self.change16(12,self.list[-1])
        st1 = s[0:7]
        st2 = s[7:12]
        st = st1 +self.change(5,self.list[2])+self.change(5,self.list[1])+'001'+st2+'1100011'
        return st
    def BLT(self):
        s = self.change16(12,self.list[-1])
        st1 = s[0:7]
        st2 = s[7:12]
        st= st1 +self.change(5,self.list[2])+self.change(5,self.list[1])+'100'+st2+'1100011'
        return st
    def BGE(self):
        s = self.change16(12,self.list[-1])
        st1 = s[0:7]
        st2 = s[7:12]
        st = st1 +self.change(5,self.list[2])+self.change(5,self.list[1])+'101'+st2+'1100011'
        return st
    def BLTU(self):
        s = self.change16(12,self.list[-1])
        st1 = s[0:7]
        st2 = s[7:12]
        st = st1 +self.change(5,self.list[2])+self.change(5,self.list[1])+'110'+st2+'1100011'

        return st
    def BGEU(self):
        s = self.change16(12,self.list[-1])
        st1 = s[1:7]
        st2 = s[7:12]
        st = st1 +self.change(5,self.list[2])+self.change(5,self.list[1])+'111'+st2+'1100011'
        return st
    def LW(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        st = self.change16(12,l1[0])+self.change(5,t)+'010'+self.change(5,self.list[1])+'0000011'
        return st
    def LH(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        str = self.change16(12,l1[0])+self.change(5,t)+'001'+self.change(5,self.list[1])+'0000011'
        return str


    def LB(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        st = self.change16(12,l1[0])+self.change(5,t)+'000'+self.change(5,self.list[1])+'0000011'
        return st
    def LHU(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        st = self.change16(12,l1[0])+self.change(5,t)+'101'+self.change(5,self.list[1])+'0000011'
        return st
    def LBU(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        str = self.change16(12,l1[0])+self.change(5,t)+'100'+self.change(5,self.list[1])+'0000011'
        return str
    def SW(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        s = self.change16(12,l1[0])
        st =s[0:7] +self.change(5,self.list[1])+self.change(5,t)+'010'+s[7:12]+'0100011'
        return st
    def SH(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        s = self.change16(12,l1[0])
        st =s[0:7] +self.change(5,self.list[1])+self.change(5,t)+'001'+s[7:12]+'0100011'
        return st
    def SB(self):
        l1 =self.list[2].partition("(")
        t = l1[-1][0:-1]
        s = self.change16(12,l1[0])
        st =s[0:7] +self.change(5,self.list[1])+self.change(5,t)+'000'+s[7:12]+'0100011'
        return st
    def CSRRW(self):
        st = self.do_with_fucking_csr(self.list[-2])+self.change(5,self.list[-1])+'001'+self.change(5,self.list[1])+'1110011'
        return st
    def CSRRS(self):
        st = self.do_with_fucking_csr(self.list[-2])+self.change(5,self.list[-1])+'010'+self.change(5,self.list[1])+'1110011'
        return st
    def CSRRC(self):
        st = self.do_with_fucking_csr(self.list[-2])+self.change(5,self.list[-1])+'011'+self.change(5,self.list[1])+'1110011'
        return st
    def CSRRWI(self):
        st = self.do_with_fucking_csr(self.list[-2])+self.change16(5,self.list[-1])+'101'+self.change(5,self.list[1])+'1110011'
        return st
    def CSRRCI(self):
        st = self.do_with_fucking_csr(self.list[-2])+self.change(5,self.list[-1])+'111'+self.change(5,self.list[1])+'1110011'
        return st
    def CSRRSI(self):
        st = self.do_with_fucking_csr(self.list[-2])+self.change(5,self.list[-1])+'110'+self.change(5,self.list[1])+'1110011'
        return st
    def FENCE_I(self):
        st = '00000000000000000001000000001111'
        return st
    def ECALL(self):
        st = '00000000000000000000000001110011'
        return st
    def EBREAK(self):
        st = '00000000000100000000000001110011'
        return st

'''
类用法：
l = change_into_bin(str00)
print(l.after_change_str)
'''



class check_label_or_opcode():#check if it is label or opcode
    parttern_label = r'.section\s+'
    parttern_section = r''
    parttern_data = r''
    parttern_text = r''

    def __init__(self,str0):
        self.str0 = str0

    def if_label(self):
        re.match(self.parttern_label,self.str0)
    #def if_section(self):
     #   se = re.match(self.parttern_section,self.str0)
        #if (se):


'''
主要扫描方式：
1遍扫描
先给定义的量以及函数分配位置
利用字典查找
'''




class do_scan():#扫描类
    label_times =0#label出现次数
    defin_times = 0#定义出现次数
    label_lines = 0  #每个label下行数
    data_lines = 0#data的长度
    data_scan =0  #地址标志位
    line_of_file = 0
    label_scan = 0
    parttern_label = r'^(\w+)[:]$'#检测是不是label
    parttern_section = r''#检测是不是函数
    data_dict = {}
    label_data_dict = {}
    data_list = []
    parttern_data = r'(\w+\s*) [:] (.+)'# 检测data
    parttern_text = r'\w+'
    parttern_define=r''
    partterna = r'\s{0,}[.section]+[.]+(.+)'
    flag = 0#检测每个代码段的边缘
    label_flag =0
    size_of_label = {}#每个label大小
    size_of_data = {}#每个data大小
    check = 0
    no_label = 1
    name_of_label = ''
    section_change =0
    stored_or_not = 0
    first_label = 0
    def __init__(self,filename):#得到文件名对其每行进行遍历
        self.filename = filename
        with open(self.filename,'r+') as self.file:#打开文件
            self.scan_first()    #做第一次扫描

    def scan_first(self):#第一次扫描函数（扫描主函数）
        for line in self.file:

            self.line_of_file +=1
            self.str0 = line.lstrip()
            print('str0:',self.str0)
            if self.str0 :#如果不是空的行
                self.if_label()
                if self.data_scan  :#为data段
                    self.scan_data()
                elif self.label_scan :#为label段
                    self.label_store()
        return self.data_dict , self.label_data_dict

    def scan_data(self):#data段的储存
        self.dataname = re.match(self.parttern_data,self.str0)

        if (self.dataname):#找到data名字
            print('b')
            self.name_of_data = self.dataname.group(1)
            self.name_of_data= ''.join(self.name_of_data).split()[0]#去除空格
            #print(self.name_of_data)
            self.data_of_data =self.dataname.group(2)
            self.data_of_data= ''.join(self.data_of_data).split()[0]#草草草草草这nm又忘了取第一个卧槽
            print('data',self.data_of_data)
            self.count_a = self.data_of_data.count(',')
            print("count",self.count_a)
            if self.count_a>0:#一次定义多个数
                self.datalist = self.data_of_data.split(',')
                #print('datalist',self.datalist)
                self.if_more_define = 1
            else :#一次定义单个数
                self.if_more_define = 0
                self.data_list = self.data_of_data

            self.data_count = self.count_a + 1
            self.h = self.size_of_data.setdefault(self.name_of_data,self.data_count)#将地址大小存入dict
            self.m = self.data_dict.setdefault(self.name_of_data,self.datalist)#将得到的data丢入存放data的字典
            #print('datalist',self.data_dict)
            #此处修改为将


    def label_store(self):#将label 移入字典
        print('lab_store')
        self.labelname = re.match(self.parttern_label,self.str0)
        self.label_check = re.match(self.partterna,self.str0)

        '''
        if self.label_check:
           pass

            if self.first_label:

                if not self.stored_or_not:
                    self.n = self.label_data_dict.setdefault(self.name_of_label,self.data_list)
                    self.o = self.size_of_label.setdefault(self.name_of_label,self.label_lines)
                    print(self.label_data_dict)
                    print('*'*20)
            else:
                self.first_label = 1

        else:
            '''
        if(self.labelname):
            print('getgetfucking'*5)


        if( self.labelname and  self.check):#无label定义前的代码处理
            print('c')
            self.no_label =0
            self.n = self.label_data_dict.setdefault(self.name_of_label,self.data_list)
            self.o = self.size_of_label.setdefault(self.name_of_label,self.label_lines)
            self.label_lines = 0
            self.data_list = []
            self.name_of_label = self.labelname.group(1)
        elif ( self.labelname and  self.check):#无label定义前无代码
            self.no_label = 0
            self.stored_or_not = 0

        elif (self.labelname and not self.label_flag and not self.no_label):#找到label
            self.stored_or_not = 0
            print('find label')
            self.label_flag = 1
            self.name_of_label = self.labelname.group(1)
        elif not self.labelname and self.label_flag and not self.no_label :
            self.stored_or_not = 0
            print('fuuuuuuck')
            self.label_lines += 1  #label行数加一
            self.data_list.append(self.str0)#将该行加入list
        elif (self.labelname and self.label_flag and not self.no_label  ):#label切换点
            print('change_label')

            #self.label_lines = str(self.label_lines)#以字符串存入
            self.n = self.label_data_dict.setdefault(self.name_of_label,self.data_list)
            self.o = self.size_of_label.setdefault(self.name_of_label,self.label_lines)
            self.label_lines = 0
            self.stored_or_not = 1
            self.data_list = []#清空列表以储存下一次
            self.name_of_label = self.labelname.group(1)
        elif self.no_label:#如果是之前没有定义label
            self.stored_or_not = 0
            print('no_label')
            self.no_label = 0
            self.check = 1
            self.label_flag = 1
            self.name_of_label = 'first_of_labels'
            #self.data_list.append(self.str0)
        else:
            print('nothing')





    def if_label(self):

        self.my_label = 'label'
        #self.change = re.match(self.partterna,self,str0)
        #if  self.change:
        #    self.section_change = 1


        self.label_check = re.match(self.partterna,self.str0)
        if (self.label_check):
            self.data_or_text = self.label_check.group(1)
            if (self.data_or_text=='data' and not self.flag ):
                self.data_scan = 1
                self.label_scan = 0
                self.flag =1
                print('get_data')

            elif (self.data_or_text == 'text' and not self.flag):#guguguugugugugugguguguguguguugu
                self.flag = 1
                self.label_scan = 1
                self.data_scan = 0
                print('get_label')



            elif (self.data_or_text=='text' and self.flag):
                if not self.stored_or_not:
                    self.h = self.size_of_data.setdefault(self.name_of_data,self.data_count)#将地址大小存入dict
                    self.m = self.data_dict.setdefault(self.name_of_data,self.datalist)
                    print('*'*20)
                self.data_scan = 0
                self.label_scan = 1
                self.flag = 1
                print('change')
                '''
                下面有问题
                '''


            elif (self.data_or_text=='data' and self.flag):
                if not self.stored_or_not:
                    self.n = self.label_data_dict.setdefault(self.name_of_label,self.data_list)
                    self.o = self.size_of_label.setdefault(self.name_of_label,self.label_lines)
                    print(self.label_data_dict)
                    print('*//'*20)
                self.label_scan = 0
                self.data_scan =1
                self.flag = 1
                print('change')


        else :
            pass

            #self.give_location(self.label_check.group(0),self.my_label)

            #return self.label_check.group(0)
    def if_define(self):
        self.mydefine = 'define'
        self.define_check = re.match(self.parttern_define,self.str0)
        if (self.define_check):
            #self.give_location(self.define_check.group(0),"define")
            return self.define_check.group(0)





'''
该类阔以利用一遍扫描算法得到data和text的字典

用法
data_dict,label_dict = do_scan(file)


'''



class change_into_hex(do_scan):
    '''
    label_location_dict，data。。。。用于之后的翻译器查找
    locationdict直接存放地址和对应的东西



    '''

    location_dict = {}#用于存放每个地址以及对应的01010
    label_location_dict ={}#用于后面转化汇编代码时直接找label
    data_location_dict = {}
    start_position = 0x0000
    data_start_position = 0x0000
    #flag = 0
    line = 0
    def __init__(self,filename,save_location):#继承do_scan的属性
        super().__init__(filename)
        #print('type',type(self.data_start_position))
        print(self.data_start_position)
        self.save_location = save_location
        self.data = self.data_dict
        self.label = self.label_data_dict
        #self.size_of_label = {}#每个label大小
        #self.size_of_data = {}#每个data大小
        #
        self.give_location()
        self.do_fucking_change()



        #下面一段很可能有个问题


        #明天记得调





    def give_location(self):#给每个data以及函数分配地址

        print('sizelabel',self.size_of_label)
        if self.size_of_label:
            for name in self.size_of_label.keys():
                print('xxcxc'*10)
                self.o = self.label_location_dict.setdefault(name,self.start_position)#将label和起始地址存入dict
                self.increase = int(4*self.size_of_label[name])
                #self.increase = 0x0001

                self.start_position  =  self.increase +self.start_position #给开始地址加入相应地址
                print('start po: ',self.start_position)
                #self.start_position = str(self.start_position[2:]).zfill(4)#四位对其
            self.o = self.label_location_dict.setdefault(name,hex(self.start_position))#将label和起始地址存入dict
        if self.size_of_data:
            #print('okokok'*10)

            self.data_start_position = self.start_position +self.data_start_position #将label段末地址赋给data段初始地址
            '''
            话撂这了，不回来改这一段算我输好吧，绝壁要改 
            '''
            for name in self.size_of_data.keys():
                self.o = self.data_location_dict.setdefault(name,self.data_start_position)
                #self.o = self.data_location_dict.setdefault(name,self.data_start_position)#将data存入dict
                self.data_increase = int(4*self.size_of_data[name])
                #print('data_increase',type(self.data_increase))
                print('start_position',self.data_start_position)
                self.data_start_position += self.data_increase#给data地址加入地址
                self.data_start_position =hex(self.data_start_position)
                print(self.data_start_position)
                #self.o = self.data_location_dict.setdefault(name,self.data_start_position)
                #self.data_start_position = str(self.data_start_position[2:]).zfill(4)
            self.o = self.data_location_dict.setdefault(name,self.data_start_position)
            #self.o = self.data_location_dict.setdefault(name,self.data_start_position)
            print('fuuuuck',self.data_location_dict)
        '''


        '''

    def check_check(self,DD):
        length=len(DD)  #求长度

        #创建一个list，将传入的str的每两个数合在一起，再求和
        list1=[]
        if(length%2==1):    #如果str长度为单数，则抛出错误
            print('数据长度有误')
        else:
            for i in range(0, length, 2):  #range（开始，结束-1，每次加多少）  这里即0——length-1  每次循环i+2
                hex_digit=DD[i:i + 2]      #将传入的str的每两个数合在一起
                list1.append('0x'+hex_digit)    #再每个字符前+0x  但是它仍然是字符，但更便于下面通过int(list1[i], 16)转换成16进制
        print(list1)

        sum=0
        for i in range(int(length/2)):   #求和
            sum=int(list1[i], 16)+sum      #int(list1[i], 16)将16进制转换成10进制 int类型
        sum=sum%256
        sum=256-sum

        #print('校验码: '+hex(sum))   #将sum和结果转换成16进制  hex(sum)
        return dec2hex(sum)

    def do_fucking_change(self):#do the fucking change !!!!!!fuck!!!我他妈好困！！！！操
        global global_label_data_dict
        if self.label_data_dict:
            print('a')
            for name in self.label_data_dict.keys():#获取label
                print('fucktadfaasf',name,self.label_data_dict[name])
                for i in range(len(self.label_data_dict[name])):#得到label下的每行
                    self.lines_in_label =self.label_data_dict[name][i]#依次获取每一行
                    self.changed = change_into_bin(self.lines_in_label)#利用转化类进行转化

                    self.chan = bin2hex(self.changed.after_change_str).zfill(8)
                    print('changed'*10,self.chan)
                    self.high = self.chan[0:2]
                    self.high2 = self.chan[2:4]
                    self.low2 = self.chan[4:6]
                    self.low = self.chan[6:]#高低位互换
                    self.word = self.low+self.low2+self.high2+self.high#互换后的16进制数
                    self.location = self.label_location_dict[name] #得到函数初始地址
                    global_label_data_dict = self.label_location_dict
                    print('aaa'*15,self.label_location_dict)
                    print('地址',self.location)
                    self.location += i*4  #换算出当前地址值操操操
                    #这个狗逼东西没有转化成16进制操操操
                    self.location = dec2hex(str(self.location) )

                    print('location',self.location)
                    self.load = self.location_dict.setdefault(self.location,self.word)#存放进地址-数据字典
        if self.data_location_dict:

            for name in self.data_location_dict.keys():
                #for i in range(len(self.data_dict[name])):
                print('a')
                if str(type(self.data_dict[name])) == "<class 'list'>":#如果一次定义多个数据#10.20做修改为找到其数据类型从而判断
                    #print('b',self.data_dict)
                    #self.list_of_data =self.data_dict[name].split(',')#依次获取每一行 10.20改做直接获取列表
                    for i in range(0,len(self.data_dict[name])):
                        self.str_of_data = self.data_dict[name][i][2:]#获取data的值

                        #print('dddddd',self.str_of_data)
                        self.high = self.str_of_data[0:2]
                        self.low = self.str_of_data[2:]#高低位互换
                        self.word = self.low+self.high
                        self.location = self.data_location_dict[name]+i*2
                        #print('操',self.location)
                        #self.location += dec2hex(str(hex(i)*4))#记住加str“”
                        self.load = self.location_dict.setdefault(self.location,self.word)
                else:
                    self.str_of_data = self.data_dict[name][2:]
                    self.low = self.str_of_data[2:]#高低位互换
                    self.word = self.low+self.high
                    self.location = self.data_location_dict[name]
                    #print('操',self.location)
                    #self.location += dec2hex(str(hex(i)*4))#记住加str“”
                    self.load = self.location_dict.setdefault(self.location,self.word)

    '''
    是否直接05出函数开始地址有待继续研究
    '''
    def write_hex(self):#写入hex
        with open(self.save_location,"w+") as sl:#打开待生成的hex
            self.firstr_to_write =':020000040800F2\n'
            sl.write(self.firstr_to_write)
            for name in self.location_dict.keys():
                #name = str(name).zfill(4)
                print(str(name).zfill(4),',,,',self.location_dict[name])
                if len(self.location_dict[name])==4:
                    self.str_without_check_to_write = '02'+str(name).zfill(4)+'00'+self.location_dict[name]#生成无校验的str
                else :
                    self.str_without_check_to_write = '04'+str(name).zfill(4)+'00'+self.location_dict[name]#生成无校验的str

                self.str_check = self.check_check(self.str_without_check_to_write)
                print('sdafdsf',self.str_check)
                self.str_to_write = ':'+self.str_without_check_to_write + self.str_check+'\n'#得到有校验位的
                sl.write(self.str_to_write)
                print('ok')
            self.main_begin = ':0400000508000000ef'+'\n'#本汇编器出来的代码默认0000开始
            sl.write(self.main_begin)
            self.last_to_write = ':00000001FF'+'\n'#文件结束
            sl.write(self.last_to_write)
'''

from_file = 'asm.txt'
filea = 'hex.txt'
a = change_into_hex(from_file,filea)
print('地址.......',a.location_dict)

print('global_label_data_dict',global_label_data_dict)
print('end')
.section.text
    addi x0,x0,0x0000
    addi x0,x0,0x0320
l:
    addi x1,x3,0x0123
.section.data
    k: 0x0912,0x1234

a.write_hex()
'''

'''
利用单次扫描后得到的相应字典
上面对每个label进行获取并转化
并存入新的地址-数据dict


'''




'''

def change_file():
    with open('ass.txt','r+') as assfile:
        with open('bin.txt','w+') as binfile:
            for line in assfile:
                changed = change_into_bin(line)
                chan = changed.after_change_str+'\n'
                binfile.write(chan)


change_file()
'''









#class_change = change_into_bin(str00)


#print(class_change.after_change_str)



















