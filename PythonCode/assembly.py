# coding =utf-8

import pin

FETCH = [
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.IR_IN | pin.PC_INC,
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.DST_IN | pin.PC_INC,
    pin.PC_OUT | pin.MAR_IN,
    pin.RAM_OUT | pin.SRC_IN | pin.PC_INC,
]

MOV = 0 | pin.ADDR2
ADD = (1 << pin.ADDR2_SHIFT) | pin.ADDR2

NOP = 0
HLT = 0x3f

#定义指令字典,遵从Key-Value原则
INSTRUCTIONS = {
    2: {
        # 为Mov指令时
        MOV: {
            #为立即数Mov时，key为立即数传值(1,0)时
            (pin.AM_REG, pin.AM_INS): [
                # 将源寄存器中的数写入目标寄存器
                pin.DST_W | pin.SRC_OUT,
            ],
            (pin.AM_REG, pin.AM_REG): [
                # 寄存器寻址会将源寄存器中的寄存器中的数写入目标寄存器
                pin.DST_W | pin.SRC_R,
            ],
            (pin.AM_REG, pin.AM_DIR): [
                # 直接寻址取值，从RAM寄存器中按地址取，与寄存器寻址不同
                # 先将SRC寄存器中的数输入到数据总线，MAR读入
                # RAM输出，目标寄存器写入
                pin.SRC_OUT | pin.MAR_IN,
                pin.DST_W | pin.RAM_OUT
            ],
            (pin.AM_REG, pin.AM_RAM): [
                # 间接寻址取值，从SRC中获取寄存器中的地址
                pin.SRC_R | pin.MAR_IN,
                pin.DST_W | pin.RAM_OUT
            ],
            (pin.AM_DIR, pin.AM_INS): [
                # 寄存器数值写入，往RAM寄存器写入立即数
                # 将目标寄存器中的值写入MAR
                pin.DST_OUT | pin.MAR_IN,
                # 将源寄存器中的值传入数据总线，RAM寄存器接收
                pin.RAM_IN | pin.SRC_OUT
            ],
            (pin.AM_DIR, pin.AM_REG): [
                # 寄存器数值写入，往RAM寄存器写入立即数
                # 将目标寄存器中的值写入MAR
                pin.DST_OUT | pin.MAR_IN,
                # 将源寄存器中的目标寄存器的值传入数据总线，RAM寄存器接收
                pin.RAM_IN | pin.SRC_R
            ],
            (pin.AM_DIR, pin.AM_DIR): [
                # 寄存器RAM之间直接传值
                pin.SRC_OUT | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_OUT | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ],
            (pin.AM_DIR, pin.AM_RAM): [
                # 寄存器RAM之间间接传值
                pin.SRC_R | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_OUT | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ],
            (pin.AM_RAM, pin.AM_INS): [
                # 寄存器数值写入，往RAM寄存器写入立即数
                # 将目标寄存器中的值写入MAR
                pin.DST_R | pin.MAR_IN,
                # 将源寄存器中的值传入数据总线，RAM寄存器接收
                pin.RAM_IN | pin.SRC_OUT
            ],
            (pin.AM_RAM, pin.AM_REG): [
                # 寄存器数值写入，往RAM寄存器写入立即数
                # 将目标寄存器中的值写入MAR
                pin.DST_R | pin.MAR_IN,
                # 将源寄存器中的目标寄存器的值传入数据总线，RAM寄存器接收
                pin.RAM_IN | pin.SRC_R
            ],
            (pin.AM_RAM, pin.AM_DIR): [
                # 寄存器RAM之间直接传值
                pin.SRC_OUT | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_R | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ],
            (pin.AM_RAM, pin.AM_RAM): [
                # 寄存器RAM之间间接传值
                pin.SRC_R | pin.MAR_IN,
                pin.RAM_OUT | pin.T1_IN,
                pin.DST_R | pin.MAR_IN,
                pin.RAM_IN | pin.T1_OUT
            ]
        }
    },
    1: {},
    0: {
        NOP: [
            pin.CYC,
        ],
        HLT: [
            pin.HLT,
        ]
    }
}

INST = INSTRUCTIONS[2]
print()
print(len(INST[MOV][1,0]))