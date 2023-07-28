import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'ins.bin')

A_WE = 2 ** 0  # 000X
A_CS = 2 ** 1  # 00X0

B_WE = 2 ** 2  # 0X00
B_CS = 2 ** 3  # X000


ALU_ADD = 0
ALU_SUB = 2 ** 4
ALU_EN = 2 ** 5

C_WE = 2 ** 6
C_CS = 2 ** 7

MC_WE = 2 ** 8
MC_CS = 2 ** 9

PC_WE = 2 ** 10
PC_EN = 2 ** 11
PC_CS = 2 ** 12

HLT = 2 ** 15

micro = [
    MC_CS | A_CS | A_WE | PC_WE | PC_EN | PC_CS,
    MC_CS | B_CS | B_WE | PC_WE | PC_EN | PC_CS,
    ALU_EN | C_CS | C_WE,
    HLT,
]

with open(filename, 'wb') as file:
    for value in micro:
        result = value.to_bytes(2, byteorder='little')
        file.write(result)
        print(value, result)


# byteorder决定了内存的大小端存储，为大端时会把数据的高字节存储在内存的低地址中（更符合人类阅读习惯），小段会把数据的高字节存储再内存的高地址中（更符合计算机处理数据）
# 如本行代码中，三个变量进行按位或后得到值 515，大端输出为0203，小端输出为0302;
print((MC_CS | A_CS | A_WE).to_bytes(2, byteorder='big'))
