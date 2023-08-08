# coding=utf-8

import os
import pin
import assembly as ASM

# 三十二位的指令系统，通过十六进制表达指令信号
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'micro.bin')

# 初始化微指令内容，全部置暂停
micro = [pin.HLT for _ in range(0x10000)]

# 编译二地址指令函数
def compile_addr2(addr, ir, psw, index):
    global micro

    # 指令前四位为操作信号
    op = ir & 0xf0
    # 二地址指令中，第五到第六位为目标寄存器
    amd = (ir >> 2) & 3
    # 二地址指令中，第七到第八位为源（立即数，寄存器中的数据，寄存器直接地址，寄存器间接地址）
    ams = ir & 3

    INST = ASM.INSTRUCTIONS[2]
    # 查找是否存在这样的二地址操作
    if op not in INST:
        micro[addr] = pin.CYC
        return
    am = (amd, ams)
    # 查找是否存在这样的二地址操作数值key
    if am not in INST[op]:
        micro[addr] = pin.CYC
        return

    # 获取执行机器码(微指令)
    EXEC = INST[op][am]

    if index < len(EXEC):
        micro[addr] = EXEC[index]
    else:
        micro[addr] = pin.CYC


def compile_addr1(addr, ir, psw, index):
    pass


# 编译零地址指令函数
def compile_addr0(addr, ir, psw, index):
    global micro

    op = ir

    INST = ASM.INSTRUCTIONS[0]
    if op not in INST:
        micro[addr] = pin.CYC
        return

    EXEC = INST[op]
    if index < len(EXEC):
        micro[addr] = EXEC[index]
    else:
        micro[addr] = pin.CYC


for addr in range(0x10000):
    # 取addr参数的第九到第十六位，作为
    ir = addr >> 8
    # 取addr参数的第五到第八位，作为程序状态字
    psw = (addr >> 4) & 0xf
    # 取addr参数的第一到第四位，作为循环周期数
    cyc = addr & 0xf

    if cyc < len(ASM.FETCH):
        micro[addr] = ASM.FETCH[cyc]
        continue

    # 当ir第八位为1时，视作二地址指令操作
    addr2 = ir & (1 << 7)
    # 当ir第七位为1时，视作一地址指令操作
    addr1 = ir & (1 << 6)

    index = cyc - len(ASM.FETCH)

    if addr2:
        compile_addr2(addr, ir, psw, index)
    elif addr1:
        compile_addr1(addr, ir, psw, index)
    else:
        compile_addr0(addr, ir, psw, index)


with open(filename, 'wb') as file:
    for var in micro:
        value = var.to_bytes(4, byteorder='little')
        file.write(value)

print('Compile micro instruction finish!!!')