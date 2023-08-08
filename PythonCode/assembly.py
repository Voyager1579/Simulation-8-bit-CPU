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