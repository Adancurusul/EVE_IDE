import os
import subprocess
import shutil
import _thread
path_evn = '/env_Eclipse'
path_drivers = '/drivers'
path_stubs = '/stubs'
target_path_eve = '/Eve'
target_path_app = '/App'
target_path_peripherals ="/Peripherals"
target_path_riscv ='/RISCV'
#target_path_start = '/START'

def read_line(name, li):  # 读取指定文件指定行
    with open(name, "r") as in_file:
        num = 0
        for line in in_file:
            num += 1
            if num == li:
                return line


def child_name(path):
    return os.listdir(path)

pp = 'D:/codes/test'
configure_file = 'configure.txt'

class do_make:
    def __init__(self, project_path,which_gcc,chip):
        if which_gcc == 'nuclei':
            self.GCC = 'riscv-nuclei-elf-gcc'
            self.OBJCOPY = 'riscv-nuclei-elf-objcopy'
            self.OBJDUMP = 'riscv-nuclei-elf-objdump'
            self.SIZE = 'riscv-nuclei-elf-size'
            self.G = 'riscv-nuclei-elf-g++'
        self.state=1

        self.pro_name = project_path.split('/')[-1]
        self.pro_path = project_path
        self.path = project_path+'/release'
        self._eve = self.path+target_path_eve
        #self._start = self._eve +target_path_start
        self._app = self.path+target_path_app
        self._riscv = self.path +target_path_riscv
        self._peripherals = self.path+target_path_peripherals

        self.source_eve = self.pro_path+'/Eve'



        #source文件夹
        self.source_rv = self.pro_path+'/RISCV'
        self.s_drivers =self.source_rv+path_drivers
        self.s_evn_path =self.source_rv+path_evn
        self.s_stubs = self.source_rv+path_stubs
        self.s_app = self.pro_path+'/Application'
        self.s_peripherals = self.pro_path+'/Peripherals'
        self.s_source = self.s_peripherals+'/Source'
        self.s_include = self.s_peripherals+'/Include'


        # target文件夹
        self.target_drivers = self._riscv + path_drivers
        self.target_evn = self._riscv + path_evn
        self.target_stubs = self._riscv + path_stubs
        self.target_source = self._peripherals+'/Source'
        self.target_peripherals = self._peripherals
        self.target_app =self._app
        #self.target_start = self._start

        #makefile文件
        self.make_evn = self.target_evn + '/sub.mk'
        self.make_app = self.target_app+'/sub.mk'
        self.make_stubs = self.target_stubs+'/sub.mk'
        self.make_source = self.target_source +'/sub.mk'
        self.make_drivers = self.target_drivers +'/sub.mk'
        self.make_peripherals = self.target_peripherals +'/sub.mk'
        self.main_source = self.path+'/source.mk'
        self.main_object = self.path + '/object.mk'
        self.main_make = self.path+'/makefile'
        #require self.listof make file
        #dir的list是一一对应的
        self.dir_soucelist = [self.pro_path,self.s_app,self.s_peripherals,self.source_rv,self.s_source,
                              self.s_stubs,self.s_drivers,self.s_evn_path]
        self.dir_targetlist = [self.path, self.target_app, self.target_peripherals, self._riscv, self.target_source,
                               self.target_stubs, self.target_drivers, self.target_evn]

        self.souce_target_dict = {}
        for i in range(len(self.dir_soucelist)):
            s = self.dir_soucelist[i]
            t = self.dir_targetlist[i]
            self.souce_target_dict.setdefault(s,t)


        self.make_list =[self.main_make,self.main_object,self.main_source,self.make_drivers,self.make_stubs,
                         self.make_evn,self.make_peripherals,self.make_source,self.make_app]
        self.corresponding_dict_A = {self.s_app:self.make_app,self.s_evn_path:self.make_evn,self.s_peripherals:self.make_peripherals
                                   ,self.s_drivers:self.make_drivers,self.s_stubs:self.make_stubs,self.s_source:self.make_source}
        self.corresponding_dict_B = {self.make_app:self.s_app,self.make_evn:self.s_evn_path,self.make_peripherals:self.s_peripherals
                                   ,self.make_drivers:self.s_drivers,self.make_stubs:self.s_stubs,self.make_source:self.s_source}

        self.gcc_i_path = [self.s_include,self.s_source,self.s_drivers,self.s_evn_path,self.s_stubs,self.s_peripherals,self.s_app]



    def create_path_gd(self):
        if os.path.exists(self.path):
            self.state =0
            #self.do_make()
        else:
            #创建target文件夹
            for dir in self.dir_targetlist:
                os.makedirs(dir)

            #创建空makefile文件
            for _file in self.make_list:
                f = open(_file, "w")
                f.write("#"*44+'\n')  # 写入文件，空
                f.write("#  Automatically generated by Eve ide \n")
                f.write("#  Please don't edit                  \n")
                f.write("#"*44+"\n")
                f.close()  # 执行完结束


            #self.create


    def create_sub_makefile_gd(self):


        for sub_file in self.corresponding_dict_B.keys():
            self.do_create(sub_file)
    def do_create(self,sub_file):
            source_p = self.corresponding_dict_B[sub_file]
            target_p = self.souce_target_dict[source_p]
            file_name = []
            file_path = []
            s_path = []
            s_path_d = []
            o_path = []
            d_path = []
            s_exist = 0
            for name in child_name(source_p):
                source_file = source_p+'/'+name

                if os.path.isfile(source_file):
                    s_file = target_p+'/'+name
                    if s_file[-2:] =='.c':
                        s_file = s_file.replace(self.path,".")
                        s_o = s_file.replace('.c','.o')
                        s_d = s_file.replace('.c','.d')
                        #print(s_d)
                        #s__d = s_file.replace('.S','.d')
                        o_path.append(s_o)
                        d_path.append(s_d)
                        #d_path.append(s__d)
                        file_name.append(name)
                        file_path.append(s_file)
                        #print(d_path)
                    elif s_file[-2:]=='.S':
                        s_file = s_file.replace(self.path, ".")
                        #print("find s")
                        s_o = s_file.replace('.S','.o')
                        s_d = s_file.replace('.S', '.d')
                        s_path_d.append(s_d)
                        o_path.append(s_o)
                        s_path.append(s_file)
                        s_exist = 1



            source_path =source_p.replace(self.pro_path,"..")
            target_path = target_p.replace(self.path+'/',"")
            _c_srcs = " \\\n".join(file_path)

            _objs = ' \\\n'.join(o_path)
            _c_deps = ' \\\n'.join(d_path)
            sub_name = {'c_srcs':_c_srcs,'c_deps':_c_deps,'objs':_objs,'d_deps':_c_deps,'source_path':source_path,'target_path':target_path,'gcc' :self.GCC,
                        'application':self.s_app,'peripherals':self.s_peripherals,'include':self.s_include,'source':self.s_source,
                        'stubs':self.s_stubs,'drivers':self.s_drivers,'evn':self.s_evn_path}



            with open(sub_file,"r+") as mk:

                mk.write("C_SRCS += \\\n\
{c_srcs} \n\
\n\
OBJS += \\\n\
{objs} \n\
\n\
\n\
C_DEPS += \\\n\
{d_deps}\n\
\n\
\n\
".format(**sub_name))

                if s_exist:
                    st = (" \\\n").join(s_path)
                    mk.write("S_UPPER_SRCS += \\\n"+st+" \n\n")
                    std= (" \\\n").join(s_path_d)
                    mk.write("S_UPPER_DEPS += \\\n"+std+"\n\n")
                    mk.write("{target_path}/%.o: {source_path}/%.S\n\t\
{gcc} -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -I\"{application}\" -I\"{peripherals}\" -I\"{include}\" -I\"{source}\" -I\"{stubs}\" -I\"{drivers}\" -I\"{evn}\" -std=gnu11 -MMD -MP -MF\"$(@:%.o=%.d)\" -MT\"$(@)\" -c -o \"$@\" \"$<\"\n\
".format(**sub_name))
                    s_exist=0


                mk.write("{target_path}/%.o: {source_path}/%.c\n\t\
{gcc} -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -I\"{application}\" -I\"{peripherals}\" -I\"{include}\" -I\"{source}\" -I\"{stubs}\" -I\"{drivers}\" -I\"{evn}\" -std=gnu11 -MMD -MP -MF\"$(@:%.o=%.d)\" -MT\"$(@)\" -c -o \"$@\" \"$<\"\n\
".format(**sub_name))


                    

    def create_makefile_obj_source_gd(self):
        name_dir = {'name' :self.pro_name,'elf' :self.pro_name+".elf",'map':self.pro_name+'.map','siz':self.pro_name+".siz",
                    'lds':self.s_evn_path+"/GD32VF103xB.lds",'bin':self.pro_name+".bin",
                    'lst':self.pro_name+".lst",'hex':self.pro_name+".hex",'gcc' :self.GCC, 'g' :self.G,'objcopy':self.OBJCOPY,
                    'objdump':self.OBJDUMP,'size':self.SIZE}#用于格式化makefile的字典
        with open(self.main_object,"r+") as obj_file:
            obj_file.write('\n'*3+'USER_OBJS :=\n'+'\n'+'LIBS :=\n')
        '''
        USER_OBJS :=

        LIBS :=
        '''
        with open(self.main_source,"r+") as source_file:
            source_file.write("ELF_SRCS :=\n" 
                "C_UPPER_SRCS :=\n"
                "CXX_SRCS :=\n"
                "C++_SRCS :=\n"
                "OBJ_SRCS :=\n"
                "CC_SRCS :=\n"
                "ASM_SRCS :=\n"
                "C_SRCS :=\n"
                "CPP_SRCS :=\n"
                "S_UPPER_SRCS :=\n"
                "O_SRCS :=\n"
                "CC_DEPS :=\n"
                "C++_DEPS :=\n"
                "OBJS :=\n"
                "C_UPPER_DEPS :=\n"
                "CXX_DEPS :=\n"
                "SECONDARY_FLASH :=\n"
                "SECONDARY_LIST :=\n"
                "SECONDARY_SIZE :=\n"
                "ASM_DEPS :=\n"
                "S_UPPER_DEPS :=\n"
                "C_DEPS :=\n"
                "CPP_DEPS :=\n")
            source_file.write('\n'*3)
            source_file.write("SUBDIRS := \\\n")
            t = self.dir_targetlist
            t.remove(self.path)
            d = []
            for i in t:
                i =i.replace(self.path+"/","")
                d.append(i)
                #print(i)
            st = " \\\n".join(d)
            source_file.write(st)

        with open(self.main_make,"r+") as make_file:
            make_file.write("\n-include ../makefile.init\n")
            make_file.write('\n'*3+"RM := rm -rf\n")
            m = self.make_list

            m.remove(self.main_make)
            #print(m)
            h=[]
            for i in m:
                i = i.replace(self.path+"/","")
                h.append(i)
            st  = "\n-include ".join(h)
            st = "\n-include "+st+"\n\n"
            make_file.write(st)
            make_file.write(
            "ifneq ($(MAKECMDGOALS),clean)\n"
            "ifneq ($(strip $(CC_DEPS)),)\n"
            "-include $(CC_DEPS)\n"
            "endif\n"
            "ifneq ($(strip $(C++_DEPS)),)\n"
            "-include $(C++_DEPS)\n"
            "endif\n"
            "ifneq ($(strip $(C_UPPER_DEPS)),)\n"
            "-include $(C_UPPER_DEPS)\n"
            "endif\n"
            "ifneq ($(strip $(CXX_DEPS)),)\n"
            "-include $(CXX_DEPS)\n"
            "endif\n"
            "ifneq ($(strip $(ASM_DEPS)),)\n"
            "-include $(ASM_DEPS)\n"
            "endif\n"
            "ifneq ($(strip $(S_UPPER_DEPS)),)\n"
            "-include $(S_UPPER_DEPS)\n"
            "endif\n"
            "ifneq ($(strip $(C_DEPS)),)\n"
            "-include $(C_DEPS)\n"
            "endif\n"
            "ifneq ($(strip $(CPP_DEPS)),)\n"
            "-include $(CPP_DEPS)\n"
            "endif\n"
            "endif\n"
            
            "-include ../makefile.defs\n"
            )

            main_str = "SECONDARY_FLASH +=  \\\n\
{hex} \\\n\
\n\
SECONDARY_LIST += \\\n\
{lst} \\\n\
\n\
SECONDARY_SIZE += \\\n\
{siz} \\\n\
\n\
all: {elf} secondary-outputs\n\
{elf}: $(OBJS) $(USER_OBJS)\n\
	@echo 'Building target: $@'\n\
	@echo 'Invoking: GNU RISC-V Cross C++ Linker'\n\
	{g} -march=rv32i -mabi=ilp32 -mcmodel=medlow -msmall-data-limit=8 -Os -fmessage-length=0 -fsigned-char -ffunction-sections -fdata-sections -fno-common  -g -T \"{lds}\" -nostartfiles -Xlinker --gc-sections -Wl,-Map,\"{map}\" --specs=nano.specs -o \"{elf}\" $(OBJS) $(USER_OBJS) $(LIBS)\n\
	@echo 'Finished building target: $@'\n\
	@echo ' '\n\
{bin}: {elf} \n\t\
{objcopy} -O binary \"{elf}\"  \"{bin}\"\n\
\n\
{hex}: {elf}\n\
	{objcopy} -O ihex \"{elf}\"  \"{hex}\"\n\
\n\
{lst}: {elf}\n\
	{objdump} --source --all-headers --demangle --line-numbers --wide \"{elf}\" > \"{lst}\"\n\
\n\
{siz}: {elf}\n\
	{size} --format=berkeley \"{elf}\"\n\
\n\
clean:\n\
	-$(RM) $(CC_DEPS)$(C++_DEPS)$(OBJS)$(C_UPPER_DEPS)$(CXX_DEPS)$(SECONDARY_FLASH)$(SECONDARY_LIST)$(SECONDARY_SIZE)$(ASM_DEPS)$(S_UPPER_DEPS)$(C_DEPS)$(CPP_DEPS) {elf}\n\
\n\
secondary-outputs: $(SECONDARY_FLASH) $(SECONDARY_LIST) $(SECONDARY_SIZE)\n\
\n\
.PHONY: all clean dependents\n\
\n\
-include ../makefile.targets".format(**name_dir)
            make_file.write(main_str)




    def do_make_gd(self):
        gcc_path = read_line(configure_file,6)[:-1]
        #(gcc_path)
        print('make_now'+gcc_path)
        cmd = "make all -C "+self.path
        #obj = subprocess.Popen("mkdir t3", shell=True, cwd='/tmp/')
        pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,cwd = gcc_path).stdout
        li_re = pipe.readlines()
        for i in li_re:
            i = str(i,encoding='utf-8')
            print(i)





    #m = do_make(pp,0)
#m.create_path()
#print(child_name(pp))











class make_project:
    def __init__(self, project_path,which_gcc):
        if which_gcc == 'nuclei':
            GCC = 'riscv-nuclei-elf-gcc'
            OBJCOPY = 'riscv-nuclei-elf-objcopy'
            OBJDUMP = 'riscv-nuclei-elf-objdump'
            SIZE = 'riscv-nuclei-elf-size'

        self.path = project_path
        self.release = self.path+'/release'
        self.source_list = []
        self.corresponding_dict = {}

        self.dirs = child_name(self.path)
        self.create_dict(self.path,self.dirs,self.corresponding_dict,None)




    def create_makefile_obj_source(self):
        name_dir = {'name' :self.pro_name,'elf' :self.pro_name+".elf",'map':self.pro_name+'.map','siz':self.pro_name+".siz",
                    'lds':self.s_evn_path+"/GD32VF103xB.lds",'bin':self.pro_name+".bin",
                    'lst':self.pro_name+".lst",'hex':self.pro_name+".hex",'gcc' :self.GCC, 'g' :self.G,'objcopy':self.OBJCOPY,
                    'objdump':self.OBJDUMP,'size':self.SIZE}#用于格式化makefile的字典
        with open(self.main_object,"r+") as obj_file:
            obj_file.write('\n'*3+'USER_OBJS :=\n'+'\n'+'LIBS :=\n')
        '''
        USER_OBJS :=
        LIBS :=
        '''
        with open(self.main_source,"r+") as source_file:
            source_file.write("ELF_SRCS :=\n" 
                "C_UPPER_SRCS :=\n"
                "CXX_SRCS :=\n")
'''
auto_make = do_make(pp,'nuclei','gd')
auto_make.create_path_gd()
if auto_make.state:
    auto_make.create_makefile_obj_source_gd()
    auto_make.create_sub_makefile_gd()
    auto_make.do_make_gd()
else:
    auto_make.do_make_gd()
'''