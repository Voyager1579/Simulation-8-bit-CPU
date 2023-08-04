# coding = utf-8

# 管脚对应着电位信号,_OUT后缀为读信号，_IN后缀为写信号
MSR = 1 # 机器状态寄存器
MAR = 2 # 内存地址寄存器
MDR = 3 # 内存数据寄存器
RAM = 4 # 随机访问存储器
IR = 5 # 指令寄存器
DST = 6 # 目标寄存器
SRC = 7 # 源寄存器

A = 8
B = 9
C = 10
D = 11
DI = 12 # 目标索引寄存器
SI = 13 # 源索引寄存器
SP = 14 # 堆栈指针

BP = 15 # 基址指针
CS = 16 # 代码段寄存器
DS = 17 # 数据段寄存器
SS = 18 # 堆栈段寄存器
ES = 19 # 附加段寄存器
VEC = 20 # 向量寄存器
T1 = 21 # 临时寄存器1
T2 = 22 # 临时寄存器2

MSR_OUT = MSR 
MAR_OUT = MAR 
MDR_OUT = MDR 
RAM_OUT = RAM 
IR_OUT = IR
DST_OUT = DST
SRC_OUT = SRC

A_OUT = A
B_OUT = B
C_OUT = C
D_OUT = D
DI_OUT = DI
SI_OUT = SI
SP_OUT = SP

BP_OUT = BP
CS_OUT = CS
DS_OUT = DS
SS_OUT = SS
ES_OUT = ES
VEC_OUT = VEC
T1_OUT = T1
T2_OUT = T2

_DST_SHIFT = 5

MSR_IN = MSR << _DST_SHIFT
MAR_IN = MAR << _DST_SHIFT
MDR_IN = MDR << _DST_SHIFT
RAM_IN = RAM << _DST_SHIFT
IR_IN = IR << _DST_SHIFT
DST_IN = DST << _DST_SHIFT
SRC_IN = SRC << _DST_SHIFT

A_IN = A << _DST_SHIFT
B_IN = B << _DST_SHIFT
C_IN = C << _DST_SHIFT
D_IN = D << _DST_SHIFT
DI_IN = DI << _DST_SHIFT
SI_IN = SI << _DST_SHIFT
SP_IN = SP << _DST_SHIFT

BP_IN = BP << _DST_SHIFT
CS_IN = CS << _DST_SHIFT
DS_IN = DS << _DST_SHIFT
SS_IN = SS << _DST_SHIFT
ES_IN = ES << _DST_SHIFT
VEC_IN = VEC << _DST_SHIFT
T1_IN = T1 << _DST_SHIFT
T2_IN = T2 << _DST_SHIFT

SRC_R = 2 ** 10 # 源寄存器
SRC_W = 2 ** 11

DST_R = 2 ** 12 # 目标寄存器
DST_W = 2 ** 13

PC_WE = 2 ** 14 # 程序计数器
PC_CS = 2 ** 15
PC_EN = 2 ** 16

# 直接为PC设置操作信号
PC_OUT = PC_CS
PC_IN = PC_CS | PC_WE
PC_INC = PC_CS | PC_WE | PC_EN

CYC = 2 ** 30
HLT = 2 ** 31

# 定义地址指令信号
ADDR2 = 1 << 7
ADDR1 = 1 << 6
# 定义偏移量
ADDR2_SHIFT = 4
ADDR1_SHIFT = 2
# 从上到下分别为：立即寻址信号，寄存器寻址信号，直接寻址信号，寄存器间接寻址信号
AM_INS = 0
AM_REG = 1
AM_DIR = 2
AM_RAM = 3
