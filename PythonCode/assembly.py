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

MOV = (0 << pin.ADDR2_SHIFT) | pin.ADDR2
ADD = (1 << pin.ADDR2_SHIFT) | pin.ADDR2
SUB = (2 << pin.ADDR2_SHIFT) | pin.ADDR2
CMP = (3 << pin.ADDR2_SHIFT) | pin.ADDR2
AND = (4 << pin.ADDR2_SHIFT) | pin.ADDR2
OR  = (5 << pin.ADDR2_SHIFT) | pin.ADDR2
XOR = (6 << pin.ADDR2_SHIFT) | pin.ADDR2

INC = (0 << pin.ADDR1_SHIFT) | pin.ADDR1
DEC = (1 << pin.ADDR1_SHIFT) | pin.ADDR1
NOT = (1 << pin.ADDR1_SHIFT) | pin.ADDR1

NOP = 0
HLT = 0x3f

#定义指令字典,遵从Key-Value原则
INSTRUCTIONS = {
    2: {
        # 为Mov指令时，寄存器赋值
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
        },
        # 加法指令
        ADD: {
            #为立即数Mov时，key为立即数传值(1,0)时
            (pin.AM_REG, pin.AM_INS): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 对B寄存器进行立即数赋值
                pin.SRC_OUT | pin.B_IN,
                # 将计算结果输出至源寄存器
                pin.OP_ADD | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            (pin.AM_REG, pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将源寄存器中指向的寄存器的值赋值于B寄存器
                pin.SRC_R | pin.B_IN,
                # 将计算结果输出至源寄存器
                pin.OP_ADD | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        # 减法指令
        SUB: {
            #为立即数Mov时，key为立即数传值(1,0)时
            (pin.AM_REG, pin.AM_INS): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 对B寄存器进行立即数赋值
                pin.SRC_OUT | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_SUB | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            (pin.AM_REG, pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将源寄存器中指向的寄存器的值赋值于B寄存器
                pin.SRC_R | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_SUB | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        CMP: {
            (pin.AM_REG, pin.AM_INS): [
                pin.DST_R | pin.A_IN,
                pin.SRC_OUT | pin.B_IN,
                pin.OP_SUB | pin.ALU_PSW
            ],
            (pin.AM_REG, pin.AM_REG): [
                pin.DST_R | pin.A_IN,
                pin.SRC_R | pin.B_IN,
                pin.OP_SUB | pin.ALU_PSW
            ],
        },
        AND: {
            (pin.AM_REG, pin.AM_INS): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 对B寄存器进行立即数赋值
                pin.SRC_OUT | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_AND | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            (pin.AM_REG, pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将源寄存器中指向的寄存器的值赋值于B寄存器
                pin.SRC_R | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_AND | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        OR: {
            (pin.AM_REG, pin.AM_INS): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 对B寄存器进行立即数赋值
                pin.SRC_OUT | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_OR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            (pin.AM_REG, pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将源寄存器中指向的寄存器的值赋值于B寄存器
                pin.SRC_R | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_OR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        },
        XOR: {
            (pin.AM_REG, pin.AM_INS): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 对B寄存器进行立即数赋值
                pin.SRC_OUT | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_XOR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
            (pin.AM_REG, pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将源寄存器中指向的寄存器的值赋值于B寄存器
                pin.SRC_R | pin.B_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_XOR | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ],
        }

    },
    1: {
        INC: {
            (pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_INC | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ]
        },
        DEC: {
            (pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_DEC | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ]
        },
        NOT: {
            (pin.AM_REG): [
                # 将目标寄存器中的数写入A寄存器
                pin.DST_R | pin.A_IN,
                # 将计算结果输出至目标寄存器
                pin.OP_NOT | pin.ALU_OUT | pin.DST_W | pin.ALU_PSW
            ]
        }
    },
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