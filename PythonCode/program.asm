
    MOV ss,1
    MOV SP,0x10
    MOV D, 10

    push D
    push 1

    POP C
    POP B
    MOV A,C
    ADD A,B
    MOV D,A

    HLT;
