# 八位二进制CPU的设计和实现

## 寄存器

- PC 程序计数器
- ALU
- PSW/FLAG 程序状态字
- A 寄存器
- B 寄存器
- C 寄存器
- D 寄存器
- IR 指令寄存器
- DST 目的操作数寄存器
- SRC 目的操作数寄存器

- MSR 存储器段寄存器
- MAR 存储器地址寄存器
- MDR 存储器数据奇存器
- MC 内存控制器

- SP 堆栈指针寄存器
- BP 基址寄存器
- SI 源变址寄存器
- DI 目的变址寄存器
- CS 代码段寄存器
- DS 数据段寄存器
- SS 堆栈段寄存器
- ES 附加段寄存器

- TMP 临时寄存器若干

## 指令系统

### 指令

- 二操作数: 3bit 最高位为1
    - mov dst, src
    - add dst, src
    - sub dst, src
    - cmp op1,  op2
    - and dst, src
    - or dst, src
    - xor dst, src
- 一操作数: 此最高位为1
    - inc src//可用add 实现
    - dec src// 可用sub 实现
    - not src 
    - call dst
    - jmp dst
    - jo dst
    - jno dst
    - jz dst
    - jnz dst
    - push src
    - pop dst
    - int dst
- 零操作数:
    - nop
    - hlt
    - ret
    - iret

### 寻址地址 2 x 3 bit

- 立即寻址 MOV A5
- 寄存器寻址 MOV AB
- 直接寻址 MOV A [5]
- 寄存器间接寻址 MOV A [B]


### 程序状态字 4bit
- OF 溢出标志
- ZF 零标志
- PF 奇偶标志
- IF 中断标志

### 指令周期 4 bit



