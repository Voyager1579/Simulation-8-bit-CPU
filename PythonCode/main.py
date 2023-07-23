import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname,'ins.bin')

WE_A = 2 ** 0  # 000X
CS_A = 2 ** 1  # 00X0

WE_B = 2 ** 2  # 0X00
CS_B = 2 ** 3  # X000

WE_C = 2 ** 4
CS_C = 2 ** 5

ALU_ADD = 0
ALU_SUB = 2 ** 6
ALU_EN = 2 ** 7

WE_MC = 2 ** 8
CS_MC = 2 ** 9

WE_PC = 2 ** 10
EN_PC = 2 ** 11
CS_PC = 2 ** 12

HLT = 2 ** 15

micro = [
    CS_MC | CS_A | WE_A | WE_PC | EN_PC| CS_PC,
    HLT,
]

with open(filename, 'wb') as file:
    for value in micro:
        result = value.to_bytes(2,byteorder='little')
        file.write(result)
        print(value, result)


# byteorder决定了内存的大小端存储，为大端时会把数据的高字节存储在内存的低地址中（更符合人类阅读习惯），小段会把数据的高字节存储再内存的高地址中（更符合计算机处理数据）
# 如本行代码中，三个变量进行按位或后得到值 515，大端输出为0203，小端输出为0302;
print((CS_MC | CS_A | WE_A).to_bytes(2, byteorder='big'))
